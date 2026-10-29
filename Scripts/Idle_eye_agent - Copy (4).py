import time
import requests
import socket
from ctypes import Structure, windll, c_uint, byref
from datetime import datetime, timedelta, date
import ctypes
from ctypes import wintypes
import json
import os
import pytz
import signal
import atexit
import sys
import traceback

# === CONFIGURATION ===
DJANGO_API_URL = "http://192.168.5.249:8000/api/log_event/"
IDLE_THRESHOLD = 180           # seconds -> when we consider user idle
IDLE_INCREMENT = 60            # seconds -> how often to increment idle minutes while idle
CHECK_INTERVAL = 10            # polling interval in seconds
END_OF_DAY_THRESHOLD = 1800    # seconds (30 minutes) -> treat long idle as end-of-day

# === TIMEZONE ===
IST = pytz.timezone("Asia/Kolkata")

SAFE_DIR = os.getenv("LOCALAPPDATA") or os.getenv("TEMP") or "."
STATE_FILE = os.path.join(SAFE_DIR, "agent_state.json")


def now_ist():
    return datetime.now(IST).replace(microsecond=0)


def parse_state_time(s):
    try:
        return IST.localize(datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))
    except Exception:
        return None


def format_time(dt):
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.astimezone(IST).replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def get_idle_time():
    class LASTINPUTINFO(Structure):
        _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = 8
    try:
        if not windll.user32.GetLastInputInfo(byref(lii)):
            return 0.0
        millis = windll.kernel32.GetTickCount() - lii.dwTime
        return max(0.0, millis / 1000.0)
    except Exception:
        return 0.0


def get_logged_in_username():
    try:
        session_id = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()
        WTSUserNameBuffer = ctypes.c_wchar_p()
        WTSDomainNameBuffer = ctypes.c_wchar_p()
        bytesReturned = wintypes.DWORD()

        ctypes.windll.Wtsapi32.WTSQuerySessionInformationW(None, session_id, 5,
                                                          ctypes.byref(WTSUserNameBuffer),
                                                          ctypes.byref(bytesReturned))
        ctypes.windll.Wtsapi32.WTSQuerySessionInformationW(None, session_id, 7,
                                                          ctypes.byref(WTSDomainNameBuffer),
                                                          ctypes.byref(bytesReturned))

        if WTSUserNameBuffer and WTSUserNameBuffer.value:
            username = WTSUserNameBuffer.value
            domain = WTSDomainNameBuffer.value
            ctypes.windll.Wtsapi32.WTSFreeMemory(WTSUserNameBuffer)
            ctypes.windll.Wtsapi32.WTSFreeMemory(WTSDomainNameBuffer)
            return f"{domain}\\{username}"
    except Exception:
        pass
    return "Unknown"


def send_idle_event_to_server(from_time, to_time, idle_minutes, first_activity_time=None, last_activity_time=None, last_work_time=None):
    """
    Sends idle/activity payload to Django API.
    All time args should be timezone-aware datetimes or strings in "%Y-%m-%d %H:%M:%S" IST.
    """
    try:
        # ensure datetimes
        if isinstance(from_time, datetime):
            from_time_ist = from_time.astimezone(IST).replace(microsecond=0)
        else:
            from_time_ist = parse_state_time(from_time) or now_ist()

        if isinstance(to_time, datetime):
            to_time_ist = to_time.astimezone(IST).replace(microsecond=0)
        else:
            to_time_ist = parse_state_time(to_time) or now_ist()

        # ensure session_start is provided: use first_activity_time if available, otherwise use from_time_ist
        session_start_val = first_activity_time or format_time(from_time_ist)

        payload = {
            # *** IMPORTANT: use 'session_start' key so your Django view accepts it ***
            "session_start": session_start_val,
            "last_activity": last_activity_time,
            "last_work_time": last_work_time,
            "username": get_logged_in_username(),
            "hostname": socket.gethostname(),
            "from_time": from_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "to_time": to_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "idle_minutes": idle_minutes,
        }

        # debug print payload (optional; remove in production)
        # print("[DEBUG] payload:", payload)

        try:
            response = requests.post(DJANGO_API_URL, json=payload, timeout=5)
            print(f"[+] Sent payload: idle_minutes={idle_minutes} {from_time_ist} -> {to_time_ist} (status: {response.status_code})")
            # if response.status_code != 201: print(response.text)
        except Exception as e:
            print(f"[!] Failed to POST to server: {e}")
    except Exception as e:
        print(f"[!] send_idle_event_to_server unexpected error: {e}")
        traceback.print_exc()



def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return {
                "idle_time_today": data.get("idle_time_today", 0.0),
                "idle_date": data.get("idle_date", str(date.today())),
                "first_activity_time": data.get("first_activity_time", None),
                "last_activity_time": data.get("last_activity_time", None),
                "last_work_time": data.get("last_work_time", None)
            }
    except Exception:
        # return fresh state
        return {
            "idle_time_today": 0.0,
            "idle_date": str(date.today()),
            "first_activity_time": None,
            "last_activity_time": None,
            "last_work_time": None
        }


def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"[!] Failed to save state: {e}")


# Graceful exit: save state and send final heartbeat
_exit_hooks_registered = False
_state_for_exit = None


def on_exit(signum=None, frame=None):
    global _state_for_exit
    try:
        if _state_for_exit is None:
            return
        state = _state_for_exit
        print(f"[INFO] Exiting agent (signal={signum}). Saving state and sending final heartbeat...")

        # determine last_activity_time and last_work_time for payload
        last_activity = state.get("last_activity_time")
        last_work = state.get("last_work_time") or last_activity

        # Attempt to send one final event indicating last known activity
        try:
            if last_activity:
                from_dt = parse_state_time(last_activity) or now_ist()
            else:
                from_dt = now_ist()

            to_dt = now_ist()
            send_idle_event_to_server(from_dt, to_dt, 0,
                                      first_activity_time=state.get("first_activity_time"),
                                      last_activity_time=state.get("last_activity_time"),
                                      last_work_time=state.get("last_work_time"))
        except Exception as e:
            print(f"[!] Final heartbeat failed: {e}")

        save_state(state)
        print("[INFO] State saved. Exiting now.")
    except Exception:
        traceback.print_exc()
    finally:
        # ensure process exits
        try:
            sys.exit(0)
        except SystemExit:
            pass


def register_exit_handlers(state_ref):
    global _exit_hooks_registered, _state_for_exit
    if _exit_hooks_registered:
        return
    _state_for_exit = state_ref
    atexit.register(on_exit)
    # signals (Windows supports SIGINT, SIGBREAK; SIGTERM may be supported depending on context)
    try:
        signal.signal(signal.SIGINT, on_exit)
    except Exception:
        pass
    try:
        signal.signal(signal.SIGTERM, on_exit)
    except Exception:
        pass
    try:
        signal.signal(signal.SIGBREAK, on_exit)
    except Exception:
        pass
    _exit_hooks_registered = True


def main():
    print(f"[*] Idle tracking agent started. State file: {STATE_FILE}")
    state = load_state()
    register_exit_handlers(state)

    # runtime trackers
    idle_start_time = None
    last_logged_seconds = 0

    # last_activity_time should be updated whenever user is active (idle < IDLE_THRESHOLD)
    # first_activity_time set on first activity of the day
    while True:
        try:
            today_str = str(date.today())
            if state.get("idle_date") != today_str:
                # reset daily values
                state["idle_time_today"] = 0.0
                state["idle_date"] = today_str
                state["first_activity_time"] = None
                state["last_activity_time"] = None
                state["last_work_time"] = None
                idle_start_time = None
                last_logged_seconds = 0

            idle_seconds = get_idle_time()
            print(f"[DEBUG] Current idle time: {idle_seconds:.2f} seconds")

            # If user is active right now, update last_activity_time
            if idle_seconds < IDLE_THRESHOLD:
                now_ts = now_ist()
                state["last_activity_time"] = format_time(now_ts)
                # first activity of day
                if state.get("first_activity_time") is None:
                    state["first_activity_time"] = format_time(now_ts)
                    print(f"[INFO] First activity detected: {state['first_activity_time']}")

            # Detect long idle -> treat as end-of-day and capture last_work_time
            if idle_seconds >= END_OF_DAY_THRESHOLD:
                # If we haven't recorded last_work_time yet for today, set it
                if state.get("last_work_time") is None:
                    # prefer last_activity_time if exists, else derive from idle_seconds
                    if state.get("last_activity_time"):
                        state["last_work_time"] = state["last_activity_time"]
                    else:
                        # fallback: now - idle_seconds
                        fallback = datetime.fromtimestamp(time.time() - idle_seconds, tz=IST)
                        state["last_work_time"] = format_time(fallback)
                    print(f"[INFO] Long idle detected. Marking last_work_time = {state['last_work_time']}")

            current_time = time.time()

            # Existing idle logging logic (unchanged behaviour, but we send new fields in payloads)
            if idle_seconds >= IDLE_THRESHOLD:
                if idle_start_time is None:
                    idle_start_time = current_time - idle_seconds
                    last_logged_seconds = IDLE_THRESHOLD
                    state["idle_time_today"] = state.get("idle_time_today", 0.0) + 3

                    from_dt = datetime.fromtimestamp(idle_start_time, tz=IST)
                    to_dt = now_ist()
                    send_idle_event_to_server(from_dt, to_dt, 3,
                                              first_activity_time=state.get("first_activity_time"),
                                              last_activity_time=state.get("last_activity_time"),
                                              last_work_time=state.get("last_work_time"))

                    print(f"[DEBUG] Idle session started and logged: {from_dt} to {to_dt}")
                else:
                    total_idle_duration = int(current_time - idle_start_time)
                    if total_idle_duration >= last_logged_seconds + IDLE_INCREMENT:
                        last_logged_seconds += IDLE_INCREMENT
                        state["idle_time_today"] = state.get("idle_time_today", 0.0) + 1

                        from_dt = datetime.fromtimestamp(current_time - CHECK_INTERVAL, tz=IST)
                        to_dt = datetime.fromtimestamp(current_time, tz=IST)
                        send_idle_event_to_server(from_dt, to_dt, 1,
                                                  first_activity_time=state.get("first_activity_time"),
                                                  last_activity_time=state.get("last_activity_time"),
                                                  last_work_time=state.get("last_work_time"))

                        print(f"[DEBUG] +1 minute idle logged: {from_dt} to {to_dt}")
            else:
                if idle_start_time is not None:
                    print("[DEBUG] User is active again. Resetting idle session tracking.")
                idle_start_time = None
                last_logged_seconds = 0

            # Persist state each loop (cheap) so restarts/crashes keep data
            save_state(state)

            print(f"[*] Sleeping for {CHECK_INTERVAL} seconds...\n")
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"[!] Main loop exception: {e}")
            traceback.print_exc()
            # Sleep a bit on unexpected exception to avoid tight loop
            time.sleep(5)


if __name__ == "__main__":
    main()

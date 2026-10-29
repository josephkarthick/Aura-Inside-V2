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
import getpass

# === CONFIGURATION (only change here) ===
IDLE_THRESHOLD_MINUTES = 3        # user considered idle after X minutes
CONTINUOUS_LOG_MINUTES = 3        # after threshold, log every X minutes

# === DERIVED CONFIG (auto-updates if you change above) ===
DJANGO_API_URL = "http://192.168.5.249:8000/api/log_event/"
IDLE_THRESHOLD = IDLE_THRESHOLD_MINUTES * 60              # seconds
IDLE_INCREMENT = CONTINUOUS_LOG_MINUTES * 60              # seconds
CHECK_INTERVAL = 10                                       # seconds (polling)
END_OF_DAY_THRESHOLD = IDLE_THRESHOLD * 4                 # fallback "long idle" -> end-of-day

# === TIMEZONE ===
IST = pytz.timezone("Asia/Kolkata")

SAFE_DIR = os.getenv("LOCALAPPDATA") or os.getenv("TEMP") or "."
STATE_FILE = os.path.join(SAFE_DIR, "agent_state.json")


def now_ist():
    return datetime.now(IST).replace(microsecond=0)


def parse_state_time(s):
    try:
        # assume naive IST string like "YYYY-MM-DD HH:MM:SS"
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return IST.localize(dt)
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
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    try:
        if not windll.user32.GetLastInputInfo(byref(lii)):
            return 0.0
        millis = windll.kernel32.GetTickCount() - lii.dwTime
        return max(0.0, millis / 1000.0)
    except Exception:
        return 0.0


def _get_username_via_wts():
    r"""
    Try to read DOMAIN\\Username of the active console session using WTS APIs.
    Returns None if unavailable.
    """
    try:
        WTS_CURRENT_SERVER_HANDLE = ctypes.c_void_p(0)
        WTSUserName = 5
        WTSDomainName = 7

        session_id = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()

        # WTSQuerySessionInformationW(
        #   hServer, SessionId, WTSInfoClass, ppBuffer(->LPWSTR), pBytesReturned
        # )
        WTSQuerySessionInformationW = ctypes.windll.Wtsapi32.WTSQuerySessionInformationW
        WTSQuerySessionInformationW.argtypes = [
            ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
            ctypes.POINTER(ctypes.c_wchar_p), ctypes.POINTER(wintypes.DWORD)
        ]
        WTSFreeMemory = ctypes.windll.Wtsapi32.WTSFreeMemory

        pUser = ctypes.c_wchar_p()
        pDomain = ctypes.c_wchar_p()
        bytes_ret = wintypes.DWORD(0)

        user_ok = WTSQuerySessionInformationW(
            WTS_CURRENT_SERVER_HANDLE, wintypes.DWORD(session_id), WTSUserName,
            ctypes.byref(pUser), ctypes.byref(bytes_ret)
        )
        domain_ok = WTSQuerySessionInformationW(
            WTS_CURRENT_SERVER_HANDLE, wintypes.DWORD(session_id), WTSDomainName,
            ctypes.byref(pDomain), ctypes.byref(bytes_ret)
        )

        if user_ok and domain_ok and pUser and pUser.value:
            username = pUser.value
            domain = pDomain.value or ""
            try:
                WTSFreeMemory(pUser)
                WTSFreeMemory(pDomain)
            except Exception:
                pass
            dom = domain.strip()
            if dom:
                return f"{dom}\\{username}"
            return username
    except Exception:
        pass
    return None


def get_logged_in_username():
    # 1) Preferred: WTS (works in services too)
    name = _get_username_via_wts()
    if name:
        return name
    # 2) Environment fallback
    user = os.environ.get("USERNAME") or getpass.getuser() or "Unknown"
    dom = os.environ.get("USERDOMAIN")
    return f"{dom}\\{user}" if dom else user


def send_idle_event_to_server(from_time, to_time, idle_minutes,
                              first_activity_time=None, last_activity_time=None, last_work_time=None):
    """
    Sends idle/activity payload to Django API.
    All time args should be timezone-aware datetimes or strings in "%Y-%m-%d %H:%M:%S" IST.
    """
    try:
        if isinstance(from_time, datetime):
            from_time_ist = from_time.astimezone(IST).replace(microsecond=0)
        else:
            from_time_ist = parse_state_time(from_time) or now_ist()

        if isinstance(to_time, datetime):
            to_time_ist = to_time.astimezone(IST).replace(microsecond=0)
        else:
            to_time_ist = parse_state_time(to_time) or now_ist()

        session_start_val = first_activity_time or format_time(from_time_ist)

        payload = {
            "session_start": session_start_val,
            "last_activity": last_activity_time,
            "last_work_time": last_work_time,
            "username": get_logged_in_username(),
            "hostname": socket.gethostname(),
            "from_time": from_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "to_time": to_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "idle_minutes": idle_minutes,
        }

        try:
            response = requests.post(DJANGO_API_URL, json=payload, timeout=5)
            print(f"[+] Sent payload: idle_minutes={idle_minutes} {from_time_ist} -> {to_time_ist} (status: {response.status_code})")
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


# === EXIT / SESSION-CLOSE HANDLING ===
_exit_hooks_registered = False
_state_for_exit = None

# Console control handler (captures logoff/shutdown/close without admin)
# https://learn.microsoft.com/windows/console/handlerroutine
CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2
CTRL_LOGOFF_EVENT = 5
CTRL_SHUTDOWN_EVENT = 6

_ctrl_handler_ref = None  # keep reference so it isn't GC'd

def _console_ctrl_handler(ctrl_type):
    # Map Windows console events to our on_exit
    try:
        print(f"[INFO] Console control event: {ctrl_type}")
        on_exit(signum=ctrl_type, frame=None)
        return True
    except Exception:
        traceback.print_exc()
        return False

def register_console_ctrl_handler():
    global _ctrl_handler_ref
    PHANDLER_ROUTINE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)
    _ctrl_handler_ref = PHANDLER_ROUTINE(_console_ctrl_handler)
    if not ctypes.windll.kernel32.SetConsoleCtrlHandler(_ctrl_handler_ref, True):
        print("[WARN] Failed to register console control handler")


def on_exit(signum=None, frame=None):
    global _state_for_exit
    try:
        if _state_for_exit is None:
            return
        state = _state_for_exit
        print(f"[INFO] Exiting agent (signal={signum}). Saving state and sending final heartbeat...")

        # Ensure last_work_time is set at least to last_activity if not already set
        if not state.get("last_work_time") and state.get("last_activity_time"):
            state["last_work_time"] = state["last_activity_time"]

        try:
            from_dt = parse_state_time(state.get("last_activity_time")) or now_ist()
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
    try: signal.signal(signal.SIGINT, on_exit)
    except Exception: pass
    try: signal.signal(signal.SIGTERM, on_exit)
    except Exception: pass
    try: signal.signal(signal.SIGBREAK, on_exit)
    except Exception: pass
    register_console_ctrl_handler()
    _exit_hooks_registered = True


# === MAIN LOOP ===
def main():
    print(f"[*] Idle tracking agent started. State file: {STATE_FILE}")
    print(f"[*] Idle threshold: {IDLE_THRESHOLD_MINUTES} minutes; continuous: {CONTINUOUS_LOG_MINUTES} minutes")
    state = load_state()
    register_exit_handlers(state)

    idle_start_time = None  # epoch seconds when idle began
    last_logged_seconds = 0 # seconds already accounted for in the current idle block

    while True:
        try:
            today_str = str(date.today())
            if state.get("idle_date") != today_str:
                state.update({
                    "idle_time_today": 0.0,
                    "idle_date": today_str,
                    "first_activity_time": None,
                    "last_activity_time": None,
                    "last_work_time": None
                })
                idle_start_time = None
                last_logged_seconds = 0

            idle_seconds = get_idle_time()
            print(f"[DEBUG] Current idle time: {idle_seconds:.2f} seconds")

            # track activity timestamps
            if idle_seconds < IDLE_THRESHOLD:
                now_ts = now_ist()
                state["last_activity_time"] = format_time(now_ts)
                if state.get("first_activity_time") is None:
                    state["first_activity_time"] = format_time(now_ts)
                    print(f"[INFO] First activity detected: {state['first_activity_time']}")

            # Fallback end-of-day if extremely long idle
            if idle_seconds >= END_OF_DAY_THRESHOLD and state.get("last_work_time") is None:
                if state.get("last_activity_time"):
                    state["last_work_time"] = state["last_activity_time"]
                else:
                    fallback = datetime.fromtimestamp(time.time() - idle_seconds, tz=IST)
                    state["last_work_time"] = format_time(fallback)
                print(f"[INFO] Long idle detected. Marking last_work_time = {state['last_work_time']}")

            current_time = time.time()

            # --- IDLE LOGGING LOGIC ---
            if idle_seconds >= IDLE_THRESHOLD:
                if idle_start_time is None:
                    # brand new idle block; set start based on last input
                    idle_start_time = current_time - idle_seconds
                    last_logged_seconds = IDLE_THRESHOLD  # accounted the first threshold minutes
                    state["idle_time_today"] += IDLE_THRESHOLD // 60

                    from_dt = datetime.fromtimestamp(idle_start_time, tz=IST)
                    to_dt = now_ist()
                    send_idle_event_to_server(from_dt, to_dt, IDLE_THRESHOLD // 60,
                                              first_activity_time=state.get("first_activity_time"),
                                              last_activity_time=state.get("last_activity_time"),
                                              last_work_time=state.get("last_work_time"))
                    print(f"[DEBUG] Idle session started and logged (first {IDLE_THRESHOLD // 60} min): {from_dt} to {to_dt}")
                else:
                    total_idle_duration = int(current_time - idle_start_time)
                    # After first threshold, add +CONTINUOUS_LOG_MINUTES every increment
                    if total_idle_duration >= last_logged_seconds + IDLE_INCREMENT:
                        chunk_start = current_time - IDLE_INCREMENT
                        chunk_end = current_time
                        last_logged_seconds += IDLE_INCREMENT
                        state["idle_time_today"] += CONTINUOUS_LOG_MINUTES

                        from_dt = datetime.fromtimestamp(chunk_start, tz=IST)
                        to_dt = datetime.fromtimestamp(chunk_end, tz=IST)
                        send_idle_event_to_server(from_dt, to_dt, CONTINUOUS_LOG_MINUTES,
                                                  first_activity_time=state.get("first_activity_time"),
                                                  last_activity_time=state.get("last_activity_time"),
                                                  last_work_time=state.get("last_work_time"))
                        print(f"[DEBUG] +{CONTINUOUS_LOG_MINUTES} minute(s) idle logged: {from_dt} to {to_dt}")
            else:
                if idle_start_time is not None:
                    print("[DEBUG] User is active again. Resetting idle session tracking.")
                idle_start_time = None
                last_logged_seconds = 0

            save_state(state)
            print(f"[*] Sleeping for {CHECK_INTERVAL} seconds...\n")
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"[!] Main loop exception: {e}")
            traceback.print_exc()
            time.sleep(5)


if __name__ == "__main__":
    main()

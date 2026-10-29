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

# === CONFIGURATION ===
DJANGO_API_URL = "http://192.168.5.249:8000/api/log_event/"
IDLE_THRESHOLD = 180  # seconds
IDLE_INCREMENT = 60   # seconds
CHECK_INTERVAL = 10   # seconds

# === TIMEZONE ===
IST = pytz.timezone("Asia/Kolkata")

SAFE_DIR = os.getenv("LOCALAPPDATA") or os.getenv("TEMP") or "."
STATE_FILE = os.path.join(SAFE_DIR, "agent_state.json")


def get_idle_time():
    class LASTINPUTINFO(Structure):
        _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = 8
    if not windll.user32.GetLastInputInfo(byref(lii)):
        return 0
    millis = windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0


def get_logged_in_username():
    try:
        session_id = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()
        WTSUserNameBuffer = ctypes.c_wchar_p()
        WTSDomainNameBuffer = ctypes.c_wchar_p()
        bytesReturned = wintypes.DWORD()

        ctypes.windll.Wtsapi32.WTSQuerySessionInformationW(None, session_id, 5, ctypes.byref(WTSUserNameBuffer), ctypes.byref(bytesReturned))
        ctypes.windll.Wtsapi32.WTSQuerySessionInformationW(None, session_id, 7, ctypes.byref(WTSDomainNameBuffer), ctypes.byref(bytesReturned))

        if WTSUserNameBuffer and WTSUserNameBuffer.value:
            username = WTSUserNameBuffer.value
            domain = WTSDomainNameBuffer.value
            ctypes.windll.Wtsapi32.WTSFreeMemory(WTSUserNameBuffer)
            ctypes.windll.Wtsapi32.WTSFreeMemory(WTSDomainNameBuffer)
            return f"{domain}\\{username}"
    except:
        pass
    return "Unknown"


def get_session_start_time():
    try:
        tick_count = windll.kernel32.GetTickCount64() // 1000  # seconds since boot
        boot_time = datetime.now(IST) - timedelta(seconds=tick_count)
        return boot_time.replace(microsecond=0)
    except:
        return datetime.now(IST).replace(microsecond=0)


def send_idle_event_to_server(from_time, to_time, idle_minutes):
    try:
        session_start_ist = get_session_start_time()
        from_time_ist = from_time.astimezone(IST).replace(microsecond=0)
        to_time_ist = to_time.astimezone(IST).replace(microsecond=0)

        payload = {
            "session_start": session_start_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "username": get_logged_in_username(),
            "hostname": socket.gethostname(),
            "from_time": from_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "to_time": to_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "idle_minutes": idle_minutes,
        }

        response = requests.post(DJANGO_API_URL, json=payload, timeout=5)
        print(f"[+] Sent idle event ({idle_minutes} min): {from_time_ist} -> {to_time_ist} (status: {response.status_code})")
    except Exception as e:
        print(f"[!] Failed to send idle event: {e}")


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return {
                "idle_time_today": data.get("idle_time_today", 0.0),
                "idle_date": data.get("idle_date", str(date.today()))
            }
    except:
        return {
            "idle_time_today": 0.0,
            "idle_date": str(date.today())
        }


def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except:
        pass


def main():
    print(f"[*] Idle tracking agent started. State file: {STATE_FILE}")
    state = load_state()

    idle_start_time = None
    last_logged_seconds = 0

    while True:
        today_str = str(date.today())
        if state["idle_date"] != today_str:
            state["idle_time_today"] = 0.0
            state["idle_date"] = today_str
            idle_start_time = None
            last_logged_seconds = 0

        idle_seconds = get_idle_time()
        print(f"[DEBUG] Current idle time: {idle_seconds:.2f} seconds")

        current_time = time.time()

        if idle_seconds >= IDLE_THRESHOLD:
            if idle_start_time is None:
                idle_start_time = current_time - idle_seconds
                last_logged_seconds = IDLE_THRESHOLD
                state["idle_time_today"] += 3

                from_dt = datetime.fromtimestamp(idle_start_time, tz=IST)
                to_dt = datetime.now(IST)
                send_idle_event_to_server(from_dt, to_dt, 3)

                print(f"[DEBUG] Idle session started and logged: {from_dt} to {to_dt}")
            else:
                total_idle_duration = int(current_time - idle_start_time)
                if total_idle_duration >= last_logged_seconds + IDLE_INCREMENT:
                    last_logged_seconds += IDLE_INCREMENT
                    state["idle_time_today"] += 1

                    from_dt = datetime.fromtimestamp(current_time - CHECK_INTERVAL, tz=IST)
                    to_dt = datetime.fromtimestamp(current_time, tz=IST)
                    send_idle_event_to_server(from_dt, to_dt, 1)

                    print(f"[DEBUG] +1 minute idle logged: {from_dt} to {to_dt}")
        else:
            if idle_start_time is not None:
                print("[DEBUG] User is active again. Resetting idle session tracking.")
            idle_start_time = None
            last_logged_seconds = 0

        save_state(state)
        print(f"[*] Sleeping for {CHECK_INTERVAL} seconds...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

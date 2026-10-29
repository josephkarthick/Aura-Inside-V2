import time
import psutil
import requests
import win32evtlog
import win32con
import socket
from ctypes import Structure, windll, c_uint, byref
import json
import os
from datetime import datetime, date
import pytz

DJANGO_API_URL = "http://192.168.5.27:8000/api/log_event/"
CHECK_INTERVAL = 60  # in seconds
MAX_EVENT_SCAN = 500
STATE_FILE = "agent_state.json"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return {
                "last_event_time": data.get("last_event_time"),
                "idle_time_today": data.get("idle_time_today", 0.0),
                "idle_date": data.get("idle_date", str(date.today()))
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "last_event_time": None,
            "idle_time_today": 0.0,
            "idle_date": str(date.today())
        }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_idle_time():
    try:
        class LASTINPUTINFO(Structure):
            _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]
        lii = LASTINPUTINFO()
        lii.cbSize = 8
        if not windll.user32.GetLastInputInfo(byref(lii)):
            raise Exception("GetLastInputInfo failed")
        millis = windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    except Exception as e:
        print(f"[!] Error in get_idle_time: {e}")
        return 0



def get_eventlog_events(event_ids, event_type_map):
    try:
        server = 'localhost'
        log_type = 'Security'
        flags = win32con.EVENTLOG_BACKWARDS_READ | win32con.EVENTLOG_SEQUENTIAL_READ
        h = win32evtlog.OpenEventLog(server, log_type)

        events = []
        scanned = 0

        while scanned < MAX_EVENT_SCAN:
            entries = win32evtlog.ReadEventLog(h, flags, 0)
            if not entries:
                break
            for entry in entries:
                scanned += 1
                if entry.EventID in event_ids:
                    event_time_str = entry.TimeGenerated.Format()
                    event_time = datetime.strptime(event_time_str, "%a %b %d %H:%M:%S %Y").replace(tzinfo=pytz.UTC)
                    if entry.EventID in [4800, 4801]:
                        details = "Locked" if entry.EventID == 4800 else "Unlocked"
                    elif entry.EventID in [4624, 4634]:
                        if entry.StringInserts and len(entry.StringInserts) >= 9:
                            username = entry.StringInserts[5]
                            domain = entry.StringInserts[6]
                            logon_type = entry.StringInserts[8]
                            if username.upper() in ["SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE"]:
                                continue
                            try:
                                lt = int(logon_type, 16) if logon_type.startswith("0x") else int(logon_type)
                                if lt not in [2, 10]:
                                    continue
                            except:
                                continue
                            details = f"{username} ({domain}), Logon Type: {lt}"
                        else:
                            continue
                    else:
                        details = "No details"

                    events.append({
                        "event_id": entry.EventID,
                        "event_type": event_type_map.get(entry.EventID, "unknown"),
                        "time": event_time,
                        "details": details
                    })
                if scanned >= MAX_EVENT_SCAN:
                    break

        win32evtlog.CloseEventLog(h)
        return events
    except Exception as e:
        print(f"[!] Error reading event log: {e}")
        return []

import win32ts
import win32con

import ctypes
from ctypes import wintypes

def get_logged_in_username():
    try:
        WTSGetActiveConsoleSessionId = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId
        session_id = WTSGetActiveConsoleSessionId()

        WTSUserName = ctypes.c_void_p()
        WTSDomainName = ctypes.c_void_p()
        WTSQuerySessionInformationW = ctypes.windll.Wtsapi32.WTSQuerySessionInformationW
        WTSFreeMemory = ctypes.windll.Wtsapi32.WTSFreeMemory

        WTSUserNameBuffer = ctypes.c_wchar_p()
        WTSDomainNameBuffer = ctypes.c_wchar_p()
        bytesReturned = wintypes.DWORD()

        WTSQuerySessionInformationW(None, session_id, 5, ctypes.byref(WTSUserNameBuffer), ctypes.byref(bytesReturned))
        WTSQuerySessionInformationW(None, session_id, 7, ctypes.byref(WTSDomainNameBuffer), ctypes.byref(bytesReturned))

        if WTSUserNameBuffer and WTSUserNameBuffer.value:
            username = WTSUserNameBuffer.value
            domain = WTSDomainNameBuffer.value
            WTSFreeMemory(WTSUserNameBuffer)
            WTSFreeMemory(WTSDomainNameBuffer)
            return f"{domain}\\{username}"

    except Exception as e:
        print(f"[!] Failed to get logged-in user from console session: {e}")
    return "Unknown"

def get_lock_unlock_events():
    return get_eventlog_events(
        event_ids=[4800, 4801],
        event_type_map={4800: "locked", 4801: "unlocked"}
    )

def get_login_logout_events():
    return get_eventlog_events(
        event_ids=[4624, 4634],
        event_type_map={4624: "login", 4634: "logout"}
    )

def send_to_server(event_type, details, timestamp=None):
    try:
        now = datetime.now(pytz.UTC)
        payload = {
            "event_type": event_type,
            "username": get_logged_in_username(),
            "hostname": socket.gethostname(),
            "timestamp": (timestamp or now.strftime("%Y-%m-%dT%H:%M:%S%z")),
            "details": details,
        }
        response = requests.post(DJANGO_API_URL, json=payload, timeout=5)
        print(f"[+] Sent {event_type}: {details} (status: {response.status_code})")
    except Exception as e:
        print(f"[!] Failed to send {event_type}: {e}")

def main():
    print("[*] Agent started. Monitoring...")
    state = load_state()

    while True:
        today_str = str(date.today())

        if state["idle_date"] != today_str:
            state["idle_time_today"] = 0.0
            state["idle_date"] = today_str

        idle_seconds = get_idle_time()
        print(f"[DEBUG] Idle time: {idle_seconds:.2f} seconds")

        if idle_seconds >= 10:
            state["idle_time_today"] += 1.0
            print(f"[DEBUG] +1.0 min idle added. Total today: {state['idle_time_today']} min")

            current_timestamp = datetime.now(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%S%z")
            send_to_server(
                "idle_time",
                f"{round(state['idle_time_today'], 2)} minutes idle",
                timestamp=current_timestamp
            )
        else:
            print("[DEBUG] User active or idle too short, not added")

        last_time_obj = None
        if state["last_event_time"]:
            try:
                last_time_obj = datetime.strptime(state["last_event_time"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
            except Exception as e:
                print(f"[!] Failed to parse last_event_time: {e}")

        lock_unlock_events = get_lock_unlock_events()
        login_logout_events = get_login_logout_events()
        all_events = sorted(lock_unlock_events + login_logout_events, key=lambda x: x["time"])

        for ev in all_events:
            if last_time_obj and ev["time"] <= last_time_obj:
                continue
            ts = ev["time"].strftime("%Y-%m-%dT%H:%M:%S%z")
            send_to_server(ev["event_type"], ev["details"], timestamp=ts)
            state["last_event_time"] = ev["time"].strftime("%Y-%m-%d %H:%M:%S")

        save_state(state)
        print(f"[*] Sleeping for {CHECK_INTERVAL} seconds...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] Agent crashed: {e}")


# storage.py
import time
import json
from typing import List, Dict, Optional
import os
from utils import TASKS_FILE, SESSIONS_FILE, ensure_data_files

ensure_data_files()

def _load_json(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_json(path: str, data: List[Dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Tasks
def get_all_tasks() -> List[Dict]:
    return _load_json(TASKS_FILE)

def add_task(name: str, category: str = "General") -> Dict:
    tasks = get_all_tasks()
    # simple case-insensitive uniqueness
    for t in tasks:
        if t["name"].strip().lower() == name.strip().lower():
            return t
    new = {
        "id": (tasks[-1]["id"] + 1) if tasks else 1,
        "name": name.strip(),
        "category": category or "General",
        "created_at": time.time()
    }
    tasks.append(new)
    _save_json(TASKS_FILE, tasks)
    return new

def find_task(name: str) -> Optional[Dict]:
    for t in get_all_tasks():
        if t["name"].strip().lower() == name.strip().lower():
            return t
    return None

# Sessions
def get_all_sessions() -> List[Dict]:
    return _load_json(SESSIONS_FILE)

def start_session(task_id: int, task_name: str) -> Dict:
    sessions = get_all_sessions()
    new = {
        "id": (sessions[-1]["id"] + 1) if sessions else 1,
        "task_id": task_id,
        "task_name": task_name,
        "start_ts": time.time(),
        "end_ts": None,
        "duration": None
    }
    sessions.append(new)
    _save_json(SESSIONS_FILE, sessions)
    return new

def stop_active_session() -> Optional[Dict]:
    sessions = get_all_sessions()
    for s in reversed(sessions):  # find most recent active session
        if s.get("end_ts") is None:
            end = time.time()
            s["end_ts"] = end
            s["duration"] = end - s["start_ts"]
            _save_json(SESSIONS_FILE, sessions)
            return s
    return None

def get_active_session() -> Optional[Dict]:
    sessions = get_all_sessions()
    for s in reversed(sessions):
        if s.get("end_ts") is None:
            return s
    return None

def update_sessions(sessions: List[Dict]):
    _save_json(SESSIONS_FILE, sessions)

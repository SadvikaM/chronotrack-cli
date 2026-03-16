# tracker.py
import time
from utils import print_header, format_duration, choose_quote, success, warning, info
from storage import add_task, find_task, start_session, stop_active_session, get_active_session, get_all_tasks, get_all_sessions, update_sessions

def add_task_cli():
    name = input("Enter task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return
    category = input("Enter category (optional): ").strip() or "General"
    task = add_task(name, category)
    print_header("Task Saved")
    print(f"ID: {task['id']}  Name: {task['name']}  Category: {task['category']}")

def start_task_cli():
    active = get_active_session()
    if active:
        print_header("Active Session Detected")
        print(f"A task is already running: {active['task_name']} (started at {time.ctime(active['start_ts'])})")
        print("Stop it first or let it run.")
        return

    name = input("Enter task name to start: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    task = find_task(name)
    if not task:
        task = add_task(name)

    session = start_session(task["id"], task["name"])
    print_header("Timer Started")
    print(f"Task: {session['task_name']}\nSession ID: {session['id']}\nStarted at: {time.ctime(session['start_ts'])}")

def stop_task_cli():
    active = get_active_session()
    if not active:
        print("No active session found.")
        return
    stopped = stop_active_session()
    if not stopped:
        print("Failed to stop session (unexpected).")
        return
    print_header("Timer Stopped")
    print(f"Task: {stopped['task_name']}\nDuration: {format_duration(stopped['duration'])}")
    print("\n" + choose_quote())

def show_status():
    active = get_active_session()
    if not active:
        print("No active task running.")
        return
    elapsed = time.time() - active["start_ts"]
    print_header("Active Task")
    print(f"Task: {active['task_name']}\nStarted at: {time.ctime(active['start_ts'])}\nElapsed: {format_duration(elapsed)}")

def list_tasks_cli():
    tasks = get_all_tasks()
    print_header("All Tasks")
    if not tasks:
        print("No tasks added yet.")
        return
    for t in tasks:
        print(f"[{t['id']}] {t['name']}  (Category: {t['category']})")

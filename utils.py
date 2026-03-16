# utils.py
import os
import json
import random
from datetime import timedelta
from colorama import Fore, Style, Back, init

# Initialize colorama (important for Windows)
init(autoreset=True)


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")

def ensure_data_files():
    """Ensure data directory and two JSON files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path in (TASKS_FILE, SESSIONS_FILE):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

def print_header(title_text):
    print("\n" + Fore.CYAN + "=" * 60)
    print(Fore.MAGENTA + title_text.center(60))
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)


def format_duration(seconds):
    """Convert seconds (int/float) to H:MM:SS string."""
    try:
        seconds = int(seconds)
    except Exception:
        seconds = 0
    return str(timedelta(seconds=seconds))
def success(text):
    return Fore.GREEN + Style.BRIGHT + text + Style.RESET_ALL

def warning(text):
    return Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL

def error(text):
    return Fore.RED + Style.BRIGHT + text + Style.RESET_ALL

def info(text):
    return Fore.CYAN + Style.BRIGHT + text + Style.RESET_ALL

def title(text):
    return Fore.MAGENTA + Style.BRIGHT + text + Style.RESET_ALL


def choose_quote():
    quotes = [
        "Focus on progress, not perfection.",
        "Track time to master it; measure to improve it.",
        "Small steps every day lead to big results.",
        "Discipline is the bridge between goals and accomplishment."
    ]
    return random.choice(quotes)

def naming_and_history_note():
    return (
        "ChronoTrack — A CLI Time Tracker\n"
        "--------------------------------\n"
        "- Name origin: 'Chrono' from Greek 'khronos' (time) + 'Track' (monitoring)\n"
        "- Working principle: create tasks, start/stop sessions; sessions are logged to JSON.\n"
    )

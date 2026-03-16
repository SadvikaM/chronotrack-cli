# timer.py
import time
import winsound
from utils import print_header

def countdown(seconds, label="Timer"):
    try:
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            print(f"{label}: {int(mins):02d}:{int(secs):02d}", end="\r", flush=True)
            time.sleep(1)
            seconds -= 1
        print(" " * 40, end="\r")
        # play beep at the end
        try:
            winsound.Beep(1000, 800)  # 1000Hz for 0.8s
        except Exception:
            print("\a", end="")  # fallback ASCII bell
    except KeyboardInterrupt:
        print("\nTimer interrupted by user.")
        return False
    return True


def pomodoro_timer():
    print_header("Pomodoro Focus Timer")
    try:
        focus_mins = int(input("Focus minutes (default 25): ").strip() or "25")
        break_mins = int(input("Break minutes (default 5): ").strip() or "5")
        rounds = int(input("Number of rounds (default 1): ").strip() or "1")
    except ValueError:
        print("Invalid input — using defaults (25/5, 1 round).")
        focus_mins, break_mins, rounds = 25, 5, 1

    for i in range(1, rounds + 1):
        print(f"\nRound {i} — Focus for {focus_mins} minutes.")
        ok = countdown(focus_mins * 60, "Focus")
        if not ok:
            break
        print("\nFocus session complete! Time for a break.")
        ok = countdown(break_mins * 60, "Break")
        if not ok:
            break
    print("\nPomodoro session(s) finished. Great job!")

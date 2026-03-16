# report.py
import time
from datetime import datetime, timedelta
from utils import print_header, format_duration
from storage import get_all_sessions, get_all_tasks
from tabulate import tabulate
import matplotlib.pyplot as plt
import os
import csv

def daily_report(date_str: str = None):
    """Show summary for a date (YYYY-MM-DD). If None, use today."""
    if date_str:
        try:
            dt = datetime.fromisoformat(date_str)
        except Exception:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
    else:
        dt = datetime.now()
    start = datetime(dt.year, dt.month, dt.day)
    end = start + timedelta(days=1)
    start_ts = start.timestamp()
    end_ts = end.timestamp()

    sessions = [s for s in get_all_sessions() if s.get("end_ts") and s["start_ts"] >= start_ts and s["start_ts"] < end_ts]
    if not sessions:
        print(f"No sessions on {start.strftime('%Y-%m-%d')}.")
        return

    summary = {}
    for s in sessions:
        summary[s["task_name"]] = summary.get(s["task_name"], 0) + s["duration"]

    table = [[task, format_duration(int(total))] for task, total in summary.items()]
    print_header(f"Daily Report — {start.strftime('%Y-%m-%d')}")
    print(tabulate(table, headers=["Task", "Time Spent"], tablefmt="grid"))

    # Plot
    labels = list(summary.keys())
    values = [summary[k] for k in labels]
    plt.figure(figsize=(8,4))
    plt.bar(labels, values)
    plt.ylabel("Seconds")
    plt.title(f"Time Spent per Task — {start.strftime('%Y-%m-%d')}")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()

def weekly_report():
    now = datetime.now()
    # include today and previous 6 days -> 7 days total
    start_day = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_ts = start_day.timestamp()
    sessions = [s for s in get_all_sessions() if s.get("end_ts") and s["start_ts"] >= start_ts]
    if not sessions:
        print("No sessions in the last 7 days.")
        return

    # aggregate per day
    daily = {}
    for s in sessions:
        day = datetime.fromtimestamp(s["start_ts"]).strftime("%Y-%m-%d")
        daily[day] = daily.get(day, 0) + s["duration"]

    # ensure all days present (fill zeros)
    days = [(start_day + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    values = [daily.get(d, 0) for d in days]

    table = [[d, format_duration(int(v))] for d, v in zip(days, values)]
    print_header(f"Weekly Report — {days[0]} to {days[-1]}")
    print(tabulate(table, headers=["Date", "Total Time"], tablefmt="grid"))

    # plot
    plt.figure(figsize=(9,4))
    plt.bar(days, values, color="teal")
    plt.ylabel("Seconds")
    plt.title("Last 7 Days - Time Spent")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()

def export_weekly_to_csv():
    print("DEBUG: CSV export started.")
    sessions = get_all_sessions()
    print(f"DEBUG: Loaded {len(sessions)} sessions.")

    if not sessions:
        print("⚠️  No session data found. Cannot export report.\n")
        return

    # Calculate start and end of the current week (last 7 days)
    end_day = datetime.now().date()
    start_day = end_day - timedelta(days=6)
    print(f"DEBUG: Start day = {start_day}, End day = {end_day}")

    # Compute daily totals
    daily = {}
    for s in sessions:
        print(f"DEBUG: Checking session {s}")  # 👈 new line
        if s.get("end_ts"):
            end_time = datetime.fromtimestamp(s["end_ts"]).date()
            if start_day <= end_time <= end_day:
                daily[end_time.isoformat()] = daily.get(end_time.isoformat(), 0) + s["duration"]

    print(f"DEBUG: Found {len(daily)} days with completed sessions.")

    if not daily:
        print("  No completed sessions found for this week.\n")
        return

    # Ensure reports folder exists
    os.makedirs("reports", exist_ok=True)
    print("DEBUG: 'reports' folder checked/created.")

    # Generate filename
    now = datetime.now()
    filename = f"weekly_report_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("reports", filename)

    # Write CSV file
    try:
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Total Time (seconds)"])
            for date, total in daily.items():
                writer.writerow([date, int(total)])

        print(f"\n Weekly report exported successfully to:\n   {os.path.abspath(filepath)}\n")

        import webbrowser
        webbrowser.open(os.path.abspath(filepath))

    except Exception as e:
        print(f"Error exporting CSV: {e}")

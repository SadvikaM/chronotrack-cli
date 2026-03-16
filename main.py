# main.py
from utils import ensure_data_files, print_header, naming_and_history_note, info, warning, success
from tracker import add_task_cli, start_task_cli, stop_task_cli, show_status, list_tasks_cli
from report import daily_report, weekly_report, export_weekly_to_csv
from timer import pomodoro_timer



def main_menu():
    ensure_data_files()
    while True:
        print_header("ChronoTrack — CLI Time Tracker")
        print(info("1.") + " Add New Task")
        print(info("2.") + " Start Task Timer")
        print(info("3.") + " Stop Task Timer")
        print(info("4.") + " View Active Status")
        print(info("5.") + " List All Tasks")
        print(info("6.") + " View Daily Report")
        print(info("7.") + " View Weekly Report")
        print(info("8.") + " Export Weekly Report to CSV")
        print(info("9.") + " Start Pomodoro Focus Session")
        print(info("10.") + " About ChronoTrack")
        print(info("11.") + " Exit")

        choice = input("\nEnter your choice (1–10): ").strip()
        if choice == "1":
            add_task_cli()
        elif choice == "2":
            start_task_cli()
        elif choice == "3":
            stop_task_cli()
        elif choice == "4":
            show_status()
        elif choice == "5":
            list_tasks_cli()
        elif choice == "6":
            # optional: ask date
            date_str = input("Enter date (YYYY-MM-DD) or leave empty for today: ").strip() or None
            daily_report(date_str)
        elif choice == "7":
            weekly_report()
        elif choice == "8":
            from report import export_weekly_to_csv
            print_header("Export Weekly Report to CSV")
            export_weekly_to_csv()
        elif choice == "9":
            pomodoro_timer()
        elif choice == "10":
            print(naming_and_history_note())
        elif choice == "11":
            print("Goodbye! Keep tracking your time.")
            break
        else:
            print("Invalid choice. Enter a number between 1 and 10.")

if __name__ == "__main__":
    main_menu()

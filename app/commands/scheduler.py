import time
import schedule
from app.commands.autoclose_overdue import update_expired_tasks


def run_scheduler():
    """
    Run the scheduler to auto-close expired tasks every day at midnight.
    """
    schedule.every().day.at("00:00").do(update_expired_tasks)
    print("Scheduler started... Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped manually.")


if __name__ == "__main__":
    run_scheduler()
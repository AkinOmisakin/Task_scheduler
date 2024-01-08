import schedule
import time
from Scripts.schedule_task import schedule_classes


if __name__ == "__main__":

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]

    for day in weekdays:
        schedule.every().day.at("00:00").do(schedule_classes)

    while True:
        schedule.run_pending()
        time.sleep(1)
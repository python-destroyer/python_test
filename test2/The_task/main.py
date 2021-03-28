import time
import schedule

from ping import ping_IPs
from post import post_file
from settings import config
from data_base import LOCAL_DIR

def main():
    schedule.every().day.at(config['csv_upload_time']).do(post_file, str(LOCAL_DIR) + "/event_list.csv", config['csv_server_address'])
    schedule.every(config['ping_period_minutes']).minutes.do(ping_IPs)
    while(1):
        schedule.run_pending()
        time.sleep(20)

if __name__ == "__main__":
    main()
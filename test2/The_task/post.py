import requests
import csv

from data_base import session, User, Event

def ItemsToRows(item):
    user_by_id = session.query(User).get(item.user_id)
    row = [item.id, user_by_id.username, user_by_id.ip_address, item.my_type, item.my_time]
    return row

def generate_csv_file(file_path):
    with open(file_path, 'w') as f:
        out = csv.writer(f)
        out.writerow(['event num', 'username', 'ip address', 'event type', 'event time'])
        rows = map(ItemsToRows, session.query(Event).all())
        out.writerows(rows)

def post_file(file_path, url):
    generate_csv_file(file_path)
    files = {'file': open(file_path, 'r').read()}
    requests.post(url, data=files)
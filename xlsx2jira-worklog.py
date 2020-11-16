import json
import logging
from datetime import timedelta

from AllocationParser import AllocationParser
from AllocationValidator import AllocationValidator
from JiraClient import JiraClient
import sys

if len(sys.argv) != 2:
    print('Usage: python3 xlsx2jira-worklog.py <path-to-xlsx-file-with-allocation>')
    sys.exit(1)

input_file_name = str(sys.argv[1])

with open('config.json', mode='rt', encoding='utf-8') as fd:
    config = json.load(fd)

parser = AllocationParser()
validator = AllocationValidator()
client = JiraClient(
    url=config['url'],
    username=config.get('username'),
    password=config.get('password'),
    cookie=config.get('cookie'),
    cert=config.get('cert'),
    logger=logging
)

logging_datetime_delta = timedelta(hours=config['logging_hour'])
all_rows = parser.parse_input_file(input_file_name)
rows_to_allocate = list(filter(lambda r: not r.in_jira, all_rows))
errors = validator.validate_allocation(rows_to_allocate)

if errors:
    for error in errors:
        print(error)
else:
    for row in rows_to_allocate:
        date_to_allocate = row.date + logging_datetime_delta
        print("Allocating task: {} on date: {} from row: {}"
              .format(row.task_id, date_to_allocate, row.row_num), flush=True, end='')
        client.allocate_work(row.task_id, date_to_allocate, row.hours, row.comment)
        print(" - OK")

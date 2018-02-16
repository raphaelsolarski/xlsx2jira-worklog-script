import json
import logging

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
    username=config['username'],
    password=config['password'],
    logger=logging)

all_rows = parser.parse_input_file(input_file_name)
rows_to_allocate = list(filter(lambda r: not r.in_jira, all_rows))
errors = validator.validate_allocation(rows_to_allocate)

if errors:
    for error in errors:
        print(error)
else:
    for row in rows_to_allocate:
        print("Allocating task: {} on date: {} from row: {}"
              .format(row.task_id, row.date, row.row_num), flush=True, end='')
        client.allocate_work(row.task_id, row.date, row.hours, row.comment)
        print(" - OK")

import openpyxl

from WorklogRecord import WorklogRecord


def parse_input_file(file_name):
    """parser asserts that first row is a header row"""
    rows = []
    wb = openpyxl.load_workbook(file_name)
    ws = wb.active
    for (index, row) in enumerate(ws.iter_rows(min_row=2, max_col=5)):
        date = row[0].value
        task_id = row[1].value
        hours = row[2].value or None
        in_jira = row[3].value != 'N'
        comment = row[4].value
        rows.append(WorklogRecord(index + 2, date, task_id, hours, in_jira, comment))
    return rows

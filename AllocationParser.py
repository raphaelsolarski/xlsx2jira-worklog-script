import openpyxl
from AllocationRecord import AllocationRecord


class AllocationParser:
    @staticmethod
    def parse_input_file(file_name):
        rows = []
        wb = openpyxl.load_workbook(file_name)
        ws = wb.active
        for (index, row) in enumerate(ws.iter_rows(min_row=1, max_col=5)):
            date = row[0].value
            task_id = row[1].value
            hours = row[2].value
            in_jira = row[3].value != 'N'
            project = row[4].value
            rows.append(AllocationRecord(index + 1, date, task_id, hours, in_jira, project))
        return rows

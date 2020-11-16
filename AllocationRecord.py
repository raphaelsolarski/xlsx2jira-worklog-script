class AllocationRecord:
    def __init__(self, row_num, date, task_id, hours, in_jira, comment):
        self.row_num = row_num
        self.date = date
        self.task_id = task_id
        self.hours = hours
        self.in_jira = in_jira
        self.comment = comment

    def __str__(self):
        return "{} {} {} {} {}".format(self.date, self.task_id, self.hours, self.in_jira, self.comment)



import datetime


class AllocationValidator:

    def validate_allocation(self, rows):
        errors = []
        for row in rows:
            errors.extend(self._validate(row))
        return errors

    def _validate(self, row):
        row_num = row.row_num
        row_errors = []
        if type(row.date) != datetime.datetime:
            row_errors.append("Wrong date format in row {}".format(row_num))
        if row.task_id is None:
            row_errors.append(self.field_lack_error_msg("task id", row_num))
        if row.hours is None:
            row_errors.append(self.field_lack_error_msg("hours", row_num))
        return row_errors

    @staticmethod
    def field_lack_error_msg(field_name, row_num):
        return "Lack of {} field in row {}".format(field_name, row_num)

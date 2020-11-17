import datetime


def validate(rows):
    errors = []
    for row in rows:
        errors.extend(_validate_row(row))
    return errors


def _validate_row(row):
    row_num = row.row_num
    row_errors = []
    if type(row.date) != datetime.datetime:
        row_errors.append(_wrong_filed_format("date", row_num))
    if row.task_id is None:
        row_errors.append(_field_lack_error_msg("task_id", row_num))
    if row.hours is None:
        row_errors.append(_field_lack_error_msg("hours", row_num))
    elif type(row.hours) != int and type(row.hours) != float:
        row_errors.append(_wrong_filed_format("hours", row_num))
    return row_errors


def _wrong_filed_format(field_name, row_num):
    return "Wrong {} format in row {}".format(field_name, row_num)


def _field_lack_error_msg(field_name, row_num):
    return "Lack of {} field in row {}".format(field_name, row_num)

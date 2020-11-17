import unittest
from datetime import datetime

import worklog_validator
from WorklogRecord import WorklogRecord


class TestValidator(unittest.TestCase):

    def test_valid_rows(self):
        errors = worklog_validator.validate([
            WorklogRecord(2, datetime(2020, 11, 17), 'task-1', 1, False, 'comment1'),
            WorklogRecord(3, datetime(2020, 11, 17), 'task-1', 1.5, False, None)
        ])
        self.assertEqual(errors, [])

    def test_invalid_rows(self):
        errors = worklog_validator.validate([
            WorklogRecord(2, 'invalid_date', 'task-1', None, False, 'comment1'),
            WorklogRecord(3, datetime(2020, 11, 17), None, 'invalid-hours', True, None)
        ])
        self.assertEqual(errors, [
            "Wrong date format in row 2",
            "Lack of hours field in row 2",
            "Lack of task_id field in row 3",
            "Wrong hours format in row 3"
        ])

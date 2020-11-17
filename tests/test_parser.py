import unittest
from datetime import datetime

import worklog_parser


class TestParser(unittest.TestCase):

    def test_parser(self):
        rows = worklog_parser.parse_input_file('tests/test-worklog.xlsx')
        self.assertEqual(len(rows), 3)

        self.assertEqual(rows[0].row_num, 2)
        self.assertEqual(rows[0].date, datetime(2017, 8, 1))
        self.assertEqual(rows[0].task_id, 'task-1550')
        self.assertEqual(rows[0].hours, 1)
        self.assertEqual(rows[0].in_jira, False)
        self.assertEqual(rows[0].comment, 'comment1')

        self.assertEqual(rows[1].row_num, 3)
        self.assertEqual(rows[1].date, datetime(2017, 8, 2))
        self.assertEqual(rows[1].task_id, 'task-1712')
        self.assertEqual(rows[1].hours, 1)
        self.assertEqual(rows[1].in_jira, True)
        self.assertEqual(rows[1].comment, 'comment2')

        self.assertEqual(rows[2].row_num, 4)
        self.assertEqual(rows[2].date, datetime(2017, 8, 3))
        self.assertEqual(rows[2].task_id, 'task-1665')
        self.assertEqual(rows[2].hours, 0.5)
        self.assertEqual(rows[2].in_jira, True)
        self.assertEqual(rows[2].comment, None)

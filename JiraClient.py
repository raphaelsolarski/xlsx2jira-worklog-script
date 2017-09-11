import requests
import pytz

from JiraClientException import JiraClientException


class JiraClient:
    def __init__(self, url, username, password, logger):
        self.logger = logger
        self.url = url
        self.username = username
        self.password = password

    def allocate_work(self, task_id, date, hours):
        def allocation_call(authorization_header):
            timezone = pytz.timezone("Europe/Warsaw")
            tz_aware = timezone.localize(date)
            dt = tz_aware.strftime('%G-%m-%dT%H:%M:%S.%f')[:-3]
            prepared_date = "%s%s" % (dt, tz_aware.strftime('%z'))
            body = {
                "started": prepared_date,
                "timeSpentSeconds": int(hours * 60 * 60)
            }
            response = requests.post(self.url + '/api/2/issue/{}/worklog'.format(task_id.upper()), json=body, headers=authorization_header)
            status_code = response.status_code
            if status_code != 201:
                msg = response
                self.logger.error('Error while logging work: {}'.format(msg))
                raise JiraClientException('Status code: {} \nresponse: \n{}'.format(status_code, msg))
        self._do_in_session(allocation_call)

    def find_worklog_for_issue(self, task_id):
        def call(authorization_header):
            body = {}
            response = requests.get(self.url + '/api/2/issue/{}/worklog'.format(task_id), json=body, headers=authorization_header)
            return response.json()
        return self._do_in_session(call)

    def _do_in_session(self, func):
        j_session = self._get_or_create_session()
        header_with_authorization_cookie = {"cookie": "JSESSIONID=" + j_session}
        return func(header_with_authorization_cookie)

    def _get_or_create_session(self):
        credentials = {"username": self.username, "password": self.password}
        session_response = requests.post(self.url + '/auth/1/session', json=credentials)
        if session_response.status_code == 200:
            session_info_json = session_response.json()
            j_session = session_info_json['session']['value']
            self.logger.debug('Recieved session (JSESSION={})'.format(j_session))
            return j_session
        else:
            msg = session_response.text
            status_code = session_response.status_code
            self.logger.error('Error while receiving session: {}'.format(msg))
            raise JiraClientException('Status code: {} \nresponse: \n{}'.format(status_code, msg))

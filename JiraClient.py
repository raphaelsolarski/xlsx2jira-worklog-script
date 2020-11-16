import pytz
import requests

from JiraClientException import JiraClientException


class JiraClient:
    def __init__(self, url, username, password, cookie, cert, logger):
        self.logger = logger
        self.url = url
        self.username = username
        self.password = password
        self.cert = cert
        if cookie:
            self.authorization_header_factory = lambda: {"cookie": cookie}
        elif username and password:
            self.authorization_header_factory = self._get_or_create_session_based_authorization_header
        else:
            raise Exception("Cookie or user/password must be specified")

    def allocate_work(self, task_id, date, hours, comment):
        def allocation_call(authorization_header):
            timezone = pytz.timezone("Europe/Warsaw")
            tz_aware = timezone.localize(date)
            dt = tz_aware.strftime('%G-%m-%dT%H:%M:%S.%f')[:-3]
            prepared_date = "%s%s" % (dt, tz_aware.strftime('%z'))
            body = {
                "started": prepared_date,
                "timeSpentSeconds": int(hours * 60 * 60),
                "comment": comment
            }
            response = requests.post('{}/api/2/issue/{}/worklog'.format(self.url, task_id.upper()), json=body,
                                     headers=authorization_header, cert=self.cert)
            status_code = response.status_code
            if status_code != 201:
                msg = response
                self.logger.error('Error while logging work: {}'.format(msg))
                raise JiraClientException('Status code: {} \nresponse: \n{}'.format(status_code, msg))

        self._with_authorization(allocation_call)

    def find_worklog_for_issue(self, task_id):
        def call(authorization_header):
            body = {}
            response = requests.get('{}/api/2/issue/{}/worklog'.format(self.url, task_id), json=body,
                                    headers=authorization_header, cert=self.cert)
            return response.json()

        return self._with_authorization(call)

    def _with_authorization(self, func):
        header_with_authorization_cookie = self.authorization_header_factory()
        return func(header_with_authorization_cookie)

    def _get_or_create_session_based_authorization_header(self):
        credentials = {"username": self.username, "password": self.password}
        session_response = requests.post('{}/auth/1/session'.format(self.url), json=credentials, cert=self.cert)
        if session_response.status_code == 200:
            session_info_json = session_response.json()
            j_session = session_info_json['session']['value']
            self.logger.debug('Recieved session (JSESSION={})'.format(j_session))
            return {"cookie": "JSESSIONID={}".format(j_session)}
        else:
            msg = session_response.text
            status_code = session_response.status_code
            self.logger.error('Error while receiving session: {}'.format(msg))
            raise JiraClientException('Status code: {} \nresponse: \n{}'.format(status_code, msg))

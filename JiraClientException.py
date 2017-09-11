from typing import Any


class JiraClientException(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

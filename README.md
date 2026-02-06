# xlsx2jira-worklog-script

## Install dependencies
```bash
pip3 install -r requirements.txt
```

## Prepare config.json file with connection configuration

### User / Password Auth
```json
{
  "url": "https://externalhttpuser:externalhttppassword@company.com/jira/rest",
  "username": "ldapUser",
  "password": "ladpPassword"
}
```

### API Token Auth
```json
{
  "url": "https://externalhttpuser:externalhttppassword@company.com/jira/rest",
  "api_token": "user-api-token"
}
```

### Cookie Auth
```json
{
  "url": "https://externalhttpuser:externalhttppassword@company.com/jira/rest",
  "cookie": "user-session-cookie"
}
```

## Run script: 
```bash
python3 xlsx2jira-worklog.py worklog.xlsx
```

## Tests
```bash
python -m unittest
```
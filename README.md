# xlsx2jira-worklog-script

#### Prepare config.json file with connection configuration

```json
{
  "url": "https://externalhttpuser:externalhttppassword@company.com/jira/rest",
  "username": "ldapUser",
  "password": "ladpPassword"
}
```

#### Run script: 

```
python3 xlsx2jira-worklog.py worklog.xlsx
```
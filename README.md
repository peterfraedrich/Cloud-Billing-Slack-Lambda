# billing-lambda

NOTE: secrets are in SSM at `/cloud/<cloud>/apikey`

This app pulls billing totals from all our cloud providers and creates a monthly report. Eventually i'd like to make this somewhat realtime and drop data into a database like ES to generate a Grafana dashboard off, but thats a little far off.


## ENV VARS
environment variables play a critical role in functionality. to enable a particular cloud you must supply that cloud's env var in format `USE_<cloud>`. The variable must not be empty, however the value does not matter.

```
CLOUD           VARIABLE        
-------------------------------------------------------
AWS             USE_AWS
Digital Ocean   USE_DO
Cloudflare      USE_CLOUDFLARE
Heroku          USE_HEROKU

```

Additionally, if you want to enable Slack reporting, you need to supply the `SLACK_REPORT=<not null>` variable.
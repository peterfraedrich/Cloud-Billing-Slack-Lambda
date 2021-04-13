import json
from get_secrets import Secrets
from aws import AWS
from heroku import Heroku
from cloudflare import Cloudflare
from do import DO
from datetime import date, time, timedelta
import os


def lambda_handler(event, context):
    secrets = Secrets()

    which_clouds = []
    for c in ['aws', 'heroku', 'do', 'cloudflare']:
        isEnabled = os.environ.get('USE_{}'.format(c.upper()), None)
        if isEnabled:
            which_clouds.append(c)

    end = last_day_of_month = date.today().replace(day=1) - timedelta(days=1)
    start = last_day_of_month.replace(day=1)

    results = []

    for cloud in which_clouds:
        res = {}
        if cloud == 'aws':
            # AWS
            aws_cloud = AWS()
            res = aws_cloud.get(start, end)

        if cloud == 'heroku':
            heroku_cloud = Heroku(secrets.get('heroku'))
            res = heroku_cloud.get(start, end)

        if cloud == 'do':
            do_cloud = DO(secrets.get('do'))
            res = do_cloud.get(start, end)

        if cloud == 'cloudflare':
            cf_cloud = Cloudflare(secrets.get('cloudflare'))
            res = cf_cloud.get(start, end)

        results.append(res)

    if os.environ.get('SLACK_REPORT', False):
        from report import REPORT
        r = REPORT(results, secrets.get('slack'), start, end, True)
        r.slack()
    return 200


if __name__ == '__main__':
    lambda_handler(None, None)

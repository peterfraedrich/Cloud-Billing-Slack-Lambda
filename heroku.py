import urllib3
import json
from datetime import timedelta, datetime
import decimal


class Heroku(object):
    token = None
    http = None

    def __init__(self, token):
        self.token = token
        self.http = urllib3.PoolManager()
        return

    def get(self, start, end):
        try:
            invoice_list = self.http.request('GET', 'https://api.heroku.com/account/invoices', headers={
                'Accept': 'application/vnd.heroku+json; version=3',
                'Authorization': 'Bearer {}'.format(self.token),
                'Content-Type': 'application/json'
            })
            list = json.loads(invoice_list.data.decode('utf-8'))
            end_plus1 = end + timedelta(days=1)
            matches = [x for x in list if x['period_start'] == start.strftime(
                '%Y-%m-%d') and x['period_end'] == end_plus1.strftime('%Y-%m-%d')]
            if len(matches) == 0:
                return None
            data = {
                'cloud': 'heroku',
                'period_start': start.strftime('%Y-%m-%d'),
                'period_end': end.strftime('%Y-%m-%d'),
                # for some reason Heroku reports their anmount in cents, so convert to dollars
                'amount': float(matches[0]['total'])/100,
                'timestamp': datetime.now().isoformat()
            }
            return data
        except Exception as e:
            print(e)
        return

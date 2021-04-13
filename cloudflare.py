import urllib3
import json
from datetime import datetime


class Cloudflare(object):
    token = None
    http = None

    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.http = urllib3.PoolManager()
        return

    def get(self, start, end):
        try:
            invoice_list = self.http.request(
                'GET', 'https://api.cloudflare.com/client/v4/user/billing/history?per_page=5', headers={
                    'Content-Type': 'application/json',
                    'X-Auth-Key': self.token,
                    'X-Auth-Email': self.email
                })
            bill_list = json.loads(invoice_list.data.decode('utf-8'))['result']
            for bill in bill_list:
                dtobj = datetime.strptime(
                    bill['occurred_at'], '%Y-%m-%dT%H:%M:%SZ').date()
                if dtobj >= start and dtobj <= end:
                    data = {
                        'cloud': 'cloudflare',
                        'period_start': start.strftime('%Y-%m-%d'),
                        'period_end': end.strftime('%Y-%m-%d'),
                        'amount': float(bill['amount'])*1.00,
                        'timestamp': datetime.now().isoformat()
                    }
                    return data
            return {'cloud': 'cloudflare'}
        except Exception as e:
            print(e)
        return

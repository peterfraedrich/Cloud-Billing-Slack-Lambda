import urllib3
import json
from datetime import datetime


class DO(object):
    token = None
    http = None

    def __init__(self, token):
        self.token = token
        self.http = urllib3.PoolManager()

    def get(self, start, end):
        try:
            invoice_list = self.http.request(
                'GET',
                'https://api.digitalocean.com/v2/customers/my/billing_history',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(self.token)
                })
            bill_list = json.loads(
                invoice_list.data.decode('utf-8'))['billing_history']
            invoices = [x for x in bill_list if x['type'] == 'Invoice']
            for i in invoices:
                dobj = datetime.strptime(
                    i['date'], '%Y-%m-%dT%H:%M:%SZ').date()
                if dobj >= start and dobj <= end:
                    data = {
                        'cloud': 'digital_ocean',
                        'period_start': start.strftime('%Y-%m-%d'),
                        'period_end': end.strftime('%Y-%m-%d'),
                        'amount': float(i['amount'])*1.00,
                        'timestamp': datetime.now().isoformat()
                    }
                    return data
        except Exception as e:
            print(e)
        return

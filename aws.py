import boto3
from datetime import datetime


class AWS(object):
    session = None

    def __init__(self):
        self.session = boto3.client('ce')
        return

    def get(self, start, end):
        try:
            res = self.session.get_cost_and_usage(
                TimePeriod={
                    'Start': start.strftime('%Y-%m-%d'),
                    'End': end.strftime('%Y-%m-%d'),
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            data = {
                'cloud': 'aws',
                'period_start': start.strftime('%Y-%m-%d'),
                'period_end': end.strftime('%Y-%m-%d'),
                'amount': float(res['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])*1.00,
                'timestamp': datetime.now().isoformat()
            }
            return data
        except Exception as e:
            print(e)
            return None

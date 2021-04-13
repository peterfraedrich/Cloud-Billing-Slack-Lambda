import json
import urllib3
from datetime import datetime
import re

emoji_map = {
    'custom': {
        'aws': ':bar_green:',
        'heroku': ':bar_purple:',
        'do': ':bar_ltblue:',
        'cloudflare': ':bar_orange:'
    },
    'stock': {
        'aws': ':koko:',
        'heroku': ':u7a7a:',
        'do': ':u6709:',
        'cloudflare': ':sa:'
    }
}


class REPORT(object):
    http = None
    data = None
    webhook = None
    total = 0.00
    pcts = {}
    custom = False
    start = None
    end = None

    def __init__(self, data, slack_webhook, start, end, custom_emoji=False):
        self.data = data
        self.webhook = slack_webhook
        self.custom = custom_emoji
        self.http = urllib3.PoolManager()
        self.start = start
        self.end = end
        return

    def slack(self):
        self._calculate()
        msg_str = self._format()
        self._send(msg_str)
        return

    def _calculate(self):
        self.total = sum([x['amount'] for x in self.data])
        for c in self.data:
            print(c)
            amt = float('{:0.2f}'.format(
                float(c['amount']) / self.total * 100))
            if amt < 1 and amt > 0:
                amt = 1.0
            self.pcts[c['cloud']] = round(amt)

    def _format(self):
        e = {}
        if self.custom:
            e = emoji_map['custom']
        else:
            e = emoji_map['stock']
        msg = slack_message
        msg['text'] = msg['text'].format(
            self.total, self.start.strftime('%B %Y'))
        msg['blocks'][0]['text']['text'] = msg['blocks'][0]['text']['text'].format(
            self.total, self.start.strftime('%B %Y'))
        msg['blocks'][1]['text']['text'] = msg['blocks'][1]['text']['text'].format(
            e['aws'], self.pcts['aws'], e['cloudflare'], self.pcts['cloudflare'], e['do'], self.pcts['digital_ocean'], e['heroku'], self.pcts['heroku'])
        aws_pct = ''.join([e['aws'] for x in range(self.pcts['aws'])])
        cf_pct = ''.join([e['cloudflare']
                          for x in range(self.pcts['cloudflare'])])
        do_pct = ''.join([e['do'] for x in range(self.pcts['digital_ocean'])])
        heroku_pct = ''.join([e['heroku'] for x in range(self.pcts['heroku'])])
        bar_chart = msg['blocks'][2]['text']['text'].format(
            *sorted([aws_pct, cf_pct, do_pct, heroku_pct], key=lambda i: len(i))
        )
        bar_list = re.findall('(:\w+:)', bar_chart)
        m = ''
        for idx, i in enumerate(bar_list, start=1):
            if idx % 15 != 0:
                m = m + i
            else:
                m = m + i + '\n'
        msg['blocks'][2]['text']['text'] = m
        raw = json.dumps(msg)
        return raw

    def _send(self, data):
        try:
            req = self.http.request(
                'POST',
                self.webhook,
                headers={
                    'Content-Type': 'application/json'
                },
                body=data)
            res = req.read()
        except Exception as e:
            print(e)
        return


slack_message = {
    'text': 'A new report is ready. We spent *${:,.2f}* on cloud services in {}.',
    'blocks': [
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'We spent *${:,.2f}* on cloud services in {}.'
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '*Services Breakdown*\n- {} AWS: {:.0f}%\n- {} Cloudflare: {:.0f}%\n- {} Digital Ocean: {:.0f}%\n- {} Heroku: {:.0f}%'
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '{}{}{}{}'
            }
        }
    ]


}

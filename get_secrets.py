import boto3


class Secrets(object):
    session = None

    def __init__(self):
        self.session = boto3.client('ssm')
        return

    def get(self, provider):
        try:
            res = self.session.get_parameter(
                Name='/cloud/{}/apikey'.format(provider),
                WithDecryption=True
            )
            if not res:
                return None
            return res['Parameter']['Value']
        except Exception as e:
            print(e)
        return

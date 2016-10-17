from datetime import datetime, timedelta
from violations import UseViolation
from BaseResource import BaseResource


class SQS(BaseResource):
    def __init__(self):
        super(BaseResource, self).__init__()
        self.session = None
        self.iam_client = None
        self.region = None
        # for import testing purposes
        print "hello"

    def set_session(self, session, region):
        self.session = session
        self.iam_client = session.client('iam')
        self.region = region

    def tag_janitor(self, rule):
        print "Tags not implemented for IAM users"

    def use_janitor(self, rule):
        violations = []
        users = []

        # Fetch all users
        response = self.iam_client.list_users(MaxItems=600)
        users += response['Users']
        if response['IsTruncated']:
            more = True
            while more:
                marker = response['Marker']
                response = self.iam_client.list_users(Marker=marker, MaxItems=600)
                if not response['IsTruncated']:
                    more = False
                users += response['Users']

        for user in users:
            if user['PasswordLastUsed'] < datetime.now() - timedelta(days=rule):
                violations.append(UseViolation(self.region, 'iam', user['UserName'], rule))
        return violations
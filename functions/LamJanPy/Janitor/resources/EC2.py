from datetime import datetime, timedelta
from violations import UseViolation, TagViolation
from BaseResource import BaseResource


class EC2(BaseResource):
    def __init__(self):
        super(BaseResource, self).__init__()
        self.session = None
        self.ec2_client = None
        self.violations = []
        self.region = None
        #for import testing purposes
        print "hello ec2"

    def set_session(self, session, region):
        self.session = session
        self.ec2_client = session.client('ec2')
        self.region = region

    def tag_janitor(self, rules):
        #TODO Error catching
        violations = []
        instances = self.ec2_client.describe_instances()['Reservations']['Instances']
        for instance in instances:
            tag_list = (tag_set['Key'] for tag_set in instance['Tags'])
            missing_tags = set(rules)-set(tag_list)
            if len(missing_tags) > 0:
                for tag in missing_tags:
                    violations.append(TagViolation(self.region, 'ec2', instance['InstanceId'], tag))
        return violations

    def use_janitor(self, rule):
        violations = []
        instances = self.ec2_client.describe_instances()['Reservations']['Instances']
        datetime.now() + timedelta(days=rule)
        for instance in instances:
            if instance['LaunchTime'] > datetime.now() + timedelta(days=rule):
                violations.append(UseViolation(self.region, 'ec2', instance['InstanceId'], rule))

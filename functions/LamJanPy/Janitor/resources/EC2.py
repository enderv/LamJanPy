from datetime import datetime, timedelta
from violations import UseViolation


class EC2:
    def __init__(self):
        self.session = None
        self.ec2_client = None
        self.violations = []
        #for import testing purposes
        print "hello ec2"

    def set_session(self, session):
        self.session = session
        self.ec2_client = session.client('ec2')

    def tag_janitor(self):
        print "Tags not yet implemented for EC2"

    def use_janitor(self, rule):
        print "Use Not implemented yet"

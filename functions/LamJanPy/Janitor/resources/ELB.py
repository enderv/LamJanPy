from violations import UseViolation
from BaseResource import BaseResource


class ELB(BaseResource):
    def __init__(self):
        super(BaseResource, self).__init__()
        self.session = None
        self.elb_client = None
        self.violations = []
        self.region = None
        #for import testing purposes
        print "hello elb"

    def tag_janitor(self):
        print "Tags not implemented for ELB"

    def set_session(self, session, region):
        self.session = session
        self.elb_client = session.client('elb')
        self.region = region

    def use_janitor(self, rule):
        violations = []
        elbs = self.elb_client.describe_load_balancers()
        for elb in elbs:
            if len(elb['Instances'] <= rule):
                violations.append(UseViolation(self.region, 'elb', elb['LoadBalancerName'], rule))

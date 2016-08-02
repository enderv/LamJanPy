from datetime import datetime, timedelta
from violations import UseViolation


class Lambda:
    def __init__(self):
        self.session = None
        self.lambda_client = None
        self.cloudwatch_client = None
        self.region = None
        #for import testing purposes
        print "hello"

    def set_session(self, session, region):
        self.session = session
        self.lambda_client = session.client('lambda')
        self.cloudwatch_client = session.client('cloudwatch')
        self.region = region

    def tag_janitor(self):
        print "Tags not yet implemented for Lamda"

    def use_janitor(self, rule):
        violations = []
        #TODO Error Catching
        function_names = (function['FunctionName'] for function in self.lambda_client.list_functions())
        for function_name in function_names:
            metrics = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Invocations',
                Dimensions=[
                    {
                        'Name': 'FunctionName',
                        'Value': function_name
                    },
                ],
                StartTime=datetime.now(),
                EndTime=datetime.now() - timedelta(days=rule),
                Period=43200,
                Statistics=['Maximum'],
                Unit='Count'
            )
            if len(metrics['Datapoints'] == 0):
                violations.append(UseViolation(self.region, 'lambda', function_name, rule))
            if not len(metric for metric in metrics['Datapoints'] if metric['Maximum'] > 0) > 0:
                violations.append(UseViolation(self.region, 'lambda', function_name, rule))
        return violations

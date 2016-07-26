from datetime import datetime, timedelta
from violations import TagViolation, UseViolation
class Lambda:
    def __init__(self, session):
        self.session = session
        self.lambda_client = session.client('lambda')
        self.cloudwatch_client = session.client('cloudwatch')
        self.function_names = (function['FunctionName'] for function in self.lambda_client.list_functions())
        self.violations = []
        #for import testing purposes
        print "hello"

    def tag_janitor(self):
        print "Tags not yet implemented for Lamda"

    def use_janitor(self, rule):
        for function_name in self.function_names:
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
                self.violations.append(UseViolation(self.region, 'lambda', function_name, rule))
            if not len(metric for metric in metrics['Datapoints'] if metric['Maximum'] > 0) > 0:
                self.violations.append(UseViolation(self.region, 'lambda', function_name, rule))
        return self.violations

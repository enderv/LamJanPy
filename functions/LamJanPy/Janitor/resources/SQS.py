from datetime import datetime, timedelta
from violations import UseViolation
from BaseResource import BaseResource


class SQS(BaseResource):
    def __init__(self):
        super(BaseResource, self).__init__()
        self.session = None
        self.cloudwatch_client = None
        self.region = None
        #for import testing purposes
        print "hello SQS"

    def set_session(self, session, region):
        self.session = session
        self.sqs_client = session.client('sqs')
        self.cloudwatch_client = session.client('cloudwatch')
        self.region = region

    def tag_janitor(self):
        print "Tags not yet implemented for SQS"

    def use_janitor(self, rule):
        violations = []
        #TODO Error Catching
        queue_names = (url[url.rfind('/')+1:] for url in self.sqs_client.list_queues()['QueueUrls'])
        for queue_name in queue_names:
            metrics = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/SQS',
                MetricName='NumberOfMessagesReceived',
                Dimensions=[
                    {
                        'Name': 'QueueName',
                        'Value': queue_name
                    },
                ],
                StartTime=datetime.now(),
                EndTime=datetime.now() - timedelta(days=rule),
                Period=43200,
                Statistics=['Maximum'],
                Unit='Count'
            )
            if len(metrics['Datapoints'] == 0):
                violations.append(UseViolation(self.region, 'sqs', queue_name, rule))
            if not len(metric for metric in metrics['Datapoints'] if metric['Maximum'] > 0) > 0:
                violations.append(UseViolation(self.region, 'sqs', queue_name, rule))
        return violations

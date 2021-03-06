import importlib
import boto3
import requests

valid_regions = ['us-east-1', 'us-west-2', 'us-west-1', 'eu-west-1', 'eu-central-1', 'ap-southeast-1',
                    'ap-northeast-1', 'ap-southeast-2', 'ap-northeast-2', 'ap-south-1', 'sa-east-1']


class Janitor():
    def __init__(self, config):
        self.resources_to_check = {}
        #make sure correct types and all there
        if not (isinstance(config['regions'], list)):
            raise TypeError("regions must be a list")
        if not (isinstance(config['resources_to_check'], list)):
            raise TypeError("resources_to_check must be a list")
        if not (isinstance(config['required_tags'], dict)):
            raise TypeError("required_tags must be a dict")
        if not (isinstance(config['use_rules'], dict)):
            raise TypeError("use_rules must be a dict")
        if len(set(config['regions']) - set(valid_regions)) > 0:
            raise ValueError(' ,'.join(set(config['regions'])-set(valid_regions)) + " are not valid regions")
        for key in config['resources_to_check']:
            try:
                #for testing later remove instance
                MyClass = getattr(importlib.import_module(".resources." + key, package="Janitor"), key)
                instance = MyClass()
                self.resources_to_check[key] = instance
            except ImportError:
                raise ValueError(key + " is not a valid resource to check")

        self.use_rules = config['use_rules']
        self.required_tags = config['required_tags']
        self.regions = config['regions']
        self.violations = []

        try:
            self.slack_url = config['slack_url']
        except AttributeError:
            print "No slack notifications will be sent"

        #Set all resource tag rules
        try:
            self.all_tags = self.required_tags['all']
        except AttributeError:
            self.all_tags = []

    def run_check(self):
        for region in self.regions:
            for name, resource in self.resources_to_check.items():
                session = boto3.Session(region_name=region)
                resource.set_session(session)
                try:
                    rule = self.required_tags[name] + self.all_tags
                    self.violations += resource.tag_janitor(rule)
                except AttributeError:
                    if len(self.all_tags) > 0:
                        print "No tag rule set for " + name + " using the all rule"
                        self.violations += resource.tag_janitor(self.all_tags)
                    else:
                        print "No tag rule set for " + name + " and no all rule set skipping tag check"
                try:
                    rule = self.use_rules[name]
                    self.violations += resource.use_janitor(rule)
                except AttributeError:
                    print "No use rule set for " + name + " skipping use check"

    def slack_report(self):
        message = '\n'.join(self.violations)
        text = "Violations Found"
        message = {"text": text, "attachments": {'color': '#fff000', 'text': message}}
        r = requests.post("http://httpbin.org/post", data=message)
        if r.status_code != 200:
            print "Error sending slack message"

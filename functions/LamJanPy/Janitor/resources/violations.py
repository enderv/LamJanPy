

class TagViolation:
    def __init__(self, region, resource_type, name, rule):
        self.region = region
        self.resource_type = resource_type
        self.name = name
        self.rule = rule


class UseViolation:
    def __init__(self, region, resource_type, name, rule):
        self.region = region
        self.resource_type = resource_type
        self.name = name
        self.rule = rule
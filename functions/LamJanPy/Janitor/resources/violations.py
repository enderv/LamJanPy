

class TagViolation:
    def __init__(self, region, resource_type, name, rule):
        self.region = region
        self.resource_type = resource_type
        self.name = name
        self.rule = rule

    def __str__(self):
        return "{0} in region {1} violated {2} tag rule {3}".format(self.name, self.region, self.resource_type,
                                                                    self.rule)


class UseViolation:
    def __init__(self, region, resource_type, name, rule):
        self.region = region
        self.resource_type = resource_type
        self.name = name
        self.rule = rule

    def __str__(self):
        return "{0} in region {1} violated {2} use rule {3}".format(self.name, self.region, self.resource_type,
                                                                    self.rule)

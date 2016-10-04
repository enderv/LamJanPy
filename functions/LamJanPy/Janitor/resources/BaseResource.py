class BaseResource(object):
    def set_session(self):
        raise NotImplementedError

    def tag_janitor(self):
        raise NotImplementedError

    def use_janitor(self):
        raise NotImplementedError

class Storage(object):

    def __init__(self):
        self.dict_ = dict()

    def matches_existing(self, string):
        return self.dict_.get(string)
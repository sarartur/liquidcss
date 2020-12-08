class Storage(object):

    def __init__(self):
        self.map_ = dict()

    def matches_existing(self, string):
        return self.map_.get(string)
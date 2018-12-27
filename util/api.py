class APIResponse(object):
    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):
        if self.data is not None and self.error is None:
            delattr(self, 'error')
        elif self.error is not None and self.data is None:
            delattr(self, 'data')
        elif self.data is None and self.error is None and self.code == 1000:
            delattr(self, 'data')
            delattr(self, 'error')
        return self.__dict__

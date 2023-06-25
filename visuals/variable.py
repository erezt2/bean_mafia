
class Variable:
    def __init__(self, info=None):
        if info is None:
            info = {}
        object.__setattr__(self, "info", info)

    def __getattr__(self, name):
        return self.info[name]

    def __setattr__(self, name, value):
        self.info[name] = value

    def __delattr__(self, name):
        del self.info[name]


class duper:
    """Super wrapper which allows property setting & deletion.
    Super can't be subclassed with empty __init__ arguments.
    Works with multiple inheritance.

    References:
      https://mail.python.org/pipermail/python-dev/2010-April/099672.html
      https://bugs.python.org/issue14965
      https://bugs.python.org/file37546/superprop.py

    Usage: duper(super())
    """

    def __init__(self, osuper):
        object.__setattr__(self, 'osuper', osuper)

    def _find(self, name):
        osuper = object.__getattribute__(self, 'osuper')
        if name != '__class__':
            mro = iter(osuper.__self_class__.__mro__)
            for cls in mro:
                if cls == osuper.__thisclass__:
                    break
            for cls in mro:
                if isinstance(cls, type):
                    try:
                        return object.__getattribute__(cls, name)
                    except AttributeError:
                        pass
        return None

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, 'osuper'), name)

    def __setattr__(self, name, value):
        osuper = object.__getattribute__(self, 'osuper')
        desc = object.__getattribute__(self, '_find')(name)
        if hasattr(desc, '__set__'):
            return desc.__set__(osuper.__self__, value)
        return setattr(osuper, name, value)

    def __delattr__(self, name):
        osuper = object.__getattribute__(self, 'osuper')
        desc = object.__getattribute__(self, '_find')(name)
        if hasattr(desc, '__delete__'):
            return desc.__delete__(osuper.__self__)
        return delattr(osuper, name)
class Base:
    class_dict = None
    class_list = None

    def __init__(self, screen, dict_key, class_name):
        self.screen = screen
        self.class_name = class_name

        self.key = dict_key
        if dict_key != "":
            self.__class__.class_dict[dict_key] = self
        self.__class__.class_list.append(self)

    def remove(self):
        self.__class__.class_list.remove(self)
        if self.key in self.__class__.class_dict:
            del self.__class__.class_dict[self.key]

    @classmethod
    def get_key(cls, key):
        return cls.class_dict.get(key)

    @classmethod
    def key_exists(cls, key):
        return key in cls.class_dict

    @classmethod
    def remove_by_key(cls, key):
        self = cls.class_dict[key]
        self.remove()

    @classmethod
    def get_by_class(cls, class_name):
        return [i for i in cls.class_list if i.class_name == class_name]

    @classmethod
    def remove_by_class(cls, class_name):
        for i in cls.get_by_class(class_name):
            i.remove()


from visuals.visual import Visual


class OrderedVisual(Visual):
    z_sorted_list = []

    def __init__(self, screen, rect, alignment, dict_key, class_name,
                 stick_to_camera, z_index):
        super().__init__(screen, rect, alignment, dict_key, class_name,
                         stick_to_camera)
        self._z = z_index
        self.insert_z_item(self)

    @classmethod
    def insert_z_item(cls, item):
        cls.z_sorted_list.insert(0, item)
        for i in range(len(cls.z_sorted_list) - 1):
            if cls.z_sorted_list[i].z > cls.z_sorted_list[i + 1].z:
                cls.z_sorted_list[i], cls.z_sorted_list[i + 1] = cls.z_sorted_list[i + 1], cls.z_sorted_list[i]
            else:
                break

    @classmethod
    def remove_z_item(cls, item):
        cls.z_sorted_list.remove(item)

    def remove(self):
        super().remove()
        self.remove_z_item(self)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        self.remove_z_item(self)
        self.insert_z_item(self)
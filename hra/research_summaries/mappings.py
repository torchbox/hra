class FieldMapping:
    def __init__(self, dest, source=None):
        self.dest = dest
        self.source = source or dest

    def get_field_data(self, data):
        if callable(self.source):
            return self.source(data)

        return data[self.source]

    def set_field(self, obj, data):
        value = self.get_field_data(data)

        setattr(obj, self.dest, value)


class ManyToManyMapping(FieldMapping):
    def __init__(self, *args, id_mapping=None, mappings=None, cls=None, **kwargs):
        self.id_mapping = id_mapping or FieldMapping('id')
        self.mappings = mappings or []
        self.cls = cls

        super().__init__(*args, **kwargs)

    def set_field(self, obj, data):
        value = self.get_field_data(data)

        related_manager = getattr(obj, self.dest)

        # Clear existing child objects in this field
        # Note: DeferringRelatedManger doesn't support the .set() method yet
        related_manager.clear()

        for child_data in value:

            cls_defaults = {}
            for field_mapping in self.mappings:
                cls_defaults.update(**{
                    field_mapping.dest: field_mapping.get_field_data(child_data)
                })

            obj, _ = self.cls.objects.get_or_create(
                **{
                    self.id_mapping.dest: self.id_mapping.get_field_data(child_data),
                    'defaults': cls_defaults,
                }
            )

            related_manager.add(obj)

from marshmallow import validate


def _get_base_field_kwargs():
    return {
        'validate': []
    }


class MetaParam(object):
    def __init__(self):
        self.field_kwargs = _get_base_field_kwargs()

    def apply(self, field_kwargs=None):
        if not field_kwargs:
            field_kwargs = _get_base_field_kwargs()
        for key, value in self.field_kwargs.items():
            if key == 'validate':
                if 'validate' not in field_kwargs:
                    field_kwargs['validate'] = []
                field_kwargs['validate'] += value
            else:
                field_kwargs[key] = value
        return field_kwargs


class LenghtParam(MetaParam):
    def __init__(self, field_me):
        super().__init__()
        # Add a length validator for max_length/min_length
        maxmin_args = {}
        if hasattr(field_me, 'max_length'):
            maxmin_args['max'] = field_me.max_length
        if hasattr(field_me, 'min_length'):
            maxmin_args['min'] = field_me.min_length
        self.field_kwargs['validate'].append(validate.Length(**maxmin_args))


class SizeParam(MetaParam):
    def __init__(self, field_me):
        super().__init__()
        # Add a length validator for max_length/min_length
        maxmin_args = {}
        if hasattr(field_me, 'max_value'):
            maxmin_args['max'] = field_me.max_value
        if hasattr(field_me, 'min_value'):
            maxmin_args['min'] = field_me.min_value
        self.field_kwargs['validate'].append(validate.Range(**maxmin_args))


class DescriptionParam(MetaParam):
    def __init__(self, field_me):
        super().__init__()
        description = getattr(field_me, 'help_text', None)
        if description:
            self.field_kwargs['description'] = description


class AllowNoneParam(MetaParam):
    def __init__(self, field_me):
        super().__init__()
        allow_none = getattr(field_me, 'null', None)
        if allow_none:
            self.field_kwargs['allow_none'] = True


class ChoiceParam(MetaParam):
    def __init__(self, field_me):
        super().__init__()
        choices = getattr(field_me, 'choices', None)
        if choices:
            self.field_kwargs['validate'].append(validate.OneOf(choices))
from django.core.exceptions import PermissionDenied


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super(FormControlMixin, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class ManagerMixin:

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        object = self.get_object()
        if not (user.groups.filter(name="Менеджеры").exists() or object.owner == user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema


class ClientTasksSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if path.endswith('/tasks') and method == 'POST':
            extra_fields = [
                coreapi.Field(
                    "task",
                    required=True,
                    location="form",
                    schema=coreschema.Integer()
                ),
                coreapi.Field(
                    "controller",
                    required=True,
                    location="form",
                    schema=coreschema.Integer()
                ),
            ]
            return extra_fields
        return super().get_manual_fields(path, method)

    def get_serializer_fields(self, path, method):
        if path.endswith('/tasks') and method == 'POST':
            return []
        return super().get_serializer_fields(path, method)


class TaskClientsSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if path.endswith('/clients') and method == 'POST':
            extra_fields = [
                coreapi.Field(
                    "to_perform",
                    required=False,
                    location="form",
                    schema=coreschema.Integer()
                ),
                coreapi.Field(
                    "to_remove",
                    required=False,
                    location="form",
                    schema=coreschema.Integer()
                ),
            ]
            return extra_fields
        return super().get_manual_fields(path, method)

    def get_serializer_fields(self, path, method):
        if path.endswith('/clients') and method == 'POST':
            return []
        return super().get_serializer_fields(path, method)

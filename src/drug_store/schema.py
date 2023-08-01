from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import build_basic_type
from drf_spectacular.types import OpenApiTypes


class Base64FileFieldSchema(OpenApiSerializerFieldExtension):
    target_class = "drf_base64.fields.Base64FileField"

    def map_serializer_field(self, auto_schema, direction):
        if direction == "request":
            return build_basic_type(OpenApiTypes.BYTE)
        elif direction == "response":
            return build_basic_type(OpenApiTypes.URI)


class Base64ImageFieldSchema(Base64FileFieldSchema):
    target_class = "drf_base64.fields.Base64ImageField"

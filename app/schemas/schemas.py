from app import ma
from marshmallow import fields

class UserBasicSchema(ma.Schema):
    name = fields.String()
    def get_name(self,obj):
        return f"hi {obj.name}"


#recordar el 'nested' si es necesario
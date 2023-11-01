from app import ma
from marshmallow import fields

class UserBasicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    def get_name(self,obj):
        return obj.name
    
class UserFullSchema(UserBasicSchema):
    image= fields.Integer()
    password = fields.String()
    email=fields.String()


#recordar el 'nested' si es necesario
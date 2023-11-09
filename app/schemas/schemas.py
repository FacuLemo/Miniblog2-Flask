from app import ma
from marshmallow import fields

#General view of schemas:
#User:
#   Basic & Full schema
#Comment:
#   Full  & Nested schema
#Post:
#   Full & Nested schema
#Category:
#   Full & Nested schema.




#Comment
class CommentFullSchema(ma.Schema):
    id= fields.Integer(dump_only=True)
    content = fields.String()
    post_id = fields.String()
    user_id = fields.String()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()

#Post
class PostFullSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    user_id = fields.Integer()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()

#Category
class CategoryFullSchema(ma.Schema):
    id= fields.Integer(dump_only=True)
    name = fields.String()

#Basic & FullNested schemas:
#User
class UserBasicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    
class UserFullNestedSchema(UserBasicSchema):
    image= fields.Integer()
    password = fields.String()
    email=fields.String()

#comment
class CommentNestedSchema(CommentFullSchema):
    post = fields.Nested(PostFullSchema,exclude=('id',))
    user_obj = fields.Nested(UserBasicSchema,exclude=('id',))

#Post
class PostNestedSchema(PostFullSchema):
    user_obj= fields.Nested(UserBasicSchema, exclude=('id',))
    comment = fields.Nested(CommentFullSchema,exclude=('id',))

#Category
class CategoryNestedSchema(CategoryFullSchema):
    posts = fields.Nested(PostFullSchema, exclude=('content',))


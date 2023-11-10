from app import ma
from marshmallow import fields

# General view of schemas:
# User:
#   Basic & FullNested schema
# Comment:
#   Full  & Nested schema
# Post:
#   Full & Nested schema
# Category:
#   Full & Nested schema.


# Comment
class CommentFullSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String()
    post_id = fields.String()
    user_id = fields.String()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()


# Post
class PostFullSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    user_id = fields.Integer()
    category_id = fields.Integer()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()


# Category
class CategoryFullSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


# User
class UserBasicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


# Nested & FullNested schemas:


class UserFullNestedSchema(UserBasicSchema):
    image = fields.Integer()
    password = fields.String()
    email = fields.String()
    posts = fields.Nested(PostFullSchema, many=True)
    comments = fields.Nested(CommentFullSchema, many=True)


# comment
class CommentNestedSchema(CommentFullSchema):
    post = fields.Nested(PostFullSchema, exclude=("id",))
    user = fields.Nested(UserBasicSchema, exclude=("id",))


# Post
class PostNestedSchema(PostFullSchema):
    user = fields.Nested(UserBasicSchema, exclude=("id",))
    category = fields.Nested(CategoryFullSchema, exclude=("id",))
    comments = fields.Nested(CommentFullSchema, many=True)


# Category
class CategoryNestedSchema(CategoryFullSchema):
    posts = fields.Nested(PostFullSchema, many=True)


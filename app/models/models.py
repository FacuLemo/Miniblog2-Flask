from app import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="category", cascade="all,delete")

    def __str__(self):
        return f"category: {self.name}"


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False) 
    image = db.Column(db.Integer, nullable=False, default=1)
    posts = db.relationship("Post", backref="user", cascade="all,delete")
    comments = db.relationship("Comment", backref="user",
                                cascade="all,delete")

    def __str__(self):
        return f"-User data: {self.nombre}, {self.email}."


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    content = db.Column(db.String(500), nullable=True)
    time_created = db.Column(DateTime(timezone=True),
                            server_default=func.now()
                            )
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, ForeignKey("user.id"),
                        nullable=False
                        )
    category_id = db.Column(db.Integer, ForeignKey("category.id"),
                            nullable=True
                            )
    comments = db.relationship("Comment", backref="post",
                               cascade="all,delete"
                               )

    def __str__(self):
        return f"-Category: f{self.name}"


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    time_created = db.Column(DateTime(timezone=True),
                            server_default=func.now()
                            )
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey("post.id"), nullable=False)

    def __str__(self):
        return f"-Comment '{self.content}' by {self.user_id}"
from datetime import timedelta
from app import app, db

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.views import MethodView
from app.models.models import (
    Category,
    Post,
    Comment,
    User,
)
from app.schemas.schemas import (
    UserBasicSchema,
    UserFullNestedSchema,
    CategoryFullSchema,
    CategoryNestedSchema,
    PostFullSchema,
    PostNestedSchema,
    CommentFullSchema,
    CommentNestedSchema,
)


# sección de la API, construida con MethodViews


# User API
class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is None:  # Si no hay parametro da vista general.
            users = User.query.all()
            resultado = UserBasicSchema().dump(users, many=True)
        else:  # Si se le manda el id del user muestra toda la info.
            users = User.query.get(user_id)
            resultado = UserFullNestedSchema().dump(users)
        return jsonify(resultado)

    def post(self):
        user_json = UserFullNestedSchema().load(request.json)
        name = user_json.get("name")
        email = user_json.get("email")
        password = user_json.get("password")
        image = user_json.get("image")
        try:
            if int(image) > 6:  # Esto debería ser una variable global...
                # Sólo se pueden elegir entre 6 fotos de perfil.
                return jsonify(
                    Error="imagen inexistente. No se registró el user."
                    )
            new_user = User(
                name=name, email=email,
                password=password, image=image
                )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(UserFullNestedSchema().dump(new_user))
        except ValueError as err:
            return jsonify(Error=err), 404

    def put(self, user_id):  # Cambiar contraseña y foto
        try:
            user_put = User.query.get(user_id)
            user_json = UserFullNestedSchema().load(request.json)
            passw = user_json.get("password")
            new_image = user_json.get("image")
            if int(new_image) > 6:  # Esto debería ser una variable global...
                # Sólo se pueden elegir entre 6 fotos de perfil.
                return jsonify(
                    Error="Cambiando a imagen inexistente. Cambios abortados."
                )
            user_put.password = passw
            user_put.image = new_image

            db.session.commit()
            return jsonify(UserBasicSchema().dump(user_put))
        except ValueError as err:
            return jsonify(Error=err), 404

    def delete(self, user_id):
        try:
            usr = User.query.get(user_id)
            db.session.delete(usr)
            db.session.commit()
            return jsonify(mensaje=f"Borraste el user {usr.name}")
        except ValueError as err:
            return jsonify(Error=err), 404


app.add_url_rule("/api/user", view_func=UserAPI.as_view("user"))
app.add_url_rule(
    "/api/user/<user_id>",
    view_func=UserAPI.as_view("user_by_id"))


# Categories API
class CategoriesAPI(MethodView):
    def get(self, category_id=None):
        if category_id is None:  # Si no hay parametro da vista general.
            categs = Category.query.all()
            resultado = CategoryFullSchema().dump(categs, many=True)
        else:
            # Si se le pasa el id, obtiene el Schema Nested.
            categ = Category.query.get(category_id)
            resultado = CategoryNestedSchema().dump(categ)
        return jsonify(resultado)

    def post(self):
        category_json = CategoryFullSchema().load(request.json)
        name = category_json.get("name")
        try:
            new_category = Category(name=name)
            db.session.add(new_category)
            db.session.commit()
            return jsonify(CategoryFullSchema().dump(new_category))
        except ValueError as err:
            return jsonify(Error=err), 404

    def put(self, category_id):  # Cambiar nombre de categoría
        try:
            categ_put = Category.query.get(category_id)
            categ_json = CategoryFullSchema().load(request.json)
            new_name = categ_json.get("name")
            categ_put.name = new_name
            db.session.commit()
            return jsonify(CategoryFullSchema().dump(categ_put))
        except ValueError as err:
            return jsonify(Error=err), 404

    def delete(self, category_id):
        try:
            categ = Category.query.get(category_id)
            db.session.delete(categ)
            db.session.commit()
            return jsonify(
                mensaje=f"Borraste la categoría '{categ.name}', y los posts asociados a éste."
            )
        except ValueError as err:
            return jsonify(Error=err), 404


app.add_url_rule(
    "/api/category",
    view_func=CategoriesAPI.as_view("category")
)
app.add_url_rule(
    "/api/category/<category_id>",
    view_func=CategoriesAPI.as_view("category_by_id")
)


# Post API
class PostAPI(MethodView):
    def get(self, post_id=None):
        if post_id is None:
            posts = Post.query.all()
            resultado = PostFullSchema().dump(posts, many=True)
        else:
            # Si se le pasa el id, obtiene el Schema Nested.
            posts = Post.query.get(post_id)
            resultado = PostNestedSchema().dump(posts)
        return jsonify(resultado)

    def post(self):
        # no confundir el método post con las variables, 'posts_json'
        posts_json = PostFullSchema().load(request.json)
        title = posts_json.get("title")
        content = posts_json.get("content")
        user = posts_json.get("user_id")
        categ = posts_json.get("category_id")
        time_created = posts_json.get("time_created") #datetime.now()
        try:
            new_post = Post(
                title=title, content=content,
                time_created=time_created, user=user,
                category_id=categ
            )
            db.session.add(new_post)
            db.session.commit()
            return jsonify(PostFullSchema().dump(new_post))
        except ValueError as err:
            return jsonify(Error=err), 404

    def put(self, post_id):  # Cambiar contenido y título
        try:
            # no confundir el método post con las variables, 'post_x'
            post_put = Post.query.get(post_id)
            post_json = PostFullSchema().load(request.json)
            title = post_json.get("title")
            content = post_json.get("content")
            post_put.title = title
            post_put.content = content
            db.session.commit()
            return jsonify(PostFullSchema().dump(post_put))
        except ValueError as err:
            return jsonify(Error=err), 404

    def delete(self, post_id):
        try:
            # no confundir la variable Post
            post = Post.query.get(post_id)
            db.session.delete(post)
            db.session.commit()
            return jsonify(
                mensaje=f"Borraste el post '{post.title}', junto a sus comentarios"
            )
        except ValueError as err:
            return jsonify(Error=err), 404


app.add_url_rule("/api/post", view_func=PostAPI.as_view("post"))
app.add_url_rule("/api/post/<post_id>",
                view_func=PostAPI.as_view("post_by_id"))


class CommentAPI(MethodView):
    def get(self, comment_id=None):
        if comment_id is None:  # Si no hay parametro da vista general.
            comments = Comment.query.all()
            resultado = CommentFullSchema().dump(comments, many=True)
        else:  # Si se le manda el id muestra toda la info nesteada.
            comments = Comment.query.get(comment_id)
            resultado = CommentNestedSchema().dump(comments)
        return jsonify(resultado)

    def post(self):
        comment_json = CommentFullSchema().load(request.json)
        content = comment_json.get("content")
        time_created = comment_json.get("time_created")
        user_id = comment_json.get("user_id")
        post_id = comment_json.get("post_id")
        try:
            new_comment = User(
                content=content,
                time_created=time_created,
                user_id=user_id,
                post_id=post_id,
            )
            db.session.add(new_comment)
            db.session.commit()
            return jsonify(CommentFullSchema().dump(new_comment))
        except ValueError as err:
            return jsonify(Error=err), 404

    def put(self, comment_id):  # Editar comment
        try:
            comment_put = CommentFullSchema().load(request.json)
            content = comment_put.get("content")
            time_updated = comment_put.get("time_updated")
            comment_put.content = content
            comment_put.time_updated = time_updated
            db.session.commit()
            return jsonify(UserBasicSchema().dump(comment_put))
        except ValueError as err:
            return jsonify(Error=err), 404

    def delete(self, comment_id):
        try:
            comment = Comment.query.get(comment_id)
            db.session.delete(comment)
            db.session.commit()
            return jsonify(mensaje=f"Borraste el comment: '{comment.content}'")
        except ValueError as err:
            return jsonify(Error=err), 404


app.add_url_rule("/api/comment", view_func=CommentAPI.as_view("comment"))
app.add_url_rule(
    "/api/comment/<comment_id>", view_func=CommentAPI.as_view("comment_by_id")
)


#Sección de enrutado con frontend, escencialmente lo mismo que en el miniblog1.


#Context Processor:
@app.context_processor
def inject_context():
    users = db.session.query(User).all()
    categ = db.session.query(Category).all()
    category1 = db.session.query(Category).first()
    if category1 == None:
        category_default = Category(name="Misceláneo")
        db.session.add(category_default)
        db.session.commit()
    return dict(users=users, categories=categ)

# Funciones de uso común:
def get_logged_user(uid):
    if uid == "guest":
        return "guest"
    else:
        return User.query.get(uid)


@app.route("/")
def RedirectGuest():
    return redirect(url_for("GuestIndexView"))

@app.route("/guest")
def GuestIndexView():
    return render_template(
        "index.html",
        posts=db.session.query(Post).order_by(Post.id.desc()).all(),
        logged_user='guest',
        comments=db.session.query(Comment).all(),
    )

@app.route("/logged")
def LoggedIndexView(user_id):
    logged_user= get_logged_user(user_id)
    render_template(
        "index.html",
        posts=db.session.query(Post).order_by(Post.id.desc()).all(),
        logged_user=logged_user,
        comments=db.session.query(Comment).all())


@app.route("/<user_id>")
def Index(user_id):
    logged_user = get_logged_user(user_id)
    return render_template(
        "index.html",
        posts=db.session.query(Post).order_by(Post.id.desc()).all(),
        logged_user=logged_user,
        comments=db.session.query(Comment).all(),
    )


@app.route("/filter/<ftype>/<tid>/<u_id>")
# fTYPE: filter type (user/categ).
# TID: (selected type) id.
# UID: logged user id.
def FilteredPosts(ftype, tid, u_id):
    logged_user = get_logged_user(u_id)
    if ftype == "user":
        posts = Post.query.filter_by(
            user_id=tid
            ).order_by(Post.id.desc()).all()
        ftext = f"posteos del usuario '{User.query.get(tid).name}'"
        return render_template(
            "filtered.html",
            ftext=ftext,
            fposts=posts,
            logged_user=logged_user,
            comments=db.session.query(Comment).all(),
        )

    if ftype == "category":
        posts = Post.query.filter_by(
            category_id=tid
            ).order_by(Post.id.desc()).all()
        ftext = f"posteos en la categoría '{Category.query.get(tid).name}'"
        return render_template(
            "filtered.html",
            ftext=ftext,
            fposts=posts,
            logged_user=logged_user,
            comments=db.session.query(Comment).all(),
        )


@app.route("/categories")
def ViewCategories():
    return render_template("categories.html")


@app.route("/users")
def ViewUsers():
    return render_template("users.html")


@app.route("/add_category", methods=["POST"])
def Addcategory():
    if request.method == "POST":
        name = request.form["name"]
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for("ViewCategories"))


@app.route("/add_user", methods=["POST"])
def AddUser():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        passw = request.form["password"]
        img = request.form["image"]
        #hashed_pass=generate_password_hash(passw, BORRAR
        #                                method='pbkdf2',
        #                                salt_length=8,
        #                                )

        new_user = User(name=name, email=email,
                        password=passw, image=img 
                        #CAMBIÉ el password=hashed_pass por 'passw'
                        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("ViewUsers"))


@app.route("/add_post/<uid>", methods=["POST"])
def AddPost(uid):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        new_post = Post(title=title, content=content,
                        category_id=category, user_id=uid)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("Index", user_id=uid))


@app.route("/add_comment/<post_id>/<uid>", methods=["POST"])
def AddComment(post_id, uid):
    if request.method == "POST":
        content = request.form["content"]
        post = post_id

        new_comment = Comment(content=content, 
                            user_id=uid,
                            post_id=post,
                            )
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("Index", user_id=uid))


@app.route("/edit_post/<id>/<uid>", methods=["POST"])
def editPost(id, uid):
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get(id)
    if title != "":
        post.title = title
    if content != "":
        post.content = content
    db.session.commit()

    return redirect(url_for("Index", user_id=uid))


@app.route("/edit_comment/<id>/<uid>", methods=["POST"])
def editComment(id, uid):
    content = request.form["content"]
    comment = Comment.query.get(id)
    if content != "":
        comment.content = content
    db.session.commit()

    return redirect(url_for("Index", user_id=uid))


@app.route("/delete_post/<id>/<uid>")
def deletePost(id, uid):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("Index", user_id=uid))


@app.route("/delete_comment/<id>/<uid>")
def deleteComment(id, uid):
    comm = Comment.query.get(id)
    db.session.delete(comm)
    db.session.commit()

    return redirect(url_for("Index", user_id=uid))


@app.route("/delete_user/<id>")
def deleteUser(id):
    usr = User.query.get(id)
    db.session.delete(usr)
    db.session.commit()
    return redirect(url_for("ViewUsers"))


@app.route("/delete_category/<id>")
def deleteCategory(id):
    cat = Category.query.get(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for("ViewCategories"))

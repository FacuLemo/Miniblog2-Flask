from datetime import timedelta
from app import app, db, jwt

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from app.models.models import (
    Category,
    Post,
    Comment,
    User,
)
from app.schemas.schemas import (
    UserBasicSchema,
)



def get_logged_user(uid):
    if uid == "guest":
        return "guest"
    else:
        return User.query.get(uid)


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
@jwt_required()
def LoggedIndexView(key):
    uid= get_jwt_identity() # trae lo que le diste como parametro en el token
    current_user=User.query.get(uid)
    render_template(
        "index.html",
        posts=db.session.query(Post).order_by(Post.id.desc()).all(),
        logged_user=current_user,
        comments=db.session.query(Comment).all())


#Al borrar la siguiente ruta recordar hacer
#ctrl f y volver a referenciar los index.

@app.route("/<user_id>")
def Index(user_id):
    logged_user = get_logged_user(user_id)
    return render_template(
        "index.html",
        posts=db.session.query(Post).order_by(Post.id.desc()).all(),
        logged_user=logged_user,
        comments=db.session.query(Comment).all(),
    )

#PARA EL FILTER:
#crear ruta: 'filter/ftype/tid/guest
#y otra ruta: 'filter/ftype/tid/logged'
#la última estando JWT_required.

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

@app.route("/login/<uid>", methods=["POST"])
def Login(uid):
    if request.method == "POST":
        user=User.query.get(uid)
        passw = request.form["passw"]
        if user and check_password_hash(user.password, passw):
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(minutes=30)
                #additional_claims={'user_type':1} -> no es necesario
            )
            return redirect(url_for("LoggedIndexView")), access_token
        return redirect(url_for("GuestIndexView")) #o 401

#login que pida los datos y des-hashee la pass para ver si coincide con el input
# if user and check_password_hash(user.password, password) -> Devuelve true o false
#   access_token = create_access_token(
#                                       identity=username
#                                       expires_delta=timedelta(minutes=30)   #datetime.now()+tmdelta                                 
#                                       additional_claims={
#                                                   'user_id':uid
#                                        }                                      
#                                      )
#   return access_token
#return "no se genero token"

    #get_info=get_jwt() -> trae el dict q pones en el token de acceso
    #if get_info ['user_type']==1:
    #    return algo admin
#en el access token hay datos como el nombre de usuario, fecha, etc.


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
        hashed_pass=generate_password_hash(passw,
                                        method='pbkdf2',
                                        salt_length=8,
                                        )
        new_user = User(name=name, email=email,
                        password=hashed_pass, image=img
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

@jwt.invalid_token_loader
def Unauth(reason):
    return f'denegado por {reason}'
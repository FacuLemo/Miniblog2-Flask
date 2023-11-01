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
    UserFullSchema,
)
#Funciones de uso común:
def get_logged_user(uid):
    if uid == "guest":
        return "guest"
    else:
        return User.query.get(uid)

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

#sección de la API, construida con MethodViews
class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is None: #Si no hay parametro da vista general.
            users= User.query.all()
            resultado = UserBasicSchema().dump(users,many=True)
        else:   #Si se le manda el id del user muestra toda la info.
            users= User.query.get(user_id)
            resultado= UserFullSchema().dump(users)
        return jsonify(resultado)
        
    def post(self):
        user_json = UserFullSchema().load(request.json)
        name= user_json.get('name')
        email= user_json.get('email')
        password= user_json.get('password')
        image= user_json.get('image')
        try:
            if int(image) > 6: #Esto debería ser una variable global...
                return jsonify(Error="imagen inexistente. No se registró el user.")
            new_user = User(name=name, email=email,
                            password=password, image=image
                            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(UserFullSchema().dump(new_user))
        except ValueError as err:
           return jsonify(Error=err), 404

    def put(self,user_id): #Cambiar contraseña y foto
        try:
            user_put= User.query.get(user_id)
            user_json = UserFullSchema().load(request.json)
            passw= user_json.get('password')
            new_image= user_json.get('image')
            if int(new_image) > 6: #Esto debería ser una variable global...
                return jsonify(Error="Cargando imagen inexistente")
            user_put.password= passw
            user_put.image=new_image
            
            db.session.commit()
            return jsonify(UserBasicSchema().dump(user_put))
        except ValueError as err:
           return jsonify(Error=err), 404
    
    def delete(self,user_id):
        try:
            usr = User.query.get(user_id)
            db.session.delete(usr)
            db.session.commit()
            return jsonify(mensaje=f"Borraste el user {id}")
        except ValueError as err:
           return jsonify(Error=err), 404
        

app.add_url_rule("/api/user",view_func=UserAPI.as_view('user'))
app.add_url_rule("/api/user/<user_id>", view_func=UserAPI.as_view('user_by_id'))

#/api
#   def delete(self,Xid)
#       try:
#            blabla
#       except ValueError as err:
#           return jsonify(Error=err), 404


#Sección de enrutado con frontend, escencialmente lo mismo que en el miniblog1.
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
#@jwt_required()
def LoggedIndexView(user_id):
    #uid= get_jwt_identity() # trae lo que le diste como parametro en el token
    #current_user=User.query.get(uid)
    logged_user= get_logged_user(user_id)
    render_template(
        "index.html",
        posts=db.session.query(Post).order_by(Post.id.desc()).all(),
        logged_user=logged_user,
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
        return redirect(url_for("LoggedIndexView"))
        """user=User.query.get(uid)
        passw = request.form["passw"]
        if user and check_password_hash(user.password, passw):
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(minutes=30)
                #additional_claims={'user_type':1} -> no es necesario
            )
            return redirect(url_for("LoggedIndexView")), access_token
        return redirect(url_for("GuestIndexView")) #o 401"""

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

#@jwt.invalid_token_loader
#def Unauth(reason):
#    return f'denegado por {reason}'
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import session
from flask import Response
from flask import flash
from flask import make_response
from apscheduler.schedulers.background import BackgroundScheduler
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError

from declaration import Declaration
from database import Database
from user import User
from schemas import user_insert_schema
from schemas import user_update_schema

from functools import wraps
import datetime
import data_importer
import json
import atexit
import hashlib
import uuid

app = Flask(__name__, static_url_path='/static', static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
schema = JsonSchema(app)

# Background Scheduler pour l'exigence A3.
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(data_importer.data_import, 'cron', hour=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


# Fonction qui permet de valider si l'authentification
# est nécessaire. Doit se trouver en haut du fichier
# pour pouvoir être exécutée par toutes les autres
# fonctions.
def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


# Fonction principale de l'application.
# Affiche la page d'accueil de l'application.
@app.route('/')
def index():
    quartiers = get_database().get_all_quartiers()
    if "id" in session:
        fullname = get_database().get_session(session["id"])
        return render_template("index.html", title="Accueil",
                               fullname=fullname,
                               quartiers=quartiers)
    return render_template("index.html", title="Accueil",
                           quartiers=quartiers)


# Fonction permettant aux utilisateurs de se connecter
# à l'application.
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", title="Se connecter")
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "" or password == "":
            return render_template("login.html", title="Se connecter",
                                   error="Veuillez entrer une adresse "
                                   "courriel et un mot de passe valide.")

        user = get_database().get_user_info(email)
        if user is None:
            return render_template("login.html", title="Se connecter",
                                   error="Veuillez entrer une adresse "
                                   "courriel et un mot de passe valide.")

        salt = user[0]
        hashed_password = hashlib.sha512(
            str(password+salt).encode("utf-8")).hexdigest()
        if(hashed_password == user[1]):
            id_session = uuid.uuid4().hex
            get_database().save_session(id_session, email)
            session["id"] = id_session
            return redirect("/")
        else:
            return render_template("login.html", title="Se connecter",
                                   error="Veuillez entrer une adresse "
                                   "courriel et un mot de passe valide.")


# Fonction permettant de modifier les quartiers favoris d'un utilisateur
# et d'ajouter/modifier une photo de profil.
@app.route("/edit_user", methods=["GET", "POST"])
@authentication_required
def edit_user():
    email = get_database().get_session(session["id"])
    user = get_database().get_all_user_infos(email)
    if request.method == "GET":
        quartiers = get_database().get_all_quartiers()
        return render_template("edit_user.html",
                               title="Modifier l'utilisateur",
                               fullname=email, quartiers=quartiers,
                               selected_quartiers=user[3], photo_id=user[4])
    else:
        liste_quartiers = request.form.getlist('liste_quartiers')
        photo = None
        picture_id = None

        if "photo" in request.files and request.files['photo'].filename != "":
            photo = request.files['photo']
            picture_id = str(uuid.uuid4().hex)
        if picture_id is not None:
            get_database().create_picture(picture_id, photo)
            updated_user = User(0, None, email, liste_quartiers,
                                None, None, picture_id)
        else:
            updated_user = User(0, None, email, liste_quartiers,
                                None, None, user[4])
        get_database().save_user(updated_user)

        flash("Les données ont été enregistrées avec succés!")
        return redirect("/edit_user")


# Fonction qui permet de retourner une image stockée dans la
# base de données.
@app.route('/image/<picture_id>.png')
def dowload_picture(picture_id):
    binary_data = get_database().load_picture(picture_id)
    if binary_data is None:
        return Response(status=404)
    else:
        response = make_response(binary_data)
        response.headers.set('Content-Type', 'image/png')
    return response


# Fonction qui permet à un utilisateur de se déconnecter.
@app.route("/logout")
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_database().delete_session(id_session)
    return redirect("/")


# Fonction qui permet de détecter si un utilisateur est
# présentement connecté.
def is_authenticated(session):
    return "id" in session


# Fonction qui permet à un utilisateur de se créer un compte.
@app.route("/register", methods=["GET", "POST"])
def register():
    quartiers = get_database().get_all_quartiers()
    if request.method == "GET":
        return render_template("register.html", title="S'enregistrer",
                               quartiers=quartiers)
    else:
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        liste_quartiers = request.form.getlist('liste_quartiers')

        # Vérifier si l'adresse email existe déjà
        existing = get_database().check_email_validity(email)

        if(existing is not None):
            return render_template("register.html",
                                   error="Cette adresse courriel est déjà "
                                   "utilisée. "
                                   "Veuillez utiliser une adresse différente.",
                                   quartiers=quartiers)

        if fullname == "" or email == "" or password == "":
            return render_template("register.html",
                                   error="Tous les champs marqués d'une "
                                   "astérisque sont obligatoires")

        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(
            str(password+salt).encode("utf-8")).hexdigest()
        user = User(None, fullname, email, liste_quartiers,
                    salt, hashed_password, None)
        get_database().save_user(user)
        return redirect('/')


# Trouver les déclarations selon la recherche.
@app.route('/find_declarations', methods=['POST'])
def find_declarations():
    search = request.form.get('search_declarations')
    results = get_database().find_declarations(search)
    if "id" in session:
        fullname = get_database().get_session(session["id"])
        return render_template("find_declarations.html",
                               title="Liste des résultats",
                               fullname=fullname, results=results)
    return render_template("find_declarations.html",
                           title="Liste des résultats", results=results)


# Service REST qui retourne la liste des déclarations entre deux dates.
@app.route('/declarations', methods=['GET'])
def get_declarations_between_dates():
    format = "%Y-%m-%d"
    du = request.args.get('du')
    au = request.args.get('au')

    try:
        datetime.datetime.strptime(du, format)
        datetime.datetime.strptime(au, format)
    except ValueError:
        return make_response(jsonify("Les dates doivent être dans"
                                     " le format AAAA-MM-JJ."
                                     "Assurez-vous également que les "
                                     "dates entrées sont valides.", 404))

    declarations = get_database().get_declarations_between_dates(du, au)
    return jsonify([declaration.asDictionary()
                    for declaration in declarations])


# Service REST qui retourne tous les quartiers avec
# le nombre de déclarations répertoriées.
@app.route('/api/quartiers', methods=['GET'])
def get_declarations_by_quartier():
    quartiers = get_database().get_declarations_by_quartier()
    return jsonify(quartiers)


# Service REST qui permet d'ajouter un utilisateur dans la BDD.
@app.route('/api/user', methods=['POST'])
@schema.validate(user_insert_schema)
def create_user():
    data = request.get_json()
    user = User(None, data["fullname"], data["email"],
                data["liste_quartiers"], data["password"], None)
    user = get_database().save_user(user)
    return jsonify(user.asDictionnary()), 201


# Route qui retourne la documentation RAML.
@app.route('/doc', methods=['GET'])
def get_raml_doc():
    return render_template("doc.html")


# Fonctions pour la base de donnees.
def get_database():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# Fonction qui retourne un message d'erreur si l'utilisateur
# essaie d'accéder à une fonction qui nécéssite d'être connecté.
def send_unauthorized():
    return Response("Nous n'avons pas vu valider votre niveau"
                    "d'accès pour cette URL.\n"
                    "Vous devez vous connecter avec les identifiants"
                    "nécessaires.", 401,
                    {'WWW-Authenticate': 'Basic realm = "Login Required"'})


# Clé secrète de l'application. Doit être présente pour les sessions.
# Cette clé a été généré par la fonction random() de python.
app.secret_key = "b'\xcb\xbd0C\xc2\xc0\x12|Xnmav\xe6\xd5W\x92_hg`\xce\x14"

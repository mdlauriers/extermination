# Mathieu Des Lauriers
# Classe pour la gestions des requêtes à la BDD.
import sqlite3
import json
from declaration import Declaration


class Database:
    # Constructeur
    def __init__(self):
        self.connection = None

    # Pour obtenir et ouvrir la connexion à la BDD.
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('database/database.db')
            self.connection.set_trace_callback(print)
        return self.connection

    # Pour fermer la connexion à la BDD.
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Fonction qui retourne toutes les déclarations ayant
    # 'search' dans leur nom de quartier ou nom d'arrondissement.
    def find_declarations(self, search):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM declarations WHERE NOM_QR LIKE"
                       " ? OR NOM_ARROND LIKE ?",
                       ('%'+search+'%', '%'+search+'%',))
        return cursor.fetchall()

    # Fonction qui retourne toutes les déclarations
    # entre deux dates.
    def get_declarations_between_dates(self, du, au):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT * FROM declarations WHERE DATE_DECLARATION >= ?"
            " AND DATE_DECLARATION < ?", (du, au,))
        declarations = cursor.fetchall()
        return [Declaration(one_declaration[0], one_declaration[1],
                one_declaration[2], one_declaration[3], one_declaration[4],
                one_declaration[5], one_declaration[6], one_declaration[7],
                one_declaration[8], one_declaration[9], one_declaration[10],
                one_declaration[11], one_declaration[12])
                for one_declaration in declarations]

    # Fonction qui retourne tous les quartiers ainsi que le nombre
    # de déclarations dans ce quartier.
    def get_declarations_by_quartier(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT NOM_QR, count(*) as compte FROM declarations "
            " GROUP BY NOM_QR ORDER BY compte DESC",)
        return cursor.fetchall()

    # Fonction qui retourne tous les quartiers qui figurent
    # dans la base de données.
    def get_all_quartiers(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT NOM_QR FROM declarations "
                       "GROUP BY NOM_QR ORDER BY NOM_QR ASC",)
        return cursor.fetchall()

    # Fonction qui permet de sauvegarder les données d'un
    # utilisateur.
    def save_user(self, user):
        connection = self.get_connection()
        if user.id is None:
            connection.execute("INSERT INTO users(fullname,"
                               "email, liste_quartiers, salt, "
                               "hash) values (?,?,?,?,?)",
                               (user.fullname, user.email,
                                json.dumps(user.liste_quartiers),
                                user.salt, user.hash))
            connection.commit()

            cursor = connection.cursor()
            cursor.execute("select last_insert_rowid()")
            result = cursor.fetchall()
            user.id = result[0][0]
        else:
            connection.execute("UPDATE users SET liste_quartiers=?,"
                               "picture=? WHERE email=?",
                               (json.dumps(user.liste_quartiers,
                                ensure_ascii=False), user.picture,
                                user.email))
            connection.commit()
        return user

    # Fonction qui retourne les informations d'un utilisateur
    # nécessaire pour la connexion.
    def get_user_info(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT salt, hash FROM "
                        "users WHERE email=?"), (email,))
        user = cursor.fetchone()

        if user is None:
            return None
        else:
            return user[0], user[1]

    # Fonction qui retourne toutes les informations d'un utilisateur
    def get_all_user_infos(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT * from users WHERE email=?"), (email,))
        return cursor.fetchone()

    # Fonction qui permet de sauvegarder la session en cours.
    def save_session(self, id_session, email):
        connection = self.get_connection()
        connection.execute(("INSERT INTO sessions(id_session, email)"
                            " values (?,?)"), (id_session, email))
        connection.commit()

    # Fonction qui permet de supprimer la session en cours.
    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("DELETE FROM sessions WHERE id_session=?"),
                           (id_session,))
        connection.commit()

    # Fonction qui permet d'obtenir la session en cours.
    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT email FROM sessions WHERE id_session=?"),
                       (id_session,))
        data = cursor.fetchone()

        if data is None:
            return None
        else:
            return data[0]

    # Fonction qui permet de valider si une adresse courriel est
    # déjà utilisée ou non lors de la création d'un utilisateur.
    def check_email_validity(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT * FROM users WHERE email=?"), (email,))
        return cursor.fetchone()

    # Fonction qui permet de sauvegarder une photo dans la
    # base de données.
    def create_picture(self, picture_id, data):
        connection = self.get_connection()
        connection.execute("INSERT INTO pictures(id, data) values (?,?)",
                           [picture_id, sqlite3.Binary(data.read())])
        connection.commit()

    # Fonction qui permet d'afficher une photo stockée dans la
    # base de données.
    def load_picture(self, pic_id):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT data FROM pictures WHERE id=?"), (pic_id,))
        picture = cursor.fetchone()

        if picture is None:
            return None
        else:
            return picture[0]

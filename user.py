class User:
    def __init__(self, id, fullname, email, liste_quartiers, salt,
                 hash, picture):
        self.id = id
        self.fullname = fullname
        self.email = email
        self.liste_quartiers = liste_quartiers
        self.salt = salt
        self.hash = hash
        self.picture = picture

    def asDictionnary(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "liste_quartiers": self.liste_quartiers,
            "password": self.password,
            "picture": self.picture,
        }

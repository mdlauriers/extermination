class Declaration:
    def __init__(self, no_declaration, date_declaration,
                 date_insp_vispre, nbr_extermin, date_debuttrait,
                 date_fintrait, no_qr, nom_qr, nom_arrond, coord_x,
                 coord_y, longitude, latitude):
        self.no_declaration = no_declaration
        self.date_declaration = date_declaration
        self.date_insp_vispre = date_insp_vispre
        self.nbr_extermin = nbr_extermin
        self.date_debuttrait = date_debuttrait
        self.date_fintrait = date_fintrait
        self.no_qr = no_qr
        self.nom_qr = nom_qr
        self.nom_arrond = nom_arrond
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.longitude = longitude
        self.latitude = latitude

    def asDictionary(self):
        return {
                 "no_declaration": self.no_declaration,
                 "date_declaration": self.date_declaration,
                 "date_insp_vispre": self.date_insp_vispre,
                 "nbr_extermin": self.nbr_extermin,
                 "date_debuttrait": self.date_debuttrait,
                 "date_fintrait": self.date_fintrait,
                 "no_qr": self.no_qr,
                 "nom_qr": self.nom_qr,
                 "nom_arrond": self.nom_arrond,
                 "coord_x": self.coord_x,
                 "coord_y": self.coord_y,
                 "longitude": self.longitude,
                 "latitude": self.latitude
        }

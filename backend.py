class Utilisateur():
    USERNAME: str
    MAIL: str
    TELEPHONE: str
    IS_ADMIN: bool

    def __init__(self, username, mail, telephone, admin) -> None:
        self.USERNAME = username
        self.MAIL = mail
        self.TELEPHONE = telephone
        self.IS_ADMIN = admin


class Lieu():
    NOM: str
    ADRESSE: str
    MAIL: str
    TELEPHONE: str
    NOTE: int
    HORAIRES: str
    TYPE: str
    CREATEUR: Utilisateur

    def __init__(self, nom: str, adresse: str, telephone: str, mail: str, horaires: str, createur: str, categorie: str, note: int) -> None:
        self.NOM = nom
        self.ADRESSE = adresse
        self.MAIL = mail
        self.HORAIRES = horaires
        self.NOTE = note
        self.CREATEUR = createur
        self.TYPE = categorie
        self.TELEPHONE = telephone

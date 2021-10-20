# Mathieu Des Lauriers
# Python3.9
# Script Python pour le téléchargement des données.
# Satisfait les exigences pour la fonctionnalité A1.
# Dépendances
import requests
import sqlite3
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

new_declarations = []


# Fonction qui télécharge les données de la ville de Montréal
# et qui les insère dans un fichier csv.
def download_data():
    # URL du site de la ville de Montréal.
    url = "https://data.montreal.ca/dataset"
    url += "/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/"
    url += "6173de60-c2da-4d63-bc75-0607cb8dcb74/download/"
    url += "declarations-exterminations-punaises-de-lit.csv"
    content = requests.get(url, allow_redirects=True)

    # Écrire le contenu dans un fichier csv.
    open("database/declarations.csv", "wb").write(content.content)


# Fonction qui prend les données du fichier csv et qui
# les insère dans la base de données.
def data_import():
    # Importer les données
    download_data()

    # Établir la connexion avec la BDD.
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()

    # Ouvrir le fichier CSV.
    with open('database/declarations.csv', 'r') as file:

        # Extraire le contenu du fichier.
        dr = csv.DictReader(file)

        # Parcourir chaque ligne.
        for i in dr:
            # Valider si une entree existe deja
            cursor.execute(
                "SELECT * FROM declarations WHERE "
                "NO_DECLARATION=?", (i['NO_DECLARATION'],))
            isPresent = cursor.fetchone()

            # Si l'entrée n'existe pas, l'insérer.
            if isPresent is None:
                entry = (i['NO_DECLARATION'], i['DATE_DECLARATION'],
                         i['DATE_INSP_VISPRE'],
                         i['NBR_EXTERMIN'], i['DATE_DEBUTTRAIT'],
                         i['DATE_FINTRAIT'], i['No_QR'],
                         i['NOM_QR'], i['NOM_ARROND'], i['COORD_X'],
                         i['COORD_Y'], i['LONGITUDE'],
                         i['LATITUDE'])
                cursor.execute("INSERT INTO declarations(NO_DECLARATION,"
                               "DATE_DECLARATION, DATE_INSP_VISPRE,"
                               "NBR_EXTERMIN,"
                               "DATE_DEBUTTRAIT,DATE_FINTRAIT,No_QR,NOM_QR,"
                               "NOM_ARROND,COORD_X,COORD_Y,LONGITUDE,LATITUDE)"
                               "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (entry))
                connection.commit()
                new_declarations.append(entry)

    send_email()
    connection.close()


# Fonction qui envoie un courriel lors de l'importation
# des données
def send_email():
    with open(r'email.yaml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    source_address = "mdlauriers1@gmail.com"
    destination_address = data["destination_address"]
    subject = "Nouvelles déclarations du jour"

    if not new_declarations:
        body = "Il n'y a aucune nouvelle déclaration depuis"
        body += "la dernière importation.\nBonne journée!"
    else:
        body = "Voici la liste des nouvelles déclarations "
        body += "depuis la dernière importation\n"
        body += "Num déclaration\t\tDate déclaration\t\t"
        body += "Date inspection\t\t"
        body += "Nb exterminations\tDate début trait.\tDate fin trait\t Num QR"
        body += "\t Nom QR\t Nom arrond.\tCoord X\tCoord Y\t"
        body += "Longitude\tLatitude\n"

        for el in new_declarations:
            body += el[0] + "\t\t\t\t" + el[1] + "\t" + el[2]
            body += "\t\t\t" + el[3]
            body += "\t\t" + el[4] + "\t" + el[5] + "\t" + el[6] + "\t"
            body += el[7] + "\t" + el[8] + "\t" + el[9] + "\t" + el[10]
            body += "\t" + el[11] + "\t" + el[12] + "\n"

        body += "Bonne journée!"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source_address
    msg['To'] = destination_address
    msg['ReplyTo'] = source_address

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(source_address, "uqam2021")
    text = msg.as_string()
    server.sendmail(source_address, destination_address, text)
    server.quit()


if __name__ == '__main__':
    data_import()

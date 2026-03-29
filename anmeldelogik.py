"""
2FA mit benutzeranmeldung (spätere gui erweiterung)

 - in diesem skript meldet sich der benutzer mit einem hardcoded mitarbeitercode und passwort an,
 - eine 2fa über email als bestätigung, 
 - 4 stelliger zufälliger 2fa code,
 - einfache login ausgabe

Hinweis:
 - wichtig in der json sind in dem punkt email variablen eingesetzt diese müssten 
   ersetzt werden in richtige emails oder in eine .env datei hinzugefügt werden 
 - SMTP- Zugang über Umgebnungsvariablen MAIL_USER und MAIL_PASS 
 - und ganz wichtig die passwörter für die jeweiligen benutzer sind folgende: 5936 ist 'Na:rc0qyVVy , 1731 ist Ti+<`_LcXp&C , 3117 ist ^LaTSVDbf_90
 - 
Noch ausstehende ideen:
 - 
 - logs mit zeitstempel
 - sicherheits überarbeitung mit limits von einloggen
 
"""
import secrets
import time
from dotenv import load_dotenv
import os 
#import tkinter as tk # aktuell noch nicht benutzt
import json
import random
import smtplib
from email.message import EmailMessage
import adminLogik
import hashlib
load_dotenv(".env")
if not os.getenv("MAIL_USER"):
    print("Warnung: .env nicht korrekt gesetzt")

def benutzerPassworddatenLaden():
    """
    lädt die json datei aus dem selben ordner wird in main aufgerufen 
    """
    with open("benutzerPassword.json","r", encoding="utf-8") as f:
        return json.load(f)

"""
def baustellendatenspeichern(baustellenListe):
    with open("baustellenListe.json", "w",encoding="utf-8") as f:
        json.dump(baustellenListe,f,indent=4, ensure_ascii=False)
"""

def benutzerabfragen():
    """
    abfrage des mitarbeiter codes 
    """
    print("Bitte Gib deinen vierstelligen mitarbeiter code ein: ")
    return input("Mitarbeitercode: ")

def passwortabfragen():
    """
    abfrage des mitarbeiterspassword
    """
    print("Bitte gib dein passwort jetzt ein: ")
    return input("Passwort: ")

def passwordhash(mitarbeiterpassword):
    return hashlib.sha256(mitarbeiterpassword.encode("utf-8")).hexdigest()

def randomlogik():
    """
    erstellt eine random zahl (muss noch zeitlich begrenzt werden oder nur einmal verwendbar gemacht werden )
    """
    zahl = secrets.randbelow(9000) + 1000
    timestampZahl = time.time()
    return zahl, timestampZahl

def abgleich(benutzerPasswordjson):
    """
    abgleich des mitarbeiter  codes mit der json wenn enthalten dann prüfung des passwortes
    dann wird die email in der json abgefragt und in zweifa weiter gereicht
    """

    for versuch in range(3):
        mitarbeitercode = benutzerabfragen()
        mitarbeiterpassword = passwortabfragen()
        passworthash = passwordhash(mitarbeiterpassword)
        if mitarbeitercode in benutzerPasswordjson["Mitarbeitercode"]:
            if passworthash == benutzerPasswordjson["Mitarbeitercode"][mitarbeitercode]["Passwort"]:
                emailadresse = emailauslesen(benutzerPasswordjson,mitarbeitercode)
                erfolg = zweiFa(benutzerPasswordjson,mitarbeitercode,emailadresse) 
                if erfolg:
                    return
                else:
                    print("Login fehlgeschlagen")
                    return
            else:
                print("Fehlerhafte Anmeldung")        
        else:
            print("Fehlerhafte anmeldung")
    print(f"Du hast die maximale anzahl an versuchen überschritten {versuch +1} ")
    return
        

def emailauslesen(benutzerPasswordjson,mitarbeitercode):
    """
    gibt die emailadresse des abgefragten mitarbeiter
    """
    email_key = benutzerPasswordjson["Mitarbeitercode"][mitarbeitercode]["Email"]
    email = os.getenv(email_key)
    if not email:
        print(f"Fehler: {email_key} nicht in .env gefunden!")
        return None
    return email
     
def zweiFa(benutzerPasswordjson,mitarbeitercode,emailadresse):
    """
    ruft emailschicken auf und gleicht den eingegebenen code aus eingabe2fa mit dem randomcode ab(zahl) und prüft auf leer 
    """
    if not emailadresse:
        print("Keine Gültige email gefunden")
        return False

    zahl,timestampZahl = randomlogik()
    emailschicken(zahl,emailadresse)

    for versuch in range(3):
        code = eingabe2fa()

        if code is None:
            print("ungültige eingabe")
            continue
        
        aktuelleZahl = time.time()
        if aktuelleZahl - timestampZahl > 300:
            print("Code ist abgelaufen")
            return False

        if zahl == code:
            login(benutzerPasswordjson,mitarbeitercode)
            return True
        else:
            print("falsche eingabe")
            
    print(f"Du hast die maximale anzahl an versuchen überschritten {versuch +1}")
    return False

def eingabe2fa():
    """
    zahlen eingabe und prüft auf int zahl 
    """
    print("Bitte gib den zugeschickten code ein: ")
    try:
        return int(input("Antwort: "))
    except ValueError:
        print("Ungültige eingabe")
        return None

def login(benutzerPasswordjson,mitarbeitercode):
    """
    eventueller anschluss in ein system
    """
    print("Du bist eingeloggt")
    adminabfrage(benutzerPasswordjson,mitarbeitercode)

def adminabfrage(benutzerPasswordjson,mitarbeitercode):
    """
    admin abfrage oder mitarbeiter
    """
    if benutzerPasswordjson["Mitarbeitercode"][mitarbeitercode]["Rolle"] == "admin":
        adminmenue()
    else:
        usermenue()

def adminmenue():
    print("TEst du bist admin")
    """hier dann vielleicht das neue skript einarbeiten"""
    adminLogik.ablauf()

def usermenue():
    print("test du bist user")
    """und hier die user gui"""

def emailschicken(zahl,emailadresse):
    """
    neues modul user, pw müssen selbst gesetzt werden für die email verschickung nötig in dem fall für gmail apppasswort
    prüft ob verfügbar 

    """
    user = os.getenv("MAIL_USER")
    pw = os.getenv("MAIL_PASS")
    if not user or not pw:
        print("Fehler: MAIL_USER oder MAIL_PASS nicht gesetzt!")
        return
    
    # 1. E-Mail-Objekt erstellen
    msg = EmailMessage()

    # Inhalt der Mail
    msg.set_content(f"Dein 2FA Code: {zahl}")

    # Betreff
    msg["Subject"] = "2FA"

    # Absender (DEINE Mail)
    msg["From"] = user

    # Empfänger
    msg["To"] = emailadresse 

    # 2. Verbindung zum Mailserver herstellen und senden
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            # Einloggen (mit App-Passwort! über os.getenv)
            smtp.login(user,pw)    
            # Mail senden
            smtp.send_message(msg)
        print(f"E-Mail wurde erfolgreich gesendet!")
    except Exception as e:
        print("Fehler beim Senden:",e )

def main():
    """
    ablauf programm
     - json wird aufgerufen 
     - zahl wird erstellt
     - code und passwort werden abgefragt
     - dann startet das eigentliche programm 
    """
    benutzerPasswordjson = benutzerPassworddatenLaden()
    abgleich(benutzerPasswordjson)

main()
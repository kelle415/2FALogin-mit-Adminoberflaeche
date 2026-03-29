"""
admin skript zum erstellen von passwörtern und neuen nutzern um gehashte passwörter zu benutzten 
"""
import json
import random
import string
import hashlib
import secrets

def benutzerPassworddatenLaden():
    """
    lädt die json datei aus dem selben ordner wird in main aufgerufen 
    """
    with open("benutzerPassword.json","r", encoding="utf-8") as f:
        return json.load(f)

def logsladen():
    with open("logsanmelden.json","r",encoding="utf-8") as f:
        return json.load(f)

def menueausgabe():
    print("\n","-" * 25)
    print("Was möchtest du machen ?")
    print("1. Mitarbeiter eintragen")
    print("2. Mitarbeiter löschen")
    print("3. Logs einsehen")
    print("4. Beenden")
    return str(input("Antwort: "))

def menueverweis(benutzerPasswordjson):
    while True:
        menueauswahl = menueausgabe()
        if menueauswahl in ("1","Mitarbeiter eintragen"):
            mitarbeitereintragen(benutzerPasswordjson)
        elif menueauswahl in ("2"," Mitarbeiter löschen"):
            ""
        elif menueauswahl in ("3","Logs einsehen"):
            ""
        elif menueauswahl in ("4", "beenden"):
            break
        else:
            print("Fehlerhafte eingabe")

def mitarbeitercodegenerieren():
    """
    erstellt eine random vierstellige zahl 
    """
    return str(random.randint(1000,9999))

def erstelltenCodePruefen(benutzerPasswordjson):
    while True:
        mitarbeitercode = mitarbeitercodegenerieren()
        if mitarbeitercode not in benutzerPasswordjson["Mitarbeitercode"]:
            return mitarbeitercode

def hashgenerieren(passwort):
    return hashlib.sha256(passwort.encode("utf-8")).hexdigest()
    
def passwortgenerieren():
    zeichen = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(zeichen) for _ in range(12))

def emailrolleeintragen():
    print("Bitte gib die emailadresse ein: ")
    emailadresse = str(input(""))
    print("Bitte gib die rolle ein (mitarbeiter/admin)")
    rolle = str(input(""))
    return emailadresse,rolle

def envKeyerstellen(mitarbeitercode):
    return f"Mitarbeiter_{mitarbeitercode}_Email"

def envKeyspeichern(envKey,emailadresse):
    with open(".env","a",encoding="utf-8") as f:
        f.write(f'{envKey}="{emailadresse}"\n')

def mitarbeitereintragen(benutzerPasswordjson):
    mitarbeitercode = erstelltenCodePruefen(benutzerPasswordjson)
    emailadresse,rolle = emailrolleeintragen()
    envKey = envKeyerstellen(mitarbeitercode)
    envKeyspeichern(envKey,emailadresse)
    passwort = passwortgenerieren()
    passworthash = hashgenerieren(passwort)
    daten = benutzerPasswordjson["Mitarbeitercode"][mitarbeitercode] = {
        "Passwort": passworthash,
        "Email": envKey,
        "Rolle": rolle
    }
    abfrage(benutzerPasswordjson,mitarbeitercode,passwort,daten)

def abfrage(benutzerPasswordjson,mitarbeitercode,passwort,daten):
    print(f"Benutzer wird angelegt sind die daten richtig? (J/N) {daten}")
    korrekturfrage = input("Antwort: ")
    if korrekturfrage in ("JA","j","J"):
        datenspeichern(benutzerPasswordjson)
        print("daten sind gespeichert")
        print(f"das passwort für den neuen Benutzer {mitarbeitercode} ist {passwort} merk dir das")
    elif korrekturfrage in ("Nein","N","n"):
        ""

def datenspeichern(benutzerPasswordjson):
    with open("benutzerPassword.json", "w", encoding="utf-8") as f:
        json.dump(benutzerPasswordjson, f, indent=4, ensure_ascii=False)

def ablauf():
    benutzerPasswordjson = benutzerPassworddatenLaden()
    #logsanmelden = logsladen()
    menueverweis(benutzerPasswordjson)
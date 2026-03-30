"""
hier entseht der code zum logs schreiben 
"""

import json
from datetime import datetime

def logsanmeldenLaden():
    """
    lädt die json datei aus dem selben ordner wird in main aufgerufen 
    """
    with open("logsanmelden.json","r", encoding="utf-8") as f:
        return json.load(f)

def dateinspeichernlogs(datenlogs):
    with open("logsanmelden.log","a",encoding="utf-8") as f:
        f.write(f"{datenlogs}\n")

def datenspeichernjson(datenjson):
    with open("logsanmelden.json", "w",encoding="utf-8") as f:
        json.dump(datenjson,f,indent=4, ensure_ascii=False)

def datenerstellenlogs(zeit,event,mitarbeitercode,ip):
    datenlogs = f" Zeit: {zeit} | Event: {event} | Mitarbeitercode: {mitarbeitercode} | IP: {ip}"
    return datenlogs

def datenerstellenjson(zeit,event,mitarbeitercode,ip,logsanmeldenJson):
    daten1 = {
        "Zeit": zeit,
        "Mitarbeitercode": mitarbeitercode,
        "Event": event,
        "Ip": ip
    }
    i = 0
    Loginversuch = "Loginversuch"
    while Loginversuch in logsanmeldenJson:
        i+=1
        Loginversuch = f"Loginversuch {i}"
    logsanmeldenJson[Loginversuch] = daten1
    datenjson = logsanmeldenJson
    return datenjson

def eventabfrage(welches):
    if welches == 1:
        event = "Login_Fehlgeschlagen_Code"
        return event
    elif welches == 2:
        event= "Login_Fehlgeschlagen_Password"
        return event
    elif welches == 3:
        event = "2FA_Fehlgeschlagen_Zeit"
        return event
    elif welches == 4:
        event= "2FA_Login_Erfolgreich"
        return event
    elif welches == 5:
        event = "2FA_Fehlgeschlagen"
        return event 
    elif welches == 6:
        event = "2FA_Fehlgeschlagen_Versuche"
        return event
    elif welches == 7:
        event = "Admin_Login"
        return event
    elif welches == 8:
        event = "Admin_Aktion_Hinzufügen"
        return event
    elif welches == 9:
        event = "Admin_Aktion_Löschen"
        return event
    elif welches == 10:
        event = "Admin_Aktion_Logs"
        return event
    elif welches == 11:
        event ="Admin_Aktion_Beenden"
        return event

def logundjson(mitarbeitercode,event):
    """hier kommt dann die entscheidung in welche gespeichert wird, datei muss mit übergeben werden und daten
    korrektur datei muss nicht übergeben werden da zwei funktionen zum speichern da sein werden 
    """
    logsanmeldenJson = logsanmeldenLaden()
    zeit = zeitstempel()
    ip = lokalip()
    datenlogs= datenerstellenlogs(zeit,event,mitarbeitercode,ip)
    datenjson= datenerstellenjson(zeit,event,mitarbeitercode,ip,logsanmeldenJson)
    dateinspeichernlogs(datenlogs)
    datenspeichernjson(datenjson)
    

def zeitstempel():
    jetzt = datetime.now()
    return jetzt.strftime("%d.%m.%Y %H:%M:%S")
    #print(zeit)

def lokalip():
    """später hier oder in einer neuen funktion das abfragen der ip hinzufügen """
    ""
    ip = "192.178.1.10"
    return ip



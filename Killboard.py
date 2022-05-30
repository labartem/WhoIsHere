import requests
import json

def getCharKillboard(id):
    abc = 0
    print(id)
    while abc < 5:

        try:


            url = "https://zkillboard.com/api/stats/characterID/" +str(id) + "/"
            x = requests.get(url)
            url_pers = "https://zkillboard.com/character/" +str(id) +"/"

            z = []

            if x.status_code == 200:
                z.append(x.json())
                z.append(url_pers)
                return z


        except Exception as e:
            if abc <5:
                print("TYPE: "  , type(e))
                print("Код ошибки запроса: ",x.status_code)
                print("Killboard file error ",e.__class__)
                #time.sleep(2)
                abc +=1
                continue
            else:
                return "ERROR"

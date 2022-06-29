import requests
import json
import time

end_point = "https://esi.evetech.net/latest"


class esi_data:
    def target_req(self,path,method,data =""):
        url = end_point + path
        a = url + data
        # Extra options
        # headers = {
        #     'accept': 'application/json',
        #     'Accept-Language': 'ru',
        #     'Content-Type': 'application/json',
        #     }
        #
        # params = (
        #      ('datasource', 'tranquility'),
        #      ('language', 'ru'),
        #      )
        abc = 0
        while abc < 2:
            try:
                abc +=1
                if method == "get":
                    x = requests.get(url,data = data)
                    if x.status_code == 200:
                        return  x.json()
                elif method == "post":
                    x = requests.post(url,data = data)
                    if x.status_code == 200:
                        return  x.json()
            except Exception as e:
                print("Error request " ,e.__class__ )
                if abc >= 2:
                    return "ERROR"

    def req_id(self,user_name):
        # Get a character ID
        path = "/universe/ids/"
        data = '["' + user_name + '"]'
        method = "post"
        return self.target_req(path,method,data)

    def req_userAffiliation(self,user_id):
        # Get User Corp and Alliance
        path = "/characters/affiliation/"
        data = '["' + str(user_id) + '"]'
        method = "post"
        return self.target_req(path,method,data)

    def req_userCorporation(self,corporation_id):
        path = "/corporations/" + str(corporation_id) + "/"
        method = "get"
        return self.target_req(path,method)

    def req_Names(self,target_id):
        # Getting different information from id
        path = "/universe/names/"
        data = '["' + str(target_id) + '"]'
        method = "post"
        return self.target_req(path,method,data)

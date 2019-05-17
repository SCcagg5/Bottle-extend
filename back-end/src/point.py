import requests
import os
import json as JSON
from requests.auth import HTTPBasicAuth
from sql import sql


login = os.getenv('SIGFOX_LOG', None)
password = os.getenv('SIGFOX_PASS', None)

class points:
    def __init__(self, userid):
        self.userid = userid

    def getall(self):
        return {"my_points": sql.get("SELECT `id` FROM `point` WHERE `user_id` = %s", (self.userid)), "shared_to_me": sql.get("SELECT `point_id` FROM `share` WHERE `user_id_to` = %s", (self.userid))}

class point:
    def __init__(self, db_id, key = None, point_id = None, userid = None):
        self.id = db_id
        self.userask = userid
        self.key = key
        self.sig_id = point_id
        self.err = [True]
        self.lat = None
        self.lng = None
        self.name = None
        self.user = None
        self.surname = None
        self.sharefrom = None
        self.shareto = []
        self.getinfos()


    def getinfos(self):
        if self.id is None:
            self.err = self.fromapiinfo()
        if self.err[0]:
            self.fromdbinfo()

    def infos(self):
        if not self.err[0]:
            return self.err
        if self.sig_id is None or self.id is None:
            return [False, "Bad Input", 403]
        ret = {
        "id" : self.id,
        "location": {"lat": self.lat, "lng": self.lng},
        "name": self.name,
        "surname": self.surname,
        "data": self.__getdata()[1]
        }
        if self.sharefrom is None:
            ret["shareto"] = self.shareto
        else:
            ret["sharefrom"] = self.sharefrom
        return [True, ret, None]

    def fromapiinfo(self):
        authentication = (login, password)
        r = requests.get(
        "https://api.sigfox.com/v2/devices/" + self.sig_id,
         auth=HTTPBasicAuth(login, password))
        try:
            data = JSON.loads(r.text)
            self.lat = data['location']['lat']
            self.lng = data['location']['lng']
            self.name = data['name']
        except:
            return [False, "Wrong ID", 500]
        self.surname = self.name
        return self.__input()

    def fromdbinfo(self):
        if self.id is None:
            self.id = sql.get("SELECT `id` FROM `point` WHERE `id_key` = %s", (self.sig_id))[0][0]
        data = sql.get("SELECT * FROM `point` WHERE `id` = %s", (self.id))[0]
        if data is None:
            return
        self.lat = data[1]
        self.lng = data[0]
        self.name = data[3]
        self.surname = data[4]
        self.user = data[5]
        self.key = data[6]
        self.sig_id = data[7]
        data = sql.get("SELECT mail FROM `user` INNER JOIN `share` ON user.id = share.user_id_to WHERE share.point_id = %s", (self.id))
        self.shareto = data if data is None else []
        if self.user is not self.userask:
            self.surname = sql.get("SELECT surname FROM `share` WHERE point_id = %s AND user_id_to = %s", (self.id, self.userask))[0][0]
            self.sharefrom = self.user


    def __input(self):
        succes = sql.input("INSERT INTO `point` (`id`, `lng`, `lat`, `name`, `surname`, `user_id`, `key`, `id_key`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", \
        (self.lng, self.lat, self.name, self.surname, self.userask, self.key, self.sig_id))
        if succes:
            return [True, None, None]
        return [False, "input error", 500]

    def __getdata(self):
        data = sql.get("SELECT * FROM `data` WHERE `point_id` = %s ORDER BY `id` DESC", (self.id))
        ret = []
        for i in data:
            b = {
                "date": i[2],
                "humidity": i[3],
                "turbidity": i[4],
                "conductance": i[5],
                "ph": i[6],
                "pression": i[7],
                "acceleration": i[8]
            }
            ret.append(b)
        return [True, ret, None]

    def __update(self):
        succes = sql.input("UPDATE `user` SET `lng` = %s, `lat` = %s , `name` = %s, `surname` = %s WHERE `id` = %s;", \
        (self.lng, self.lat, self.name, self.surname, self.id))
        if succes:
            return True
        return False

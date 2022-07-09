import sqlite3
import datetime
import time
import Esi
import Killboard
import os
# Creating a sqlite3 database and working with it

def connect_db():
    dir_path = "%s\\WhoIsHere\\user_data.db" %os.path.expanduser('~\Documents')
    global conn
    conn = sqlite3.connect(dir_path,check_same_thread=False)

def create_db():
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE if not exists user_info (Nickname text,Corporation text,Alliance text,Sec_status float,Ship_Kill int,Solo_Kill int,Ship_Lost int,Gang_Ratio int,ZKillboard_inf int, time_update float, url_zkillb text) """)
    cursor.execute(""" CREATE TABLE if not exists user_filter (Nickname text, User_acc int ) """)
    conn.commit()

def check_file_path():
    file_path = os.path.abspath(os.curdir)
    full_file_path = file_path + "\\user_data.db"

def insert_nick_in_filter(name):
    # Insert in general filter table
    name = search_nicknames_in_filter(name)
    cursor = conn.cursor()
    flag = 0
    for i in range(0,len(name)):
        cursor.execute("""INSERT INTO user_filter VALUES (?,?)""",(name[i],flag))
    conn.commit()
    cursor.close()

def insert_nick_in_filter_user_acc(name):
    # Insert in user acc filter table
    cursor = conn.cursor()
    flag = 1
    for i in range(0,len(name)):
        cursor.execute("""INSERT INTO user_filter VALUES (?,?)""",(name[i],flag))
    conn.commit()
    cursor.close()

def search_nicknames_in_filter(name):
    name = search_nicknames_in_filter_user_acc(name)
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE Nickname = ? and User_acc = 0"
    search_data_update = []
    for i in range(0,len(name)):
        cursor.execute(sql, (name[i],))
        result = cursor.fetchall()
        if result  == []:
            search_data_update.append(name[i])
        if result != []:
            pass
    cursor.close()
    return search_data_update

def search_nicknames_in_filter_user_acc(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE Nickname = ? and User_acc = ?"
    search_data_update = []
    for i in range(0,len(name)):
        cursor.execute(sql, (name[i],1))
        result = cursor.fetchall()
        if result  == []:
            search_data_update.append(name[i])
    cursor.close()
    return search_data_update


def search_nicknames_in_filter_for_add_user_acc(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE Nickname = ? and User_acc = ?"
    search_data_update = []
    for i in range(0,len(name)):
        cursor.execute(sql, (name[i],0))
        result = cursor.fetchall()
        if result  != []:
            update_filter_user_flag(cursor,name[i])
        if result == []:
            search_data_update.append(name[i])
    cursor.close()
    return search_data_update


def update_filter_user_flag(cursor,name):
    cursor.execute("UPDATE user_filter SET User_Acc = ? WHERE Nickname = ?", (1,name))
    conn.commit()

def get_data_in_filter():
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE User_acc = 0 "
    cursor.execute(sql,)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_data_in_u_acc_filter():
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE User_acc = 1 "
    cursor.execute(sql,)
    result = cursor.fetchall()
    cursor.close()
    return result

def delete_data_filter():
    cursor = conn.cursor()
    sql =    "DELETE FROM user_filter WHERE User_acc = 0 "
    cursor.execute(sql,)
    conn.commit()
    cursor.close()

def delete_data_u_acc_filter():
    cursor = conn.cursor()
    sql =    "DELETE FROM user_filter WHERE User_acc = 1 "
    cursor.execute(sql,)
    conn.commit()
    cursor.close()

def insert_data(name):
    # Inserting processed user data into a table
    cursor = conn.cursor()
    req_data_user = user_req(name)
    cursor.execute("""INSERT INTO user_info VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time(),req_data_user[9]))
    conn.commit()
    return req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8]
    cursor.close()

def del_data():
    cursor = conn.cursor()
    sql = "DELETE FROM user_info"
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def search_nicknames(name):
    # Searching for information in the database
    cursor = conn.cursor()
    sql = "SELECT * FROM user_info WHERE Nickname = ? "
    search_data_update = []
    cursor.execute(sql, (name,))
    result =  cursor.fetchall()
    cursor.close()
    if result  == []:
        return insert_data(name)
    if result != []:
        if (time.time() - result[0][9]) > 1800 or result[0][1] == "ERROR":
            return update_data(name)
        else:
            return result[0]

def update_data(name):
    # Update data about user
    cursor = conn.cursor()
    req_data_user = user_req(name)
    cursor.execute("""UPDATE user_info set Corporation = ? ,Alliance = ?,Sec_status = ? ,Ship_Kill = ? ,Solo_Kill = ?,Ship_Lost = ?,Gang_Ratio = ? ,ZKillboard_inf = ?, time_update = ?  WHERE Nickname == ?""",(req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time(),name))
    try:
        cursor.execute(sql,req)
    except Exception as e:
        print("SQL : " ,e.__class__)
    conn.commit()
    cursor.close()
    return req_data_user

def user_req(name):
    #Here is the processing of data received from the game server Eve online and the site zkillboard.com. Including options when some information may not be available.
    user_r = Esi.esi_data()
    user_id = user_r.req_id(name)
    if user_id == "ERROR":
        user_Alliance = "ERROR"
        user_Corporation = "ERROR"
        user_killboard = 0
    else:
        try:
            id_Affiliation  = user_r.req_userAffiliation(user_id['characters'][0]['id'])
            try:
                id_Alliance =  id_Affiliation[0]['alliance_id']
            except Exception as e:
                id_Alliance = 0
            id_Corporation =   id_Affiliation[0]['corporation_id']
            user_Corporation = user_r.req_Names(id_Corporation)[0]['name']
            if id_Alliance != 0 :
                user_Alliance = user_r.req_Names(id_Alliance)[0]['name']
            else:
                user_Alliance = "Not in an alliance"

        except Exception as e:
            user_Alliance = "Try again later"
            user_Corporation = "Try again later"
        user_killboard = Killboard.getCharKillboard(user_id['characters'][0]['id'])

    if user_killboard == 0:
        killb_info = 'None'
    else:
        killb_info = str(user_killboard[0]['info'])
    if killb_info == 'None' or killb_info == 'none' or killb_info == 'null':
        user_killb_info = 0
        user_secstatus = 0
        user_destroyship = 0
        user_solokill = 0
        user_shiplost = 0
        user_gangratio = 0
    else:
        user_killb_info = 1
        try:
            user_secstatus =  str("{:.2f}".format(user_killboard[0]['info']['secStatus']))
        except Exception as e:
            user_secstatus = "Нет в БД КБ"
        try:
            user_destroyship = str(user_killboard[0]['shipsDestroyed'])

        except Exception as e:
            user_destroyship = 0
        try:
            user_solokill = str(user_killboard[0]['soloKills'])
        except Exception as e:
            user_solokill = 0
        try:
            user_shiplost = str(user_killboard[0]['shipsLost'])
        except Exception as e:
            user_shiplost = 0
        try:
            user_gangratio = str(user_killboard[0]['gangRatio'])
        except Exception as e :
            user_gangratio = 0
    if user_id == "ERROR":
        return [name,user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info]
    else:
        return [user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info,user_killboard[1]]

def user_url_req(name):
    # We take a link to the character on the site zkillboard
    cursor = conn.cursor()
    sql = "SELECT * FROM user_info WHERE Nickname = ? "
    cursor.execute(sql, (name,))
    result =   cursor.fetchall()
    cursor.close()
    return result[0][10]

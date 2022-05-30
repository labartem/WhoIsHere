import sqlite3
import datetime
import time
import Esi
import Killboard
import os


dir_path = "%s\\WhoIsHere\\user_data.db" %os.environ['APPDATA']
conn = sqlite3.connect(dir_path,check_same_thread=False)

def create_db():
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE if not exists user_info (Nickname text,Corporation text,Alliance text,Sec_status float,Ship_Kill int,Solo_Kill int,Ship_Lost int,Gang_Ratio int,ZKillboard_inf int, time_update float, url_zkillb text) """)
    cursor.execute(""" CREATE TABLE if not exists user_filter (Nickname text, User_acc int ) """)
    conn.commit()

def check_file_path():
    file_path = os.path.abspath(os.curdir)
    # # print(file_path)
    # # print(os.path.abspath(__file__))
    # # print(os.getcwd())
    full_file_path = file_path + "\\user_data.db"
    # # print(full_file_path)
    # # print(os.path.isfile(full_file_path))

def insert_nick_in_filter(name):
    # # print("1")
    name = search_nicknames_in_filter(name)
    cursor = conn.cursor()
    # # print("Name ", name)
    flag = 0
    for i in range(0,len(name)):
        cursor.execute("""INSERT INTO user_filter VALUES (?,?)""",(name[i],flag))
        # # print(name[i])
    # for i in range(0,len(name)):
    #     # print("Sql insert", name[i])
    #     cursor.execute("""INSERT INTO user_filter VALUES (?)""",(name[i],))
    # cursor.execute("""INSERT INTO user_filter VALUES (?)""",(name[i]))
    conn.commit()
    cursor.close()

def insert_nick_in_filter_user_acc(name):
    cursor = conn.cursor()
    # # print("Name ", name)
    flag = 1
    for i in range(0,len(name)):
        cursor.execute("""INSERT INTO user_filter VALUES (?,?)""",(name[i],flag))
        # # print(name[i])
    conn.commit()
    cursor.close()

def search_nicknames_in_filter(name):
    name = search_nicknames_in_filter_user_acc(name)
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE Nickname = ? and User_acc = 0"
    search_data_update = []
    # # print("search_nicknames ",name)

    for i in range(0,len(name)):
        # cursor.execute(sql, (name,))
        # print(i, " ", name)
        cursor.execute(sql, (name[i],))
        result = cursor.fetchall()
        # print(result)
        if result  == []:
            # print("ISNERT",name[i])
            search_data_update.append(name[i])
        if result != []:
            pass
            # print("Есть в Бд удалили из списка ", name[i])

    # print("Выход ", search_data_update)
    cursor.close()
    return search_data_update

def search_nicknames_in_filter_user_acc(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE Nickname = ? and User_acc = ?"
    search_data_update = []
    # print("search_nicknames ",name)
    for i in range(0,len(name)):
        # cursor.execute(sql, (name,))
        # print(i, " ", name[i])
        cursor.execute(sql, (name[i],1))
        result = cursor.fetchall()
        # print("result " , result)
        if result  == []:
            # print("Не мой аккаунт ",name[i])
            search_data_update.append(name[i])
    # print(search_data_update)
    cursor.close()
    return search_data_update


def search_nicknames_in_filter_for_add_user_acc(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_filter WHERE Nickname = ? and User_acc = ?"
    search_data_update = []
    # print("search_nicknames nicknames for filter user ",name)
    for i in range(0,len(name)):
        # cursor.execute(sql, (name,))
        # print(i, " ", name[i])
        cursor.execute(sql, (name[i],0))
        result = cursor.fetchall()
        # print("result search nicknames for filter user " , name[i])
        if result  != []:
            # print("",name[i])
            update_filter_user_flag(cursor,name[i])
        if result == []:
            search_data_update.append(name[i])

    cursor.close()
    return search_data_update


def update_filter_user_flag(cursor,name):
    # print("update", name)
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


def insert_data_many(name):
    spisok_user = []
    z =[]
    # print(spisok_user)
    for l in range(0,len(name)):
        spisok_user.append([])
        for i in range(1) :
            x = time.time()
            spisok_user[l].append(name[l][0])
            spisok_user[l].append(x)

    z = spisok_user
    # for i in z:
    #     # print(i)
    for i in range(0,len(name)):
        cursor.execute("""INSERT INTO user_info VALUES (?,?)""",(z[i][0],z[i][1]))
    conn.commit()

def insert_data(name):
    cursor = conn.cursor()
    req_data_user = user_req(name)
    # print("INSERT NAME ",name)
    ## print(req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],sep = '\n')
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
    cursor = conn.cursor()
    sql = "SELECT * FROM user_info WHERE Nickname = ? "
    search_data_update = []
    # print("search_nicknames ",name)
    cursor.execute(sql, (name,))
    ## print(name[i])
    result =  cursor.fetchall()
    cursor.close()
    ## print("Fetachall: ", result)
    if result  == []:
        # print("ISNERT")
        return insert_data(name)
    if result != []:
        # print("Есть в БД", name,result[0][9])
        if (time.time() - result[0][9]) > 1800 or result[0][1] == "ERROR":

            # print("Последний раз обновлялся ",time.ctime(result[0][9]) ," ", result[0][1],result[0][2])
            # print(time.ctime(time.time()))
##            # print("Обновимся?")

            #search_data_update.append(name[i])

            return update_data(name)

##        elif result[0][1] == "ERROR":
##            # print("В ПОСЛЕДНИЙ РАЗ ПРОИЗОШЛА ОШИБКА")
##            return update_data(name)
        else:
            # print("рановато " , name)

            return result[0]


    ## print("Время  ",search_data_update)
    #update_data(search_data_update)
    ##    for i in range(0,len(search_dubliacate)):

def update_data(name):
    cursor = conn.cursor()

#Ben Solomon Carson

    # print("update_data " , name)
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
    user_r = Esi.esi_data()
    user_id = user_r.req_id(name)
    # print(user_id)
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
                # print("id_Alliance Ошибка: " ,e.__class__)
                id_Alliance = 0
                # print("нет Альянса")
            ## print("id Альянс\Корпорация " , id_Affiliation[0]['alliance_id'],"  " ,id_Affiliation[0]['corporation_id'] )

                    ## print(id_Alliance)
            id_Corporation =   id_Affiliation[0]['corporation_id']
                    ## print(id_Corporation)
            user_Corporation = user_r.req_Names(id_Corporation)[0]['name'] #
             ## print("id Корпорации " +  str(id_Corporation) + " name: " +   user_Corporation)
            # print(user_id['characters'])
            if id_Alliance != 0 :
                user_Alliance = user_r.req_Names(id_Alliance)[0]['name']
            else:
                user_Alliance = "Не состоит в альянсе"

        except Exception as e:
            # print("Affiliaton Ошибка: " ,e.__class__)
            user_Alliance = "Try again later"
            user_Corporation = "Try again later"



        user_killboard = Killboard.getCharKillboard(user_id['characters'][0]['id'])

    if user_killboard == 0:
        killb_info = 'None'
    else:
        killb_info = str(user_killboard[0]['info'])
    if killb_info == 'None' or killb_info == 'none' or killb_info == 'null':
        # print("Ник введён не правильно или не добавлен в БД Killboard")
        user_killb_info = 0
        user_secstatus = 0
        user_destroyship = 0
        user_solokill = 0
        user_shiplost = 0
        user_gangratio = 0
    else:
        user_killb_info = 1
        try:
            ## print("Sec status " , user_killboard['info']['secStatus'],sep = '\n',end = '\n')
            user_secstatus =  str("{:.2f}".format(user_killboard[0]['info']['secStatus']))
            ## print(user_secstatus)
        except Exception as e:
            # print("Ошибка: ", e.__class__)
            user_secstatus = "Нет в БД КБ"
        try:
            ## print("Уничтожил",user_killboard['shipsDestroyed'], " кораблей")
            user_destroyship = str(user_killboard[0]['shipsDestroyed'])
            ## print("User ", user_destroyship)
        except Exception as e:
            # print("user_destroyship Ошибка:  Уничтожил 0 кораблей" ,e.__class__)
            user_destroyship = 0
        try:
            ## print("Уничтожил в одиночку",user_killboard['soloKills'], " кораблей")
            user_solokill = str(user_killboard[0]['soloKills'])
            ## print("User ", user_solokill)
        except Exception as e:
            # print("User_solokill Ошибка: " ,e.__class__)
            user_solokill = 0
        try:
            ## print("Потерял: ",user_killboard['shipsLost'], " кораблей")
            user_shiplost = str(user_killboard[0]['shipsLost'])
            ## print("Потерял: ", user_shiplost)
        except Exception as e:
            # print("User_ship Ошибка: " ,e.__class__)
            user_shiplost = 0
        try:
            ## print(user_killboard['gangRatio'])
            user_gangratio = str(user_killboard[0]['gangRatio'])
        except Exception as e :
            # print("User_gang Ошибка: " ,e.__class__)
            user_gangratio = 0

    if user_id == "ERROR":
        return [name,user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info]
    else:
        ## print("id Альянса " + str(id_Alliance) + " name: " +  user_Alliance)
        # print(user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info, sep = '  ')
        return [user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info,user_killboard[1]]

def user_url_req(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_info WHERE Nickname = ? "
    cursor.execute(sql, (name,))
    ## print(name[i])
    result =   cursor.fetchall()
    # print("Resultat: " , result[0][10])
    cursor.close()
    return result[0][10]

# nicknames2 = [('ANNE MIDNIGHT',),
#             ('Awari Berend',),
#             ('CMOYIER',) ]

nicknames2 = ['ANNE MIDNIGHT',
            'Awari Berend',
            'CMOYIER',
            'brown drago']

nicknames = ['ANNE MIDNIGHT',
'Borntofly G Ornot',
'Borntofly H Ornot',
'Crassius',
'Dave Hawk']


# insert_nick_in_filter_user_acc(nicknames)
# insert_nick_in_filter(nicknames2)

# r = search_nicknames_in_filter(nicknames2)
# # search_nicknames_in_filter_for_add_user_acc(nicknames2)
# search_nicknames_in_filter_user_acc(r)
#
#
# search_nicknames_in_filter_for_add_user_acc(nicknames)
#check_database()
# create_db()




# nicknames_test = [('Arctos Bear',),
#     ('ANNE MIDNIGHT',),
#     ('Berlin Saimon',),
#     ('brown drago',),
#     ('Cubic Bistot',),
#     ('Drexston McDaddy',),
#     ('CMOYIER',)
                  # ]



#cursor.execute("""UPDATE user_info set Alliance = 102  WHERE Nickname == "Ben Solomon Carson" """)

#cursor.executemany("INSERT INTO testdb VALUES (?)", nicknames)
##name_is = "ANNE MIDNIGHT"
##cursor.execute("SELECT * FROM testdb WHERE Nickname=?",(name_is,))
### print(cursor.fetchall()[0][0])

##for i in cursor.execute("SELECT rowid, * FROM  testdb WHERE Nickname =?"):
##    # print(i)

##a = [('Arctos Bear',),]
### print(a[0])
##for i in nicknames_test:
##    search_nicknames(i)
## print("ZZZZ: ",z)
#insert_data(nicknames)


#del_data()
#cursor.execute("""INSERT INTO testdb VALUES ('Eugenii')""")

#insert_data("Evgenii")
##for row in cursor.execute("SELECT rowid, * FROM testdb ORDER BY Nickname"):
##    if (time.time() - row[2]) > 1800:
##        # print(row[1])
##        # print("Время обновиться")
##        # print( "%.2f" % ((row[2] - time.time())/60))
##        x = time.time()
##        # print(x)
##        cursor.execute("UPDATE testdb SET time_update = ? WHERE Nickname = ?", (x,row[1]))
##        conn.commit()
##    else:
##        # print("Время ещё не пришло")
##    ## print(time.ctime(row[2]))

# https://zkillboard.com/api/characterID/1120815457/shipTypeID/47270/

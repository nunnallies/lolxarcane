import mysql.connector 

def createConnectionToDb():
    try : 
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lolarcane"
        )
        if conn.is_connected():
            print("Connexion réussie")
            
            return conn
    except mysql.connector.Error as e : 
         print("Erreur lors de l'exécution :", e)
         return 
    

def closeConnectionToDb(conn):
    if conn.is_connected():
        conn.cursor().close()
        conn.close()
    return 0

def MatchNotInDb(matchId,mysqlconn):
    cursor=mysqlconn.cursor()
    sql=f"SELECT * FROM `match` WHERE `matchId`='{matchId}'"
    print(sql)
    cursor.execute(sql)
    resultat=cursor.fetchall()
    print(resultat)
    if not resultat : 
        print(f"match {matchId} non présent dans la bdd")
        return True
    else : 
        print("match déjà présent dans la bdd")
        return False 
    
def PuuidNotInDb(puuid,mysqlconn):  
    cursor=mysqlconn.cursor()
    sql=f"SELECT * FROM `players` WHERE `puuid`='{puuid}'"
    cursor.execute(sql)
    resultat=cursor.fetchall()
    if not resultat : 
        
        return True
    else :
        return False 
    
def SavePlayerPuuidinDb(puuid,summonerId,mysqlconn):
    cursor=mysqlconn.cursor()
    sql=f"INSERT INTO `players` (`puuid`,`summonerId`) VALUE ('{puuid}','{summonerId}')"
    cursor.execute(sql)
    return 0

def SaveMatch(data,mysqlconn):
    cursor=mysqlconn.cursor()
    print("enregistrement du match :" +  data[0])
    sql=f"INSERT INTO `match` (`matchId`, `gameMode`, `gameType`, `gameStartDate`, `gameDuration`, `summonnersPuuid`, `championList`) VALUES ('{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[4]}','{data[5]}','{data[6]}')"
    print(sql)
    cursor.execute(sql)
    return 0

def SelectAllFromplayers(mysqlconn):
    cursor=mysqlconn.cursor()
    sql=f"SELECT * FROM `players`"
    cursor.execute(sql)
    resultat=cursor.fetchall()
    return resultat 
import requests
from  utils.AccountUtils import * 
import csv
import datetime 
import os 
import json
import math
from utils.CsvUtils import *
from utils.databaseUtils import *
from utils.ApiUtils import *



def GetMatchesbyGameName(baseRegionUrl,key,gameName,tagLine):
    puuid=GetPuuidByGameName(baseRegionUrl,gameName,tagLine,key)
    result=GetMatchesIDByPuuid(baseRegionUrl,key,puuid,100)
    
    return result

def GetMatchesIDByPuuid(baseRegionUrl,key,puuid,nbofmatches):
    endpoint=f"{baseRegionUrl}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={nbofmatches}&api_key={key}"
    matchesid=treshold_endpoint_get_request(endpoint).json()
    print(matchesid)
    return matchesid

def GetMatchDataByMatchId(baseRegionUrl,key,matchId):
    endpoint=f"{baseRegionUrl}/lol/match/v5/matches/{matchId}?api_key={key}"
    matchData=treshold_endpoint_get_request(endpoint).json()
    return(matchData)

def IsInDateLineWanted():
    
    pass

def SaveMatchIntoCSV(csvName,matchData,refDate):
    
    fieldsnames=["matchId","gameMode","gameType","gameStartDate","gameDuration","summonnersPuuid","championList"]
    if 'metadata' in matchData : 
        #On extrait les données intéréssantes pour notre analyse
        matchId=matchData['metadata']['matchId']
        gameMode=matchData['info']['gameMode']
        gameType=matchData['info']['queueId']
        gameStartDate=GetDateFromTimestamp(refDate,matchData['info']['gameStartTimestamp'])
        championList=GetChampionListfromMatchData(matchData)
        summonnersPuuid=matchData['metadata']['participants'] 
        gameDuration=ConvertSecIntoMin(matchData['info']['gameDuration'])
        summonnersPuuid_json=json.dumps(summonnersPuuid)
        championList_json=json.dumps(championList)
        if gameMode !='ARAM' and MatchIdNotInCsv(csvName,matchId):
            data=[]
            data.append(matchId)
            data.append(gameMode)
            data.append(gameType)
            data.append(gameStartDate)
            data.append(gameDuration)
            data.append(summonnersPuuid_json)
            data.append(championList_json)
            WriteInCsv(csvName,fieldsnames,data)
        return 0
    else : 
        return -1
        

def GetDateFromTimestamp(RefDate,timestamp):
    splittedDate=RefDate.split("-")
    formatedRefDate=datetime.datetime(int(splittedDate[0]),int(splittedDate[1]),int(splittedDate[2]),0,0,0)
    realDate=formatedRefDate+datetime.timedelta(seconds=int(timestamp)/1000)
    return realDate

def GetChampionListfromMatchData(matchData):
    championlist=[]
    for elt in matchData['info']['participants'] :
        championlist.append(elt['championName'])
    return championlist



def ConvertSecIntoMin(timeToConvert):
    min=math.ceil(timeToConvert/60)
    return min

def SavePlayersMatches(baseRegionUrl,baseRegionUrl2,key,matchesid,RefDate,mysqlconn):
    for i in range (len(matchesid)) : 
        print("traitement du match :" + matchesid[i] )
        if MatchNotInDb(matchesid[i],mysqlconn):
            print("Obtention des données du match")
            matchData=GetMatchDataByMatchId(baseRegionUrl,key,matchesid[i])
            SaveMatchIntoDb(baseRegionUrl2,key,matchData,RefDate,mysqlconn)
    return 0
    

def SaveMatchIntoDb(baseRegionUrl,key,matchData,refDate,mysqlconn):
    
    if 'metadata' in matchData :
        print("metadata trouvées.")
        #On extrait les données intéréssantes pour notre analyse
        matchId=matchData['metadata']['matchId']
        gameMode=matchData['info']['gameMode']
        gameType=matchData['info']['queueId']
        gameStartDate=GetDateFromTimestamp(refDate,matchData['info']['gameStartTimestamp'])
        championList=GetChampionListfromMatchData(matchData)
        summonnersPuuid=matchData['metadata']['participants'] 
        
        #On enregistre les id de tout les joueurs dans la game pour pouvoir récupérer leurs parties plus tard
        
        SavePlayersPuuid(baseRegionUrl,key,matchData['metadata']['participants'],mysqlconn)
        print(f"enregistrement des joueurs du match {matchId} fait")
        gameDuration=ConvertSecIntoMin(matchData['info']['gameDuration'])
        summonnersPuuid_json=json.dumps(summonnersPuuid)  
        championList_json=json.dumps(championList)  
        print(gameMode)
        if gameMode != 'ARAM' or gameMode=='CLASSIC':
            print("5")
            data=[]
            data.append(matchId)
            data.append(gameMode)
            data.append(gameType)
            data.append(gameStartDate)
            data.append(gameDuration)
            data.append(summonnersPuuid_json)
            data.append(championList_json)
            SaveMatch(data,mysqlconn)
            return 0
    else : 
        return -1 
    
    
def SavePlayersPuuid(baseRegionUrl,key,summonnerspuuid,mysqlconn):
    for elt in summonnerspuuid:
        if PuuidNotInDb(elt,mysqlconn):
            summonerId=GetSummonnerIdByPuuid(baseRegionUrl,elt,key)
            SavePlayerPuuidinDb(elt,summonerId,mysqlconn)
            return 0
        else :
            return -1
        

def GatherManyPlayersData(baseRegionUrl,baseRegionUrl2,key,RefDate,mysqlconn):
    players=SelectAllFromplayers(mysqlconn)
    for row in players : 
        matchesid=GetMatchesIDByPuuid(baseRegionUrl,key,row[0],100)
        SavePlayersMatches(baseRegionUrl,baseRegionUrl2,key,matchesid,RefDate,mysqlconn)
    return 0
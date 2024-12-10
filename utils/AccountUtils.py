import requests 
from utils.ApiUtils import *

def GetPuuidByGameName(baseRegionUrl,gameName,tagLine,key):
    endpoint=f"{baseRegionUrl}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={key}"
    account=treshold_endpoint_get_request(endpoint).json()
    return account['puuid']

def GetSummonnerIdByPuuid(baseRegionUrl,puuid,key):
    endpoint=f"{baseRegionUrl}/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={key}"
    account=treshold_endpoint_get_request(endpoint).json()
    if "id" in account : 
        summonnerId=account['id']
        return summonnerId
    else :
        return "erreurId"

def GetPlayerSoloRankBySummonnerId(baseRegionUrl,summonnerId,key):
    endpoint=f"{baseRegionUrl}lol/league/v4/entries/by-summoner/{summonnerId}?api_key={key}"
    info=treshold_endpoint_get_request(endpoint).json()
    if ('queueType') in info and (info['queueType']=="RANKED_SOLO_5x5"):
        tier=info['tier']
        division=info['division']
    return tier,division
    
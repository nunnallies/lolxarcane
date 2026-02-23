import requests
from utils.MatchUtils import *
from utils.databaseUtils import *

# Analyse de l'impact d'Arcane sur la sélection des champions : 
# => Créer une bdd de Game récente entre 2022 et 2024 
#       - Utiliser l'Api Riot 
#       - Trouver un nombre de game important dans la BDD 
#       - Sous quel format stocker les games (CSV?)
#       - Tri sur les dates 
# => Analyser les pickrate par date 
# => Analyser le temps d'écran des persos de la série par acte 
# P-ê pour plus tard découper l'analyse en élo 

mysqlconn=createConnectionToDb()
REFDATE="1970-01-01"
key="key"
baseRegionUrl="https://europe.api.riotgames.com"
baseRegionUrl2="https://euw1.api.riotgames.com"
gameName="Denkipez"
tagLine="EUW"
#list=GetMatchesbyGameName(baseRegionUrl,key,gameName,tagLine,mysqlconn)

#SavePlayersMatches(baseRegionUrl,baseRegionUrl2,key,list,REFDATE,mysqlconn)
GatherManyPlayersData(baseRegionUrl,baseRegionUrl2,key,REFDATE,mysqlconn)




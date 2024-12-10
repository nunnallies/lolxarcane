import csv 
import os

def WriteInCsv(csvName,fieldsnames,data):
    with open(csvName,"a",newline='') as matchcsv :
            writer = csv.DictWriter(matchcsv, fieldsnames)
            if os.path.exists(csvName) and os.path.getsize(csvName) == 0:
                writer.writeheader()
            writer.writerow(dict(zip(fieldsnames,data)))
    return 0

def MatchIdNotInCsv(csvName,matchId):
    if os.path.exists(csvName) :
        with open(csvName, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                for row in reader:
                
                    if len(row) > 0 and row[0] == matchId:
                        return False
                    else :
                        return True 
    else : 
        return True
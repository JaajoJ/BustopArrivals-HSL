import json
import time
import os
import csv
import sys
from datetime import datetime

busValues = "HSL-pysakit.csv"

#Examples
#print(inputToLongID("H2056"))
#Output: 1020124
#print(inputToLongID("Kaivokatu"))
#Output: 1020124
def inputToLongID(userInput):
    if userInput == "":
        return ""
    csvFile = open(busValues)
    csvreader = csv.reader(csvFile)
    header = next(csvreader)

    rows = []
    for i in csvreader:
        rows.append(i)
    csvFile.close()
    for i in rows:
        if userInput in i:
            return i[1], i[2], i[10]
    return "-1"

#Example downloadID(1020131)
def downloadID(ID):
    f = open("command","r")
    command = [f.readline().replace('\n', ''),f.readline()]
    os.system(command[0]+str(ID)+command[1])
    f.close()


def IDtoBusTimes(ID):
    f = open("output.json")

    data = json.load(f)

    BusInfo = []
    #For metros and train stations 
    stopType = "stops"
    if "stations" in data["data"]:
        stopType = "stations"

    for i in data["data"][stopType][0]["stoptimesForPatterns"]:
        BusHeadsign = i["pattern"]["headsign"]
        for o in i["stoptimes"]:

            BusNum = o["trip"]["route"]["shortName"]
                
            Arrival = time.strftime('%H:%M', time.gmtime(int(o["realtimeArrival"])))
            BusInfo.append({'BusNum': BusNum, 'BusHeadsign': BusHeadsign, 'Arrival': Arrival, 'ArrivalSeconds': int(o['realtimeArrival'])})
                
      
    f.close()

    #Sort the Arrival times
    def myFunc(e):
        return e['ArrivalSeconds']
    BusInfo.sort(key=myFunc)
    return BusInfo

#asks for input its either in E1248 or 198248912 or Kaivokatu
# if argument contains f it formats output
# if you dont give output it uses already downloaded file
def main(argument):
    longID, shortID, busstopName = inputToLongID(input())
    if longID == "-1":
        print("Invalid input! Check HSL-pysakit.csv for valid codes or names.")
    else:
        downloadID(longID)

        BusTimes = IDtoBusTimes(longID)

        if "f" in argument: 
            BusInfo8 = [BusTimes[0], BusTimes[1],BusTimes[2], BusTimes[3], BusTimes[4], BusTimes[5], BusTimes[6], BusTimes[7]]
            
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            print("{:10}       {:50}         {:50}\n".format(shortID,busstopName, current_time))
                        
            headlines = "{:10}       {:50}         {:50}".format("Bussi","Suunta","Kellonaika")
            print(headlines)

            for i in BusInfo8:
                print("{:10}       {:50}         {:50}".format(i["BusNum"], str(i["BusHeadsign"]), i["Arrival"]))

        else:
            print(BusTimes)
            
main(str(sys.argv))

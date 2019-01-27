import requests #For http POST
import time #For sleeping and current time for file and folder creation
from xml.etree import ElementTree
import shutil #For savings Get'ed pictures
################ END IMPORTS ################

################ START DERBYNET CONFIG ################
derbynetserverIP = "http://192.168.1.134"   #Server that's hosting DerbyNet - NO TRAILING SLASH!
checkinintervalnormal = 5   #seconds between polling server when not racing
checkinintervalracing = 0.25 #seconds between polling server when racing
################ END DERBYNET CONFIG ################

################ START SETUP GLOBALS ################
replayurl = derbynetserverIP + "/action.php"
Pstatus = -1
PreplayFin = 0
playbackstarted = False
################ END SETUP GLOBALS ################

################ START MAIN ROUTINE ################
# Setup last checkin to ensure triggered on first run
lastcheckin = time.time() - 30

# setup polling interval
checkininterval = checkinintervalnormal

# Setup photo location list
racerphotosloc = ["one", "two", "three"]

while True:
    curTime = time.time()
    #is it time to check in?
    if curTime - lastcheckin > checkininterval:
        #Time to check - let's do this
        racerparams = {'query':"poll.now-racing", 'row-height':"100"}
        print(racerparams)
        r = requests.get(url = replayurl, params = racerparams)
        print(r.url)
        #Check we got a valid response
        if r.status_code == requests.codes.ok:
            # Reset checkin time
            lastcheckin = curTime

            #Look for the data
            print(r.content)
            tree = ElementTree.fromstring(r.content)
            for currentheat in tree.iter("current-heat"):
                print("Den =",currentheat.text)
                print("Race =",currentheat.attrib["round"])
                print("Heat",currentheat.attrib["heat"],"of",currentheat.attrib["number-of-heats"])
            for racer in tree.iter("racer"):
                print("Name:",racer.attrib["name"])
                print("Car:",racer.attrib["carname"])
                print("Number:",racer.attrib["carnumber"])
                print("Lane:",racer.attrib["lane"])
                print("Photo located:",racer.attrib["photo"])
                print("Finish Time:",racer.attrib["finishtime"])
                print("Index:",int(racer.attrib["lane"])-1)
                racerphotosloc[int(racer.attrib["lane"])-1] = racer.attrib["photo"]

            #Get the photos
            print(racerphotosloc)
            for num, photoloc in enumerate(racerphotosloc, start=1):
                print("Racer#",num,":",photoloc)

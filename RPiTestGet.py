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

# Setup lists
raceinfo = ["Den", "Race", "Heat", "Total Heats"]
racerinfo = [ ["Name", "Car", "Number", "Lane", "Photo Location"], ["Name", "Car", "Number", "Lane", "Photo Location"], ["Name", "Car", "Number", "Lane", "Photo Location"] ]
racerphotosloc = ["one", "two", "three"]

while True:
    curTime = time.time()
    #is it time to check in?
    if curTime - lastcheckin > checkininterval:
        #Time to check - let's do this
        racerparams = {'query':"poll.now-racing", 'row-height':"150"}
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
                raceinfo = [currentheat.text, currentheat.attrib["round"], currentheat.attrib["heat"], currentheat.attrib["number-of-heats"] ]
            for racer in tree.iter("racer"):
                racerindex = int(racer.attrib["lane"])-1
                racerinfo[racerindex] = [racer.attrib["name"], racer.attrib["carname"], racer.attrib["carnumber"], racer.attrib["lane"], racer.attrib["photo"] ]
                racerphotosloc[int(racer.attrib["lane"])-1] = racer.attrib["photo"]

            #Get the photos
            print(raceinfo)
            print(racerinfo[0])
            print(racerinfo[1])
            print(racerinfo[2])
            print(racerphotosloc)
            for num, photoloc in enumerate(racerphotosloc, start=1):
                print("Racer#",num,":",photoloc)
                imgurl = derbynetserverIP + "/derbynet/" + photoloc
                imgresponse = requests.get(imgurl)
                if imgresponse.status_code == requests.codes.ok:
                    racerimgname = "racer" + num + ".jpg"
                    with open(racerimgname, 'wb') as f:
                        f.write(imgresponse.content)



# Global Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
num_hosts = 50

#A host is created using a dictionary, so we can add/remove attributes as we please

#Build a default host at position x, y. Modify this function to add more params to the host structure
def buildDefaultHostAtXY(x, y, s):
    return {'x': x, 'y': y, 'bandwidth': s, 'signalDistance': 0, 'myAP': None, 'showInterference': False}
                    
def distanceBetweenHosts(h1, h2):
    return sqrt((h1['x'] - h2['x'])**2 + (h1['y'] - h2['y'])**2)    

def drawLineBetweenHosts(h1, h2):
    line(h1['x'], h1['y'], h2['x'], h2['y'])

def printInterferenceStats():
    totalInterference = 0
    for host in hosts:
        x = host['x']
        y = host['y']
        
        for compare in hosts:
            if(distanceBetweenHosts(host, compare) < host['signalDistance']):
                totalInterference = totalInterference + 1
        
    print "Average number of interfering nodes per node: "
    print (totalInterference + 0.0) / len(hosts)
    print "Number of nodes:"
    print len(hosts)
    print "Number of interferences:"
    print totalInterference
                           
def refreshHostSignalDistances():
    for host in hosts:
        myAP = host['myAP']
        host['signalDistance'] = sqrt((host['x'] - myAP['x'])**2 + (host['y'] - myAP['y'])**2)
    

def refreshTopology():
    setHostAPsTravisAlgorithm()
    refreshHostSignalDistances()
    printInterferenceStats()
    
    
#Randomly generate some hosts for the network
def randomlyGenerateHosts(num):
    hosts = []
    for i in range(num):
        hosts.append(buildDefaultHostAtXY(random(SCREEN_WIDTH), random(SCREEN_HEIGHT), random(50)))
    return hosts

def randomlyGenerateHostsInGroups(numGroups, maxHostsPerGroup, spread):
    hosts = []
    
    for i in range(numGroups):
        x = random(SCREEN_WIDTH)
        y = random(SCREEN_HEIGHT)
        for j in range(int(random(maxHostsPerGroup-1) + 1)):
            hosts.append(buildDefaultHostAtXY(x + random(spread) - spread/2, y + random(spread) - spread/2, random(50)))
    
    return hosts
   
def setHostAPsNullAlgorithm():
    for host in hosts:
        host['myAP'] = AP 
        
def setHostAPsTravisAlgorithm():
    subAPs = []
    global hosts
    
    for host in hosts:
        if host.has_key('myAP'):
            del host['myAP']
    
    hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(AP, k) - AP['signalDistance'])
    
    for host in hosts:
        if 'myAP' not in host:
            host['myAP'] = AP
            host['signalDistance'] = sqrt((host['x'] - AP['x'])**2 + (host['y'] - AP['y'])**2)
            setSurroundingHostsAP(host)
   
     
def setSurroundingHostsAP(subAP):
    tempHosts = sorted(hosts, key=lambda k: distanceBetweenHosts(subAP, k) - subAP['signalDistance']) 
    
    print "subAP signalDistance: " + str(subAP['signalDistance'])
    
    numberOfHosts = 0
    for host in tempHosts:
        if 'myAP' not in host and distanceBetweenHosts(subAP, host) < subAP['signalDistance']:
            host['myAP'] = subAP
            
            numberOfHosts += 1
            
            # arbitrary number (should make this max number of hosts meaningful)
            if numberOfHosts > 5:
                return


#Processing setup -- use this only for setting up processing stuff, not other python stuff   
def setup():
    print "Setup" 
    ellipseMode(CENTER)
    size(SCREEN_WIDTH,SCREEN_HEIGHT)
    background(255)     

#Draw loop - should ideally be used only for drawing stuff, not our algorithms
def draw():
    
    background(255);
    
    for host in hosts:
        stroke(0)
        fill(0)
        x = host['x']
        y = host['y']
        bandwidth = host['bandwidth']
        ellipse(x, y, 10,10)
        drawLineBetweenHosts(host, host['myAP'])
        if(host['showInterference'] or AP['showInterference']):
            noStroke()
            fill(0, bandwidth)
            distToAP = host['signalDistance']
            ellipse(x, y, 2*distToAP, 2*distToAP)
        
    noStroke() 
    fill(0,0,255)
    ellipse(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 50, 50)
    
#Called when the mouse is pressed -- I know, profound.
def mousePressed():
    
    clickedOnHost = False
    
    for host in hosts:
        x = host['x']
        y = host['y']
        
        
        #If we clicked on this host
        if(abs(x - mouseX) < 10 and abs(y - mouseY) < 10):
            
            host['showInterference'] = not host['showInterference']
            clickedOnHost = True
            break
        
    if(not clickedOnHost):
        hosts.append(buildDefaultHostAtXY(mouseX, mouseY, random(50)))
        refreshTopology()
        
    #If we clicked the AP, flip its showInterference attribute
    if(abs(mouseX - AP['x']) <= 25 and abs(mouseY- AP['y']) <= 25):
        AP['showInterference'] = not AP['showInterference']
       
         
AP = buildDefaultHostAtXY(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0)
        
#hosts = randomlyGenerateHosts(num_hosts)
hosts = randomlyGenerateHostsInGroups(10,10,50)

refreshTopology()
#The 'showInterference' flag on the AP is used to override the showInterference flag for all other hosts to generate an overall interference map
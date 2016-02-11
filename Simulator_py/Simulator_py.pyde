

# Global Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
num_hosts = 50
show_stats = False
current_algorithm = 1
total_number_algorithms = 5
current_randomization_pattern = 1

#A host is created using a dictionary, so we can add/remove attributes as we please

#Build a default host at position x, y. Modify this function to add more params to the host structure
def buildDefaultHostAtXY(x, y, s):
    return {'x': x, 'y': y, 'bandwidth': s, 'signalDistance': 0, 'myAP': None, 'showInterference': False, 'nodeColor': 0}
                    
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
    
def show_statistics():
    fill(0, 102, 153)
    totalInterference = 0
    for host in hosts:
        x = host['x']
        y = host['y']
        
        for compare in hosts:
            if(distanceBetweenHosts(host, compare) < host['signalDistance']):
                totalInterference = totalInterference + 1
        
    text("Average number of interfering nodes per node: ", 10, 10)
    text ((totalInterference + 0.0) / len(hosts), 300, 10)
    text ("Number of nodes: ", 10, 30)
    text (len(hosts), 120, 30)
    text ("Number of interferences:", 10, 50)
    text (totalInterference, 170, 50)
                           
def refreshHostSignalDistances():
    for host in hosts:
        myAP = host['myAP']
        host['signalDistance'] = sqrt((host['x'] - myAP['x'])**2 + (host['y'] - myAP['y'])**2)
    

def refreshTopology():
    global current_algorithm
    global hosts
    global AP
    if abs(current_algorithm % total_number_algorithms) == 1:
        setHostAPsNullAlgorithm()
        print("Null algorithm")
    elif abs(current_algorithm % total_number_algorithms) == 2:
        setHostAPsTravisAlgorithm()
        print("Travis' Algorithm")
    elif abs(current_algorithm % total_number_algorithms) == 3:
        setHostAPsTravisAlgorithmExtended()
        print("Travis' Algorithm Extended")
    elif abs(current_algorithm % total_number_algorithms) == 4:
        setHostAPsErikAlgorithm()
        print("Erik's Algorithm")
    else:
        setHostAPsIanAlgorithm(5, hosts, AP)
        print("Ian's Algorithm")
    refreshHostSignalDistances()
    #printInterferenceStats()
    
    
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
        host['nodeColor'] = 0
    
##AFTER MORE TESTING, I'VE REALIZED THAT THIS ALGO IS TOTALLY SHIT AT THIS POINT -- NEEDS WORK (-Ian)    
def setHostAPsIanAlgorithm(numSubAPs, hosts, baseAP):
    
    global AP
    
    for host in hosts:
        host['myAP'] = host
    
    for i in range(min(numSubAPs, len(hosts))):
        for host in hosts:
            distanceSum = 0
            host['distanceSum'] = 0
            host['nodeColor'] = 1
            for compare in hosts:
                if(compare['myAP'] == host):
                    host['distanceSum'] += distanceBetweenHosts(host, compare)
                else:
                    host['distanceSum'] += distanceBetweenHosts(host, compare)*999999999
            
        
        hosts = sorted(hosts, key=lambda k:  k['distanceSum'])
        hosts[i]['myAP'] = baseAP
        
    for host in hosts[numSubAPs:]:
        distances = []
        for subAP in hosts[:numSubAPs]:
            distances.append(distanceBetweenHosts(host, subAP))
        host['myAP'] = hosts[distances.index(min(distances))]
        host['nodeColor'] = 0
        
    if AP == baseAP:
        for host in hosts:
            if host['myAP'] == AP:
                subHosts = []
                for compare in hosts:
                    if compare['myAP'] == host:
                        subHosts.append(compare)
                if(len(subHosts) >= numSubAPs/2):
                    setHostAPsIanAlgorithm(numSubAPs, subHosts, host)

def setHostAPsErikAlgorithm():
    global AP
    global hosts
    for host in hosts:
        host['myAP'] = None
    hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(AP, k))
    temp = hosts
    subAPs = []
    for i in range(5):
       hosts[i]['myAP'] = AP
       hosts[i]['nodeColor'] = 0 
       subAPs.append(hosts[i])
    for host in hosts[5:]: 
       temp_hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(host, k))
       for h in temp_hosts:
           if h in subAPs:
               host['myAP'] = h
               subAPs.append(host)
               host['signalDistance'] = sqrt((host['x'] - h['x'])**2 + (host['y'] - h['y'])**2)
               break
       host['nodeColor'] = 0
    
def setHostAPsTravisAlgorithmExtended():
    
    global AP
    global hosts
    
    setHostAPsTravisAlgorithm()
    
    currentSubs = []
    for host in hosts:
        if host['myAP'] == AP:
            currentSubs.append(host)
                  
    for host in hosts:
        if host in currentSubs:
            continue
        distances = []
        for subAP in currentSubs:
            distances.append(distanceBetweenHosts(host, subAP))
        host['myAP'] = currentSubs[distances.index(min(distances))]
        
                        
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
            host['nodeColor'] = 1
            host['signalDistance'] = sqrt((host['x'] - AP['x'])**2 + (host['y'] - AP['y'])**2)
            setSurroundingHostsAP(host)
   
     
def setSurroundingHostsAP(subAP):
    tempHosts = sorted(hosts, key=lambda k: distanceBetweenHosts(subAP, k) - subAP['signalDistance']) 
    
    #print "subAP signalDistance: " + str(subAP['signalDistance'])
    
    numberOfHosts = 0
    for host in tempHosts:
        if 'myAP' not in host and distanceBetweenHosts(subAP, host) < subAP['signalDistance']:
            host['myAP'] = subAP
            host['nodeColor'] = 0
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
        if host['nodeColor'] == 1:
            fill(255,0,0)
            ellipse(x, y, 20, 20)
        else:
            ellipse(x, y, 10, 10)
        bandwidth = host['bandwidth']
        drawLineBetweenHosts(host, host['myAP'])
        if(host['showInterference'] or AP['showInterference']):
            noStroke()
            fill(0, bandwidth)
            distToAP = host['signalDistance']
            ellipse(x, y, 2*distToAP, 2*distToAP)
    
    if show_stats:
        show_statistics()
        
    noStroke() 
    fill(0,0,255)
    ellipse(AP['x'], AP['y'], 50, 50)
    
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

#Called when key is pressed -- Holy shit no way?
def keyPressed(): 
    global hosts
    global show_stats
    global current_algorithm
    global current_randomization_pattern
    # refreshes screen with new topology
    if key == 'r' or key == 'R': 
        if current_randomization_pattern %2 == 1:
            hosts = randomlyGenerateHosts(num_hosts)
        else:
            hosts = randomlyGenerateHostsInGroups(10,10,50)
        refreshTopology() 
    if key == ' ' and show_stats:
        show_stats = False
    elif key == ' ':
        show_stats = True
    elif keyCode == RIGHT:
        current_algorithm = current_algorithm + 1
        refreshTopology()
    elif keyCode == LEFT:
        current_algorithm = current_algorithm - 1
        refreshTopology()
    elif keyCode == UP:
        current_randomization_pattern = current_randomization_pattern + 1
    elif keyCode == DOWN:
        current_randomization_pattern = current_randomization_pattern - 1
        
        
#The AP is going to be centered by default, but this should be changeable (not all networks have centered AP)         
AP = buildDefaultHostAtXY(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0)
        
hosts = randomlyGenerateHosts(num_hosts)

refreshTopology()
#The 'showInterference' flag on the AP is used to override the showInterference flag for all other hosts to generate an overall interference map
import csv
# Global Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
num_hosts = 100
show_stats = False
current_algorithm = 1
total_number_algorithms = 7
current_randomization_pattern = 1



##############This is some statistics code from StackOverflow which I'm using for standard deviation##############

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = (sum(data) + 0.0 )/len(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

##############This is some statistics code from StackOverflow which I'm using for standard deviation##############




#A host is created using a dictionary, so we can add/remove attributes as we please

#Build a default host at position x, y. Modify this function to add more params to the host structure
def buildDefaultHostAtXY(x, y, s):
    return {'x': x, 'y': y, 'bandwidth': s, 'signalDistance': 0, 'myAP': None, 'showInterference': False, 'nodeColor': 0}
                    
def distanceBetweenHosts(h1, h2):
    return sqrt((h1['x'] - h2['x'])**2 + (h1['y'] - h2['y'])**2)    

def drawLineBetweenHosts(h1, h2):
    line(h1['x'], h1['y'], h2['x'], h2['y'])
    
def show_statistics():
    fill(0, 0, 0, 200)
    rect(0,0,365,165)
    
    fill(255)
    
    
def getInterferenceStats():
    global AP
    totalInterference = []
    totalHops = []
    totalDistance = []
    totalTraffic = 0
    
    
    for host in hosts:
        x = host['x']
        y = host['y']
        
        interference = 0
        hops = 0
        distance = distanceBetweenHosts(host, host['myAP']) 
        
                        
        for compare in hosts:
            if(distanceBetweenHosts(host, compare) < host['signalDistance']):
                interference = interference + 1
                
        hostTmp = host['myAP']
        
        while hostTmp != AP:
            hops = hops + 1
            distance += distanceBetweenHosts(hostTmp, hostTmp ['myAP'])
            hostTmp = hostTmp['myAP']
                
        totalInterference.append(interference)
        totalHops.append(hops)
        totalDistance.append(distance)
        totalTraffic = totalTraffic + ((hops + 1) * host['bandwidth'])

    
    return {'interference': (sum(totalInterference) + 0.0) / len(hosts),
        'sd_interference': (pstdev(totalInterference)),
        'nodes': len(hosts),
        'hops': (sum(totalHops) + 0.0) / len(hosts),
        'sd_hops': pstdev(totalHops),
        'distance': (sum(totalDistance) + 0.0) / len(hosts),
        'sd_dist': (pstdev(totalDistance)),
        'totalTraffic': totalTraffic}
                
                
def show_statistics():
    fill(0, 0, 0, 200)
    rect(0,0,365,155)
    
    fill(255)
    
    stats = getInterferenceStats()
    #totalTraffic = totalTraffic + ((hops + 1) * host['bandwidth'])
        
    text("Average number of interfering nodes per node: ", 10, 40)
    text (stats['interference'], 300, 40)
    text ("Standard deviation: +/-", 10,60)
    text ('%.3f'%(stats['sd_interference']), 155, 60)
    text ("Number of nodes: ", 10, 20)
    text (stats['nodes'], 120, 20)
    text("Average number of hops to AP: ", 10, 80)
    text (stats['hops'], 200,80)
    text ("Standard deviation: +/-", 10, 100)
    text ('%.3f'%(stats['sd_hops']), 155, 100)
    text("Average signal distance travelled to AP: ", 10, 120)
    text (stats['distance'], 250, 120)
    text ("Standard deviation: +/-", 10, 140)
    text ('%.3f'%(stats['sd_dist']), 155, 140)
    text ("Total Traffic: ", 10, 160)
    text (stats['totalTraffic'] , 80, 160)

                                                      
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
        print("Erik's Algorithm: Distance Greedy")
    # elif abs(current_algorithm % total_number_algorithms) == 5:
    #     setHostAPsErikAlgorithm3()
    #     print("Erik's Algorithm 3: Distance Greedy")
    elif abs(current_algorithm % total_number_algorithms) == 5:
        setHostAPsIanAlgorithmRecursive(5, hosts, AP)
        print("Ian's Algorithm: Recursive")
    elif abs(current_algorithm % total_number_algorithms) == 6:
        setHostAPsIanAlgorithmRecursiveNew(5, hosts, AP)
        print("Ian's Algorithm: Recursive New")
    else:
        setHostAPsIanAlgorithm(5, hosts, AP)
        print("Ian's Algorithm")
    refreshHostSignalDistances()
    
    
#Randomly generate some hosts for the network
def randomlyGenerateHosts(num):
    hosts = []
    for i in range(num):
        hosts.append(buildDefaultHostAtXY(random(SCREEN_WIDTH), random(SCREEN_HEIGHT), random(10)))
    return hosts

def randomlyGenerateHostsInGroups(numGroups, hostsPerGroup, spread):
    hosts = []
    
    for i in range(numGroups):
        x = random(SCREEN_WIDTH)
        y = random(SCREEN_HEIGHT)
        for j in range(hostsPerGroup):
            hosts.append(buildDefaultHostAtXY(x + random(spread) - spread/2, y + random(spread) - spread/2, random(10)))
    
    return hosts
   
def setHostAPsNullAlgorithm():
    for host in hosts:
        host['myAP'] = AP 
        host['nodeColor'] = 0
    
##AFTER MORE TESTING, I'VE REALIZED THAT THIS ALGO IS TOTALLY SHIT AT THIS POINT -- NEEDS WORK (-Ian)    
def setHostAPsIanAlgorithmRecursive(numSubAPs, hosts, baseAP):
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
                    
# a subAP and its hosts will reconfigure to find the most central host to be the subAP
def recalculateSubAPs(hosts,subAPs,baseAP):
    global AP

    for s in subAPs:
        groupOfHosts = [s]
        for host in hosts:
            if host['myAP'] == s:
                groupOfHosts.append(host)
        avgX = 0
        avgY = 0
        for h in groupOfHosts:
            avgX += h['x']
            avgY += h['y']
        avgX = avgX/len(groupOfHosts)
        avgY = avgY/len(groupOfHosts)
        
        minDistance = 999999999
        newSub = s
        for h in groupOfHosts:
            distanceToCenter = sqrt((avgX - h['x'])**2 + (avgY - h['y'])**2)
            if minDistance > distanceToCenter:
                newSub = h
                minDistance = distanceToCenter
        s['nodeColor'] = 0
        for h in groupOfHosts:
            if h == newSub:
                h['nodeColor'] = 1
                h['myAP'] = baseAP
            else:
                h['myAP'] = newSub

#hosts will choose the closest AP or SubAP to be their AP
def redetermineMyAPs(hosts, baseAP):
    currentSubs = [baseAP]
    
    for host in hosts:
        if host['myAP'] == baseAP:
            currentSubs.append(host)
    
    subsubs = []
    for s in currentSubs[1:]:
        for host in hosts:
            if host['myAP'] == s: 
                if distanceBetweenHosts(host,s) > distanceBetweenHosts(host,baseAP):
                    host['myAP']=baseAP
                subsubs.append(host)
             
    
    currentSubs = currentSubs + subsubs
    for host in hosts:
        if host in currentSubs:
            continue
        distances = []
        for subAP in currentSubs:
            distances.append(distanceBetweenHosts(host, subAP))
        host['myAP'] = currentSubs[distances.index(min(distances))]
        
        

def setHostAPsIanAlgorithmRecursiveNew(numSubAPs, hosts, baseAP):
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
    
    #this to the end is the only difference between the Old one
    
    #this causes issue due to my poorly written function
    # subs = []
    # for host in hosts:
    #     if host['myAP'] == AP:
    #         subs.append(host)
    # recalculateSubAPs(hosts,subs,AP)
    
    # the subSubAPs and its hosts will reconfigure to find the most central host to be the subAP
    for host in hosts:
        if host['myAP'] == AP:
            subHosts = []
            for compare in hosts:
                if compare['myAP'] == host:
                    subHosts.append(compare)
            recalculateSubAPs(hosts,subHosts,host)
    #hosts choose the closest AP or subAP to be their new AP
    redetermineMyAPs(hosts,baseAP)    

            
    
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

def setHostAPsErikAlgorithm():
    global AP
    global hosts
    for host in hosts:
        host['myAP'] = None
    hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(AP, k))
    temp = hosts
    subAPs = []
    for i in range(4):
       hosts[i]['myAP'] = AP
       hosts[i]['nodeColor'] = 0 
       subAPs.append(hosts[i])
    for host in hosts[4:]: 
       temp_hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(host, k))
       for h in temp_hosts:
           if h in subAPs:
               host['myAP'] = h
               subAPs.append(host)
               host['signalDistance'] = sqrt((host['x'] - h['x'])**2 + (host['y'] - h['y'])**2)
               break
       host['nodeColor'] = 0
       
def setHostAPsErikAlgorithm2():
    # A combination of distance greedy and bandwidth. host will first 
    # look for a subAP with large bandwidth within a certain range then settle for the closest host
    # -- edit this to make it be a combination of closest node/least amount of hops between host and AP 
    global AP
    global hosts
    for host in hosts:
        host['myAP'] = None
    hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(AP, k))
    temp = hosts
    subAPs = []
    for i in range(4):
       hosts[i]['myAP'] = AP
       hosts[i]['nodeColor'] = 0 
       subAPs.append(hosts[i])
    for host in hosts[4:]: 
       assigned = False
       temp_hosts = sorted(hosts, key=lambda k: k['bandwidth'], reverse=True)
       closest_hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(host, k))
       for h in temp_hosts:
           if h in subAPs and distanceBetweenHosts(host, h) < 200:
               host['myAP'] = h
               subAPs.append(host)
               host['signalDistance'] = sqrt((host['x'] - h['x'])**2 + (host['y'] - h['y'])**2)
               assigned = True
               break
       if not assigned:
           host['myAP'] = closest_hosts[i]
           subAPs.append(host)
           host['signalDistance'] = sqrt((host['x'] - closest_hosts[i]['x'])**2 + (host['y'] - closest_hosts[i]['y'])**2)
               
           
       host['nodeColor'] = 0

# def gatherNearbyHosts(i, subAPs):
#     global hosts
#     temp_hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(subAPs[i], k))
#     for h in temp_hosts:
#         if h in subAPs:
#             break
#         possibleNewDistance = sqrt((subAPs[i]['x'] - h['x'])**2 + (subAPs[i]['y'] - h['y'])**2)
#         if h['myAP'] != None:
#             if h['signalDistance'] > possibleNewDistance:
#                 h['myAP'] = subAPs[i]
#                 h['signalDistance'] = possibleNewDistance
#                 subAPs.append(h)
                
#                 print "new distance, change AP:", possibleNewDistance
#         else:
#             h['myAP'] = subAPs[i]
#             h['signalDistance'] = possibleNewDistance
#             subAPs.append(h)
            
#             print "new distance:", possibleNewDistance
#             print h['x'],h['y']
    
# def setHostAPsErikAlgorithm3():
#     global AP
#     global hosts
#     for host in hosts:
#         host['myAP'] = None
#     hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(AP, k))
#     temp = hosts
#     subAPs = []
    
#     for i in range(4):
#        hosts[i]['myAP'] = AP
#        hosts[i]['nodeColor'] = 0 
#        subAPs.append(hosts[i])
       
#     for i in range(len(subAPs)):
#         gatherNearbyHosts(i,subAPs)

#     for i in range(len(hosts[4:])): 
#         host = hosts[i+4]
#         temp_hosts = sorted(hosts, key=lambda k: distanceBetweenHosts(host, k))
#         for h in temp_hosts:
#             if h in subAPs:
#                 host['myAP'] = h
#                 subAPs.append(host)
#                 host['signalDistance'] = sqrt((host['x'] - h['x'])**2 + (host['y'] - h['y'])**2)
#                 gatherNearbyHosts(-1,subAPs)
#                 break
#         host['nodeColor'] = 0


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
            if numberOfHosts > 6:
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
        
    #If we clicked the AP, flip its showInterference attribute
    if(abs(mouseX - AP['x']) <= 25 and abs(mouseY- AP['y']) <= 25):
        AP['showInterference'] = not AP['showInterference']
    elif(not clickedOnHost):
        hosts.append(buildDefaultHostAtXY(mouseX, mouseY, random(50)))
        refreshTopology()
        
    

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
            hosts = randomlyGenerateHostsInGroups(10, 50, num_hosts)
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

#get statistics and write out to csv
# with open('/Users/travissiems/NetworkTopology/Simulator_py/stats.csv', 'wb') as csvfile:
#     fieldnames = ['algorithm', 'nodes', 'interference', 'sd_interference', 'hops', 'sd_hops', 'distance', 'sd_dist', 'totalTraffic', 'cluster']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     # each run is done 3 times, avg will be taken
#     # pure randomly
#     for numHost in [30, 100, 250]:
#         for trial in range(0, 3):
#             hosts = randomlyGenerateHosts(numHost)
#             show_stats=True
#             for alg in range(1, total_number_algorithms+1):
#                 current_algorithm = alg
#                 refreshTopology()
#                 stats = (getInterferenceStats())
#                 stats['algorithm'] = current_algorithm
#                 stats['cluster'] = 'None'
#                 writer.writerow(stats)
        
#     # groups
#     for numHost in [3, 10, 25]:
#         for trial in range(0, 3):
#             # weakly clustered
#             hosts = randomlyGenerateHostsInGroups(numHost, 10, 100)
#             show_stats=True
#             for alg in range(1, total_number_algorithms+1):
#                 current_algorithm = alg
#                 refreshTopology()
#                 stats = (getInterferenceStats())
#                 stats['algorithm'] = current_algorithm
#                 stats['cluster'] = 'Weak'
#                 writer.writerow(stats)    
        
#             # strongly clustered
#             hosts = randomlyGenerateHostsInGroups(numHost, 10, 35)
#             show_stats=True
#             for alg in range(1, total_number_algorithms+1):
#                 current_algorithm = alg
#                 refreshTopology()
#                 stats = (getInterferenceStats())
#                 stats['algorithm'] = current_algorithm
#                 stats['cluster'] = 'Strong'
#                 writer.writerow(stats)    

# print("Before Loop")

# file = open("ianStats.txt", 'w')
# for i in range(total_number_algorithms):
#     print("Algorithm")
#     current_algorithm = i
#     write = "Algorithm: "
#     write += str(i)
#     write += "\n Random:\n"
#     write += "Low Density: \n"
#     hosts = randomlyGenerateHosts(30)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
#     write += "Medium Density: \n"
#     hosts = randomlyGenerateHosts(100)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
#     write += "High Density: \n"
#     hosts = randomlyGenerateHosts(250)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
    
#     write += "\n Weakly Clustered:\n"
#     write += "Low Density: \n"
#     hosts = randomlyGenerateHostsInGroups(3, 10, 100)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
#     write += "Medium Density: \n"
#     hosts = randomlyGenerateHostsInGroups(10, 10, 100)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
#     write += "High Density: \n"
#     hosts = randomlyGenerateHostsInGroups(25, 10, 100)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
    
#     write += "\n Strongly Clustered:\n"
#     write += "Low Density: \n"
#     hosts = randomlyGenerateHostsInGroups(3, 10, 35)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
#     write += "Medium Density: \n"
#     hosts = randomlyGenerateHostsInGroups(10, 10, 35)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
#     write += "High Density: \n"
#     hosts = randomlyGenerateHostsInGroups(25, 10, 35)
#     refreshTopology()
#     write += str(getInterferenceStats())
#     write += "\n"
    
#     file.write(write)
    
    
    
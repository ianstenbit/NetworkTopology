# Global Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
num_hosts = 50

#A host is created using a dictionary, so we can add/remove attributes as we please

#Build a default host at position x, y. Modify this function to add more params to the host structure
def buildDefaultHostAtXY(x, y, s):
    return {'x': x, 'y': y, 'signal': s, 'showInterference': False}


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
        

#hosts = randomlyGenerateHosts(num_hosts)
hosts = randomlyGenerateHostsInGroups(10,10,50)
#The 'showInterference' flag on the AP is used to override the showInterference flag for all other hosts to generate an overall interference map

AP = buildDefaultHostAtXY(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0)
   
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
        signal = host['signal']
        ellipse(x, y, 10,10)
        line(x, y, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        if(host['showInterference'] or AP['showInterference']):
            noStroke()
            fill(0, signal)
            distToAP = sqrt((x-SCREEN_WIDTH/2)**2 + (y-SCREEN_HEIGHT/2)**2)
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
        
    #If we clicked the AP, flip its showInterference attribute
    if(abs(mouseX - SCREEN_WIDTH/2) <= 50 and abs(mouseY- SCREEN_HEIGHT/2) <= 50):
        AP['showInterference'] = not AP['showInterference']
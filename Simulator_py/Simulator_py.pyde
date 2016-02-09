
def randomlyGenerateHosts(num):
    hosts = []
    for i in range(num):
        hosts.append({'x' : random(1600),
                      'y' : random(900),
                      'showInterference' : False})
    return hosts

hosts = randomlyGenerateHosts(50)
AP = {'x': 800, 'y': 450, 'showInterference': False}

def setup():
    print "Setup"
    
    ellipseMode(CENTER)
    size(1600,900)
    background(255)
        

def draw():
    
    background(255);
    
    for host in hosts:
        stroke(0)
        fill(0)
        x = host['x']
        y = host['y']
        ellipse(x, y, 10,10)
        line(x, y, 800, 450)
        if(host['showInterference'] or AP['showInterference']):
            noStroke()
            fill(0, 20)
            distToAP = sqrt((x-800)**2 + (y-450)**2)
            ellipse(x, y, 2*distToAP, 2*distToAP)
        
        
    fill(0,0,255)
    ellipse(800, 450, 50, 50)
    

def mousePressed():
    
    for host in hosts:
        x = host['x']
        y = host['y']
        
        if(abs(x - mouseX) < 10 and abs(y - mouseY) < 10):
            print host
            host['showInterference'] = not host['showInterference']
            break

    if(abs(mouseX - 800) <= 50 and abs(mouseY- 450) <= 50):
        AP['showInterference'] = not AP['showInterference']
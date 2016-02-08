from collections import namedtuple

Host = namedtuple("Host", "x y")

#Host number 0 is the AP
def randomlyGenerateHosts(num):
    hosts = []
    for i in range(num):
        hosts.append(Host(x = random(1600), y = random(900)))
    return hosts

hosts = randomlyGenerateHosts(50)
AP = Host(x = 800, y = 450)

def setup():
    print "Setup"
    
    ellipseMode(CENTER)
    size(1600,900)
    background(255)
        

def draw():
    
    for host in hosts:
        fill(0)
        ellipse(getattr(host, 'x'), getattr(host, 'y'), 10,10)
        line(getattr(host, 'x'), getattr(host, 'y'), getattr(AP, 'x'), getattr(AP, 'y'))
        
        
    fill(0,0,255)
    ellipse(getattr(AP, 'x'), getattr(AP, 'y'), 50, 50)

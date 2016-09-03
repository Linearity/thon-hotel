import math
import sys

class Constraint:
    elementIndices = ()
    
    def satisfy( elements ):
        return

class DistanceConstraint (Constraint):
    distance = 0
    
    def __init__( self, elementIndices = (), distance = 0 ):
        self.elementIndices = elementIndices
        self.distance = distance
        
    def satisfy( self, elements ):
        index0 = self.elementIndices[0]
        index1 = self.elementIndices[1]
        
        midpoint = vectorScale( vectorSum( elements[ index0 ], elements[ index1 ] ), 0.5 )
        
        unitR0 = vectorUnit( vectorDiff( elements[ index0 ], midpoint ) )
        elements[ index0 ] = vectorSum( midpoint, vectorScale( unitR0, 0.5 * self.distance ) )
        
        unitR1 = vectorUnit( vectorDiff( elements[ index1 ], midpoint ) )
        elements[ index1 ] = vectorSum( midpoint, vectorScale( unitR1, 0.5 * self.distance ) )
        
        return
    
class PinConstraint (Constraint):
    position = (0, 0)
    
    def __init__( self, elementIndices = (), position = (0, 0) ):
        self.elementIndices = elementIndices
        self.position = position
        
    def satisfy( self, elements ):
        index0 = self.elementIndices[0]
        elements[ index0 ] = self.position
        
        

sizeX = 400
sizeY = 300
t = 0.0
dtp = 1.0
#positions = [(-20, 100.0), (20, 100.0), (60, 100.0), (100, 100.0), (140, 100.0), (150, 100.0)]
positions = [(-20.0, 99.9999750025), (8.911694006227787, 72.35715450887334), (44.99998895953905, 55.104944752772425), (85.00004124945079, 55.10495424104732), (121.08834709399369, 72.3571912097667), (150.0, 99.9999750025)]
#prevPositions = [(-20, 100.0), (20, 100.0), (60, 100.0), (100, 100.0), (140, 100.0), (150, 100.0)]
prevPositions = [(-20.0, 99.9999750025), (8.911694006227787, 72.35715450887334), (44.99998895953905, 55.104944752772425), (85.00004124945079, 55.10495424104732), (121.08834709399369, 72.3571912097667), (150.0, 99.9999750025)]

constraints = [
       DistanceConstraint( (0,1), 40 ),
       DistanceConstraint( (1,2), 40 ),
       DistanceConstraint( (2,3), 40 ),
       DistanceConstraint( (3,4), 40 ),
       DistanceConstraint( (4,5), 40 ),
       PinConstraint( (0,), (-20, 100.0) ),
       #PinConstraint( (5,), (150.0, 100.0) )
]

forces = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
gravity = (0, -0.01)
mouseSpring = None

def screenOffset( position ):
    return (position[0] + (sizeX / 2), -position[1] + (sizeY / 2))

def screenUnoffset( position ):
    return (position[0] - (sizeX / 2), (sizeY / 2) - position[1])

def setup():
    size( sizeX, sizeY )

def drawEndpoint( position ):
    screenPosition = screenOffset( position )
    ellipse( screenPosition[0], screenPosition[1], 10, 10 )

def drawLine( startPoint, endPoint ):
    screenStartPoint = screenOffset( startPoint )
    screenEndPoint = screenOffset( endPoint )
    line( screenStartPoint[0], screenStartPoint[1], screenEndPoint[0], screenEndPoint[1] )
    
def vectorSum( x1, x2 ):
    return ( x1[0] + x2[0], x1[1] + x2[1] )

def vectorDiff( x1, x2 ):
    return ( x1[0] - x2[0], x1[1] - x2[1] )

def vectorScale( x, k ):
    return ( x[0] * k, x[1] * k )

def vectorDotProduct( x1, x2 ):
    return x1[0] * x2[0] + x1[1] * x2[1]

def vectorSqMag( x ):
    return x[0] * x[0] + x[1] * x[1]

def vectorMag( x ):
    return math.sqrt( vectorSqMag( x ) )

def vectorUnit( x ):
    m = vectorMag( x )
    if m == 0:
        return x
    else:
        return vectorScale( x, 1.0 / m )
        
def vectorProj( x1, x2 ):
    unitX2 = vectorScale( x2, 1.0 / vectorMag( x2 ) )
    return vectorScale( unitX2, vectorDotProduct( x1, unitX2 ) )

def motion( x, xp, f, dt ):
    global dtp

    assert( len( positions ) is len( prevPositions ) )
    for k in range( len( x ) ):
        # temp = vectorSum(
        #     x[k],
        #     vectorScale(
        #         vectorSum(
        #             vectorScale( vectorDiff( x[k], xp[k] ), dt / dtp ),
        #             vectorScale( (0, -0.01), dt * dt )
        #         ),
        #         0.9999
        #     )
        # )
        
        temp = vectorSum(
           x[k],
           vectorScale(
               vectorSum(
                   vectorDiff( x[k], xp[k] ),
                   vectorScale( f[k], dt * dt )
               ),
               0.9999
           )
        )
                          
        xp[k] = x[k]
        x[k] = temp
    
    dtp = dt
    
def satisfyConstraints( elements ):
    for k in range(1):
        for c in constraints:
            c.satisfy( elements )
            
def applyGravity( f ):
    for k in range( len( f ) ):
        f[k] = vectorSum( f[k], gravity )
        
def applyMouseSpring( x, f ):
    if mouseSpring is not None:
        f[mouseSpring] = vectorSum( f[mouseSpring], vectorScale( vectorDiff( screenUnoffset( (mouseX, mouseY) ), x[mouseSpring] ), 0.0001 ) )
        
def clearForces( f ):
    for k in range( len( f ) ):
        f[k] = (0, 0)
        
def mousePressed():
    global mouseSpring
    
    candidates = []
    distances = []
    for k in range( len( positions ) ):
        difference = vectorDiff( screenUnoffset( (mouseX, mouseY) ), positions[k] )
        magnitude = vectorSqMag( difference )
        if magnitude < 100.0:
            candidates.append( k )
            distances.append( magnitude )
           
    #minimum = sys.float_info.max
    minimum = 100000000000.0
    winner = None
    for k in range( len( candidates ) ):
        if distances[k] < minimum:
            minimum = distances[k]
            winner = k
    
    if winner is not None:
        mouseSpring = candidates[winner]
        
def mouseReleased():
    global mouseSpring
    mouseSpring = None
    

def draw():
    global t
    t_new = millis()
    dt = t_new - t
    t = t_new
    
    clearForces( forces )
    applyGravity( forces )
    applyMouseSpring( positions, forces )
    
    for k in range( 0, int( dt // 0.05  ) ):
        satisfyConstraints( positions )
        motion( positions, prevPositions, forces, 0.05 )
    
    satisfyConstraints( positions )
    motion( positions, prevPositions, forces, math.fmod( dt, 0.05 ) )

    background(255)
    fill(255)
    stroke(0)
    
    for x in positions:
        drawEndpoint( x )
        
    for c in constraints:
        if len( c.elementIndices ) is 2:
            drawLine( positions[ c.elementIndices[0] ], positions[ c.elementIndices[1] ] )
            
    fill(64, 255, 64)
    stroke( 64, 255, 64)
    
    ellipse( mouseX, mouseY, 5, 5 )
    
    if mouseSpring is not None:
        drawLine( positions[mouseSpring], screenUnoffset( (mouseX, mouseY) ) )
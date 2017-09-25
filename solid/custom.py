from solid import *
from solid import extensions
from math import *
import operator as op


def hullPath(path, vertexObject):
    '''
    path: collection of points as tuples
    vertexObject: object to copy at each vertex
    '''
    obj = None
    for point0, point1 in zip(path[0:-1], path[1:]):
        segment = hull( vertexObject.copy().translate(point0) + vertexObject.copy().translate(point1))
        obj = obj + segment if obj else segment
    return obj

def hullObject(vertex, vertexObject):
    '''
    vertex: collection of points as tuples
    vertexObject: object to copy at each vertex
    '''

    objects = [vertexObject.copy().translate(point) for point in vertex]
    return hull(objects)

def distance(p0, p1):
    d = sqrt(sum([(v0-v1)**2 for v0,v1 in zip(p0,p1)]))
    return d

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

def berzier(points, segments=10, maxSegment=None):
    '''
    points: collection of 2d points as tuples. First will be taen as starting point, last as ending
    '''
    def nBerzier(nps,t):
        n=len(nps)-1
        return sum([ncr(n,i)*ip*(1-t)**(n-i)*t**i for i,ip in enumerate(nps)])

    if maxSegment is not None:
        vertexPathLenght =sum([distance(p0,p1) for p0,p1 in zip(points[:-1], points[1:])])
        segments = ceil(vertexPathLenght/maxSegment)

    berzierPath = []
    for i in range(0,int(segments+1)):
        berzierPath.append([nBerzier(p,float(i)/segments) for p in zip(*points)])

    return berzierPath

def arc2d(points=None,angles=None,center=None,r=None, sol=0, segments=10, maxSegment=None):
    '''
    points: 2 or 3 points where the arc pass through
    angles: start and end angles of the arc, in degrees
    center: 1 point for the arc center
    r: 1 or 2 radius lengths
    sol: index, when more than one solution is posible
    segments: nr of segments to use (def:10)
    maxSegments: max lenght of each segment
    Supported combinations: 
    - angles + center + 1 r
    - angles + center + 2 r
    - 3 points
    - 2 points + center => 2 solutions
    - 2 points + 1 r => 4 solutions
    - 1 point + 1 angle + center => 3 solutions
    '''
    angDelta=None
    rDelta=None

    def createSegments():
        if maxSegment:
            nSegments = int(segments if angDelta*r0/segments<maxSegment else floor(angDelta*r0/maxSegment))
        else:
            nSegments = int(segments)
        angStep = angDelta/float(nSegments)
        rStep = rDelta/float(nSegments)

        pos = []
        for i in range(0,nSegments+1):
            ang = ang0 + float(i)*angStep
            r = r0 + float(i)*rStep
            pos.append([center[0]+cos(ang)*r, center[1]+sin(ang)*r])
        return pos

    def toRad(deg): return deg / 180.*pi

    def isCollection(l):
        return isinstance(l,(list,tuple))

    def nrPoints():
        return 0 if not points else len(points) if isCollection(points) and isCollection(points[0]) else 0

    def getAngle(center,point):
        return atan2(point[1]-center[1],point[0]-center[0])

    def sign(val):
        return 1 if val>0 else -1 if val<0 else 0

    if nrPoints() == 3:
        #from m: http://math.okstate.edu/people/wrightd/INDRA/MobiusonCircles/node4.html
        p0, p1, p2 = points[0][0]+points[0][1]*1j, points[1][0]+points[1][1]*1j, points[2][0]-points[2][1]*1j
        w = p2-p0
        w /= p1-p0
        c = (p0-p1)*(w-abs(w)**2)/2j/w.imag-p0
        center = [c.real, c.imag]

        ang0=getAngle(center,points[0])
        ang1=getAngle(center,points[1])
        ang2=getAngle(center,points[2])
        angDelta02 = (ang2-ang0)
        angDelta01 = (ang1-ang0)
        angDelta = angDelta02 if sign(angDelta02) == sign(angDelta01) else angDelta02-2*pi if angDelta02>0 else 2*pi+angDelta02

        r0 = distance(center,points[0])
        rDelta=0

    if nrPoints() == 2 and r:
        d=distance(points[0],points[1])
        dx=points[1][0]-points[0][0]
        dy=points[1][1]-points[1][0]
        xm=(points[0][0]+points[1][0])/2.
        ym=(points[0][1]+points[1][1])/2.
        u=sqrt(r**2-(d/2)**2)

        center=[xm-u*dy/d, ym+u*dx/d] if sol%2 == 0 else [xm+u*dy/d, ym-u*dx/d]
        sol = sol/2

    if nrPoints() == 2 and center:
        r0=distance(center, points[0])
        r1=distance(center, points[1])
        rDelta=(r1-r0)

        ang0=getAngle(center,points[0])
        ang1=getAngle(center,points[1])
        angDelta = (ang1-ang0)
        angDelta = angDelta if sol%2 == 0 else angDelta-2*pi if angDelta>0 else 2*pi+angDelta
        sol=sol/2

    if nrPoints() == 1 and len(angles) == 1:
        ang0 = getAngle(center,points[0])
        ang1 = toRad(angles[0])
        angDelta = ang1 if sol == 0 else ang1-ang0 if sol ==1 else 2*pi - (ang0-ang1)

        r0=distance(center,points[0])
        rDelta=0

    if angles and not angDelta:
        ang0 = toRad(angles[0])
        angDelta = toRad(angles[1]-angles[0])

    if r and not rDelta:
        if isCollection(r):
            r0=r[0]
            rDelta= (r[1]-r[0])
        else:
            r0=r
            rDelta= 0
        print r0,rDelta

    return createSegments()
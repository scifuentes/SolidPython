from solid import *

def object_move(self, v = None, x = 0, y = 0, z = 0):
    if v:
        return translate(v)(self)
    else :
        return translate([x,y,z])(self)
OpenSCADObject.move = object_move

def object_rot(self, v = None, x = 0, y = 0, z = 0):
    if v:
        return rotate(v)(self())
    else:
        return rotate([x,y,z])(self)
OpenSCADObject.rot = object_rot

def cubeSize(self):
    size = self.params['size']
    if isinstance(size, list):
        return size
    else:
        return [size, size, size]
objects.cube.getSize = cubeSize

def cylinderSize(self):
    h = self.params['h']
    if self.params['d']:
        d = self.params['d']
    elif self.params['d1']:
        d = self.params['d1']
    elif self.params['r']:
        d = 2 * self.params['r']
    elif self.params['r1']:
        d = 2 * self.params['r1']
    return [d, d, h]
objects.cylinder.getSize = cylinderSize

def sphereSize(self):
    if self.parems['d']:
        d = self.self.params['d']
    elif self.params['r']:
        d = 2 * self.self.params['r']
    return [d, d, d]
objects.sphere.getSize = sphereSize

objects.cube.relativeCenter = [.5,.5,.5]
objects.cylinder.relativeCenter = [0,0,.5]
objects.sphere.relativeCenter = [0,0,0]

def object_center(self, axis='xyz'):
    toCenter = [s*c for s,c in zip(self.getSize(), self.relativeCenter)]
    m = [0, 0, 0]
    if 'x' in axis:
        m[0] = -toCenter[0]
    if 'y' in axis:
        m[1] = -toCenter[1]
    if 'z' in axis:
        m[2] = -toCenter[2]

    return translate(m)(self)

OpenSCADObject.center = object_center

def object_align(self, a1='center',a2='center',a3='center'):
    alignPos = {}
    alignPos['center']=[0,0,0]
    alignPos['top']=[0,0,-.5]
    alignPos['bottom']=[0,0,.5]
    alignPos['right']=[-.5,0,0]
    alignPos['left']=[.5,0,0]
    alignPos['front']=[0,-.5,0]
    alignPos['back']=[0,.5,0]

    rAlign = [ax+ay+az for ax,ay,az in zip(alignPos[a1], alignPos[a2], alignPos[a3])]
    align = [a*s for a,s in zip(rAlign, self.getSize())]
    return self.center().translate(align)
OpenSCADObject.align = object_align

def object_mirrorCopy(self, axis='xyz' ): #also allows a vector
    if isinstance(axis, str):
        v = [0,0,0]
        if 'x' in axis:
            v[0]=1
        if 'y' in axis:
            v[1]=1
        if 'z' in axis:
            v[3]=1
    else:
        v=axis

    return self + self.copy().mirror(v)

OpenSCADObject.mirrorCopy = object_mirrorCopy

#==========

if __name__ == '__main__':

    d = sphere(r=5).center().move(x=10).move(y=5)

    with open('solidPython.scad','w') as f:
        f.write(scad_render(d))

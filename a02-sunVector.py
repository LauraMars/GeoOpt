import Rhino.Geometry as rg
import math

#create a sun vector

#1. create a Sphere at point (0,0,0) with radius 1 and output it to a
#output the sphere to a

origin= rg.Point3d(0,0,0)
sphere= rg.Sphere(origin,1.0)
a = sphere


#2. evaluate a point in the sphere using rg.Sphere.PointAt() at coordintes x and y
#the point should only be on the upper half of the sphere (upper hemisphere)
#the angles are in radians, so you might want to use math.pi for this
#output the point to b

a = rg.Sphere.ToNurbsSurface(a)
domain = rg.Surface.SetDomain(a, 0, rg.Interval(0,1))
print(domain)

point=rg.Surface.PointAt(a,x,y)

b = point



#create a vector from the origin  and reverse the vector
#keep in mind that Reverse affects the original vector
#output the vector to c

vec1= rg.Vector3d(origin)
vec2= rg.Vector3d(b)
vecO=  rg.Vector3d.Add(vec1,vec2)

vec= rg.Vector3d.Negate(vecO)

c = vec

"""Provides a scripting component.
    Inputs:
        m: a mesh
        s: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        """
        

import Rhino.Geometry as rg
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import math
import ghpythonlib.components as ghc


#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a

meshFaces=[]
faces= len(m.Faces)
for j in range(faces):
    mesh= m.FaceNormals[j]
    vector= rg.Vector3d(mesh)
    vector_reverse= vector.Negate(vector)
    meshFaces.append(vector_reverse)

a=meshFaces
print(a)




#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b


centers = []

for i in range(faces):
    center = m.Faces.GetFaceCenter(i)
    centers.append(center)

b = centers



#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

angleList=[]

for i in range(faces):
    angle= rg.Vector3d.VectorAngle(a[i],s)
    angleList.append(angle)

c = angleList




#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d



exploded=[]

copy_mesh= rg.Mesh.Duplicate(m)

copy_m= len(copy_mesh.Faces)

#print(copy_m)
#print(copy_mesh)

for i in range(copy_m):
    extract_faces= copy_mesh.Faces.ExtractFaces([0])
    exploded.append(extract_faces)


d = exploded

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!


# I am trying to move the mesh faces in relation to the sun vector and scale them in relation to the angle value 

move_point=[]

for i in centers:
    point_move=[]
    newPt= i - s
    point_move.append(newPt)
    move_point.append(point_move)

e = th.list_to_tree(move_point)


#Move vertices of mesh in relation to the sun vector
V_mesh=m.Vertices


print(V_mesh)
print(type(V_mesh))
print(len(V_mesh))


AllVert=[]
for i in V_mesh:
    vertix=[]
    v= rg.Point3d(i)
    move_pt= v - s
    vertix.append(move_pt)
    AllVert.append(vertix)

f = th.list_to_tree(AllVert)


#move face
"""
Move_faces=[]
for j in exploded:
    face_move=[]

"""
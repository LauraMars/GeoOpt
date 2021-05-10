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
#SUPPORT WITH DAI

#0 Remap angle values to control the range of the scale
remaped_angles=[]
min_offset=min_off
max_offset=max_off #reverse
for i in angleList:
    remaped = ( (i - min(angleList)) / (max(angleList) - min(angleList)) ) * (max_offset - min_offset) + min_offset
    remaped_angles.append(remaped)


#1.move faces in relation to sun vector
moved_faces=[]

for i in range(len(exploded)):
    face=rg.Mesh.Duplicate(exploded[i])
    vector = s+rg.Vector3d(a[i])/200
    moved=rg.Mesh.Transform(face,rg.Transform.Translation(-vector/8)) #gives true/false
    moved_faces.append(face)



#2.scale faces in relation to angle value
#2.1 Get faces outlines
moved_outlines=[]
for i in moved_faces:
    FaceOutlines=rg.Mesh.GetNakedEdges(i)
    moved_outlines.append(FaceOutlines)


#2.2 Convert to curves and Join
joined_moved=[]
for i in range(len(moved_outlines)):
    curves=[]
    for j in range(len(moved_outlines[i])):
        #convert to nurbs curve
        curve=rg.Polyline.ToNurbsCurve(moved_outlines[i][j])
        curves.append(curve)
    joined_curves=rg.NurbsCurve.JoinCurves(curves)[0]
    joined_moved.append(joined_curves)


#2.3 Offset joined outlines
offset_outlines=[]
for i in range(len(joined_moved)):
    #convert mesh to surface
    face_points=rg.Mesh.Vertices.GetValue(moved_faces[i])
    surface=rg.NurbsSurface.CreateFromPoints([rg.Point3d(pt) for pt in face_points],2,2,2,2)#list_comprehension 
    offseted=rg.Curve.OffsetOnSurface(joined_moved[i],surface,remaped_angles[i],.001)[0]
    offset_outlines.append(offseted)
#########################
outlines=[]
for i in exploded:
    FaceOutlines=rg.Mesh.GetNakedEdges(i)
    outlines.append(FaceOutlines)
joined=[]
for i in range(len(outlines)):
    curves=[]
    for j in range(len(outlines[i])):
        #convert to nurbs curve
        curve=rg.Polyline.ToNurbsCurve(outlines[i][j])
        curves.append(curve)
    joined_curves=rg.NurbsCurve.JoinCurves(curves)[0]
    joined.append(joined_curves)


#2.4 Loft 
panels_with_openings=[]
for i in range(len(offset_outlines)):
    curves_list=[offset_outlines[i],joined[i]]
    lofted=rg.Brep.CreateFromLoft(curves_list,rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType.Normal,False)[0]
    panels_with_openings.append(lofted)









"""
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



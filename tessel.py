import numpy as np
from matrix import matrix
import statistics
from cameraMatrix import cameraMatrix
class tessel:

    def __init__(self,objectTuple,camera,light):
        self.__faceList = [] #List of faces with attributes
        EPSILON = 0.001

        #Transform light position into viewing coordinates
        facePoints=0
        for object in objectTuple:
            u = object.getURange()[0]
            while u + object.getUVDelta()[0] < object.getURange()[1]  + EPSILON:
                v = object.getVRange()[0]
                while v + object.getUVDelta()[1] < object.getVRange()[1] + EPSILON:
                  #Collect surface points and transform them into viewing coordinates
                  p1 = camera.worldToViewingCoordinates(object.getT()*object.getPoint(u,v))
                  p2 = camera.worldToViewingCoordinates(object.getT()*object.getPoint(u+object.getUVDelta()[0],v))
                  p3 = camera.worldToViewingCoordinates(object.getT()*object.getPoint(u+object.getUVDelta()[0],v+object.getUVDelta()[1]))
                  p4 = camera.worldToViewingCoordinates(object.getT()*object.getPoint(u,v+object.getUVDelta()[1]))
                  facePoints= (p1,p2,p3,p4)

		    #Compute vector elements necessary for face shading
                  Lv = light.getPosition()
                  C = self.__centroid(facePoints) #Find centroid point of face
                  N = self.__vectorNormal(facePoints) #Find normal vector to face
                  S = self.__vectorToLightSource(Lv,C) #Find vector to light source
                  R = self.__vectorSpecular(S,N) #Find specular reflection vector
                  V = self.__vectorToCentroid(C) #Find vector from surface centroid to origin of viewing coordinates

		    #If surface is not a back face

                    	#Compute face shading 

                    	#Transform 3D points expressed in viewing coordinates into 2D pixel coordinates

		    	#Add the surface to the face list. Each list element is composed of the following items:
		        #[depth of the face centroid point (its Z coordinate), list of face points in pixel coordinates, face shading]

                  v += object.getUVDelta()[1]
                u += object.getUVDelta()[0]
    #Returns the column matrix containing the face centroid point
    def __centroid(self,facePoints):
      p1, p2,p3,p4 = facePoints
      cm = matrix(np.zeros((1,4)))
      x = statistics.mean([p1.get(0,0),p2.get(0,0),p3.get(0,0),p4.get(0,0)])
      y = statistics.mean([p1.get(1,0),p2.get(1,0),p3.get(1,0),p4.get(1,0)])
      z = statistics.mean([p1.get(2,0),p2.get(2,0),p3.get(2,0),p4.get(2,0)])
      cm.set(0,0,x)
      cm.set(0,1,y)
      cm.set(0,2,z)
      cm.set(0,3,0)
      return cm
    
    #Returns the column matrix containing the normal vector to the face.
    def __vectorNormal(self,facePoints):
      p1, p2,p3,p4 = facePoints
      vN = matrix(np.zeros((1,4)))
      v1 = p3-p1
      v2 = p4-p2
      v1 = v1.removeRow(3).transpose()
      v2 = v2.removeRow(3).transpose()
      normal =v1.crossProduct(v2) 
      return normal.insertColumn(3,0.0)
    
    #Returns the column matrix containing the vector from the centroid to the light source
    def __vectorToLightSource(self,L,C):
      l = L.transpose()
      return l-C
    
    #Returns the column matrix containing the vector of specular reflection
    def __vectorSpecular(self,S,N):
      n = N.transpose()
      temp = S *n
      vS = -S+ 2* (S * N)/ pow(N.determinant(),2) * N
      return 0
    
    #Returns the column matrix containing the vector from the face centroid point to the origin of the viewing coordinates
    def __vectorToCentroid(self,C):
      return 0

    def getFaceList(self): #Returns the face list ready for drawing
        return self.__faceList
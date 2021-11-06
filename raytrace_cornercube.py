import mpl_toolkits.mplot3d as a3d
import matplotlib.pyplot as plt

with open("cornercube.stl.txt") as stlfile:
    file_lines = stlfile.readlines()
def dotprod(vec1,vec2):
    total = 0
    for i in range(len(vec1)):
        total += vec1[i]*vec2[i]
    return total
def normalize(vector):
    magnitude = dotprod(vector,vector)**0.5
    return [v / magnitude for v in vector]
class Solid():
    def __init__(self):
        self.facets = []
        self.vertices = []
    def add_facet(self,facet):
        self.facets.append(facet)
class Facet():
    def __init__(self,normalvec):
        self.vertices = []
        self.normal = normalize(normalvec)
    def add_vertex(self,vert):
        self.vertices.append(vert)
    def __str__(self):
        return ";".join([str(v) for v in self.vertices])
class Vertex():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def toList(self):
        return [self.x,self.y,self.z]
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"
    def __getitem__(self,key):
        return [self.x,self.y,self.z][key]
currentBody = None
for line in file_lines:
    if "endsolid" in line:
        pass
    elif "solid" in line:
        currentBody = Solid()
    elif "facet normal" in line:
        _,_,normalx,normaly,normalz = line.split()
        currentFacet = Facet([float(normalx),float(normaly),float(normalz)])
    elif "outer loop" in line:
        pass
    elif "vertex" in line:
        _,x,y,z = line.split()
        newvert = Vertex(float(x),float(y),float(z))
        if newvert not in currentBody.vertices:
            currentBody.vertices.append(newvert)                
        currentFacet.add_vertex(newvert)
    elif "endloop" in line:
        pass
    elif "endfacet" in line:
        currentBody.add_facet(currentFacet)
class Ray():
    #xyz is where ray starts from, v1,v2,v3 is a normalized vector of departure
    def __init__(self,x,y,z,v1,v2,v3):
        self.o1 = x
        self.o2 = y
        self.o3 = z
        self.origin = [x,y,z]
        self.d1 = v1
        self.d2 = v2
        self.d3 = v3
        self.direction = normalize([v1,v2,v3])
    #https://math.stackexchange.com/questions/100439/determine-where-a-vector-will-intersect-a-plane
    def intersect_site(self,chosen_facet):
        normal = chosen_facet.normal
        if dotprod(normal,self.direction) == 0:
            return None
        A = chosen_facet.vertices[0]
        numerator = normal[0] *(A[0]-self.o1) + normal[1] *(A[1]-self.o2) + normal[2] *(A[2]-self.o3)
        denominator = dotprod(self.direction,normal)
        t = numerator / denominator
        intersect = [self.o1 + self.d1 * t,self.o2 + self.d2 * t,self.o3 + self.d3 * t]
        return t,intersect,chosen_facet
    #Get the resulting vector that comes from this vector bouncing off a facet
    def resultant(self,chosen_facet):
        
        new_origin = self.intersect_site(chosen_facet)[1]
        #If our intersect is the top of the cube (exiting), we're done. Make a new vector departing.
        if all(v[2] == 35 for v in chosen_facet.vertices):
            return Ray(*new_origin,*self.direction)
        
        scaled_normal = [2 * (dotprod(self.direction,chosen_facet.normal)) * x for x in chosen_facet.normal]
        new_direct = [0,0,0]
        for i in range(len(self.direction)):
            new_direct[i] = self.direction[i] - scaled_normal[i]
        return Ray(*new_origin,*new_direct)
    #Gives a new vector, of this one after bouncing off some facet of body
    def reflect(self,body):
        intersects = [self.intersect_site(facet) for facet in body.facets]
        viable_intersects = [i for i in intersects if i != None and i[0] > 1e-10] #only get forward results
        
        shortest_intersects = sorted(viable_intersects, key=lambda x: x[0])
        out_vec = self.resultant(shortest_intersects[0][2])
        return out_vec



#Uncomment this to run a test of over 89,000 vertical vectors and confirm they all come out vertical

##raystartxvals = [x / 10 for x in range(-149,150)]
##raystartyvals = [y / 10 for y in range(-149,150)]
##vectorstested = 0
##for xval in raystartxvals:
##    for yval in raystartyvals:
##        vectorstested += 1
##        rayStart = xval,yval,35
##        currentRay = Ray(*rayStart,0,0,-1)
##        ray_bounces = [rayStart]
##        keepRunning = True
##        while(keepRunning):
##            olddirection = currentRay.direction
##            currentRay = currentRay.reflect(currentBody)
##            if olddirection == currentRay.direction:
##                keepRunning = False
##            ray_bounces.append(currentRay.origin)
##        #Judge if ray came out vertical
##        if not dotprod(currentRay.direction,[0,0,1]) > (1 - 1e5):
##            print("FAIL!")
##print("Tested " + str(vectorstested) + "Vectors!")

rayStart = -5,10,35
currentRay = Ray(*rayStart,0,0,-1)
ray_bounces = [rayStart]
keepRunning = True
while(keepRunning):
    olddirection = currentRay.direction
    currentRay = currentRay.reflect(currentBody)
    if olddirection == currentRay.direction:
        keepRunning = False
    ray_bounces.append(currentRay.origin)
    
ax = a3d.Axes3D(plt.figure())
ray = ax.plot3D(*list(zip(*ray_bounces)),'r')

for facet in currentBody.facets:
    verts = [v.toList() for v in facet.vertices]
    triangle = ax.plot3D(*list(zip(*verts)),'k')

ax.set_xlim(-50,50)
ax.set_ylim(-50,50)
ax.set_zlim(-50,50)
plt.show()

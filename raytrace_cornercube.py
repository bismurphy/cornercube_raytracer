with open("cornercube.stl.txt") as stlfile:
    file_lines = stlfile.readlines()
def dotprod(vec1,vec2):
    total = 0
    for i in range(len(vec1)):
        total += vec1[i]*vec2[i]
    return total
class Solid():
    def __init__(self):
        self.facets = []
        self.vertices = []
    def add_facet(self,facet):
        self.facets.append(facet)
class Facet():
    def __init__(self,normalvec):
        self.vertices = []
        self.normal = normalvec
    def add_vertex(self,vert):
        self.vertices.append(vert)
    def __str__(self):
        return ";".join([str(v) for v in self.vertices])
class Vertex():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
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
        self.d1 = v1
        self.d2 = v2
        self.d3 = v3
    #https://math.stackexchange.com/questions/100439/determine-where-a-vector-will-intersect-a-plane
    def intersect_site(self,chosen_facet):
        normal = chosen_facet.normal
        A = chosen_facet.vertices[0]
        numerator = normal[0] *(A[0]-self.o1) + normal[1] *(A[1]-self.o2) + normal[2] *(A[2]-self.o3)
        denominator = self.d1 + self.d2 + self.d3
        t = numerator / denominator
        intersect = [self.o1 + self.d1 * t,self.o2 + self.d2 * t,self.o3 + self.d3 * t]
        return intersect

testRay = Ray(5,5,35,0,0,-1)
reflectPoint = testRay.intersect_site(currentBody.facets[18])

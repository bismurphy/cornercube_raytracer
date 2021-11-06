import numpy as np
import matplotlib.pyplot as plt

######Load STL######
def load_stl(filename):
    with open(filename) as stlfile:
        file_lines = stlfile.readlines()
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
        def asarray(self):
            return np.array([self.x,self.y,self.z])
        def toList(self):
            return [self.x,self.y,self.z]
        def __eq__(self,other):
            return self.x == other.x and self.y == other.y and self.z == other.z
        def __repr__(self):
            return f"({self.x},{self.y},{self.z})"
        def __getitem__(self,key):
            return [self.x,self.y,self.z][key]
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
    return currentBody
        

#Given a point which is on the plane of a triangle, determine if it's inside the triangle.
def is_within_triangle(point,triangle):
    #Take each pair of vertices of the triangle. The extended line between them divides the plane in two.
    #If the point of interest is on the same side of the line as the third vertex, it's on the proper side
    #If, for all pairs of points, it's on the proper side of the line, it's in the triangle.
    #To tell if it's on the same side as the third vertex, get midpoint of the line, and then draw two
    #vectors: One from the point to the midpoint, and one from third vertex to the midpoint.
    #If dot product of those vectors is positive, they are on same side of the line.
    for i in range(3):
        vertex_1 = triangle.vertices[i].asarray()
        vertex_2 = triangle.vertices[(i+1)%3].asarray()
        vertex_3 = triangle.vertices[(i+2)%3].asarray()
        midpoint = (vertex_1 + vertex_2) / 2
        vec_from_3_to_midpoint = midpoint - vertex_3
        vec_from_p_to_midpoint = point - vertex_3
        if dotprod(vec_from_p_to_midpoint,vec_from_3_to_midpoint) < 0:
            return False
    return True
def normalize(vector):
    magnitude = dotprod(vector,vector)**0.5
    return [v / magnitude for v in vector]
def dotprod(vec1,vec2):
    total = 0
    for i in range(len(vec1)):
        total += vec1[i]*vec2[i]
    return total
#Convert those angular directions to rays
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
    
    def body_intersect(self,body):
        intersects = [self.intersect_site(facet) for facet in body.facets]
        viable_intersects = [i for i in intersects if i != None and i[0] > 1e-10] #only get forward results
        
        shortest_intersects = sorted(viable_intersects, key=lambda x: x[0])\
        #Go through shortest intersects until you find the first one which is within the triangle.
        for intersection in shortest_intersects:
            _,intersection_location,intersected_facet = intersection
            if is_within_triangle(intersection_location, intersected_facet):
                return True
        
camera_pos = 0,-50,50

light_pos = 10,40,60

fov_x = 90
fov_y = 90

resolution_x = 500
resolution_y = 500

x_directions = np.linspace(-fov_x/2,fov_x/2,resolution_x)[:-1]
y_directions = np.linspace(-fov_y/2,fov_y/2,resolution_y)[:-1]
out_array = np.zeros(shape=(resolution_x,resolution_y))
rendered_object = load_stl("cornercube.stl")        
for x in x_directions:
    for y in y_directions:
        view_ray = Ray(*camera_pos,x,0,y)
        xpixel = int((x/fov_x + 0.5) * resolution_x )
        ypixel = int((y/fov_y + 0.5) * resolution_y )

        out_array[xpixel,ypixel] = view_ray.body_intersect(rendered_object)
plt.imshow(out_array)
plt.show()
print("done")

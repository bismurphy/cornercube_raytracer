
difference(){
    translate([0,0,17.5])
    cube([35,35,35],center=true);
    translate([0,0,45])
    //This builds the "obelisk" that will carve out the cube
    difference(){
        rotate(90-atan(1/sqrt(2)),[1,-1,0])
        cube(50,center=true);
        //a tube to cut through the tilted cube
        difference(){
            cube([100,100,100],center=true);
            cube([30,30,100],center=true);
        }
    }
}
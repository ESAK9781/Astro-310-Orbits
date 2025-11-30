Explanation.md

Author: Elijah Sakamoto

Documentation: None

# A Brief Explanation of Some More Complicated Parts of the Software

## What is this?

I got bored one weekend (after I had already turned in MS I) and started thinking about how the process of choosing COEs to cover the target points could be automated with software. The authorized resources for this project include computational tools, and python is a computational tool. I fully intended to use these python scripts to generate full constellations for future milestones, but the highly-guided design process required in the submission template for MS II made this impossible. Instead, I plan to use some of the codebase I wrote for this software as a tool to write another software which is more guided along the path of the MS II template.

## Orbital Simulation Explanation
All of the logic for simulating orbits using the COEs is included in the Orbit.py class, which uses the COEs and formulas learned in class to handle orbit-related computations. All of these formulas can be viewed under the corresponding methods of the Orbit class in the Orbit.py file unless otherwise indicated.

### Instantiation
Whenever an Orbit is instantiated, it first performs some checks on the COEs used to create it. Angles that must stay on a specific range, such as inclination (0-180), are looped across that range if they are not already on it. I.E, a true anomaly of 361 goes to 1, and a true anomaly of -1 goes to 359. 

Additionally, special orbits, such as a circular one, are avoided by shifting these COEs ever so slightly off of their "special" value. An eccentricity of zero, for example, becomes something near 0.00001. This avoids having to program logic for these special cases with minimal impact on the functionality and accuracy.

Finally, several important variables that depend on the COEs are calculated using the exact formulas on the formula sheet. Among these are period and n.

### Getting Position Based on True Anomaly
This is likely the most complicated part of the Orbit class. Simulating COEs at a future time is easy, we covered the process in class (v->E->M->M->E->v), but this does not help us with checking for coverage of the points. Coverage of the points, you see, depends on actual cartesian coordinates, which we never learned in class how to compute from the COEs.

Figuring this out took several hours with a Whiz wheel. I ended up using rotation matrices I had learned in my Linear Algebra class. At first I ligned up all the wheels such that the angles are all zeroed out. The sattelite's (sat's) position on the whiz wheel absent consideration of any other COEs is <r*cos(v), r*sin(v), 0>, where r is the current distance from the center of the Earth as computed using the formula on the formula sheet. By applying the following transformations on this point, we can factor in the other COEs to obtain the final coordinates of the sat in three dimensional space:
-    Rotate about the z axis by w degrees, where w is the argument of perigee
-    Rotate about the x axis by i degrees, where i is the inclination
-    Rotate about the z axis by raan degrees, where raan is the right ascention of the ascending node

These rotations were derived by manipulating the whiz wheel, and the matrices for these rotations were multiplied together in Wolfram Alpha (a computation tool for matrices) in order to get one comprehensive matrix that does all the transformations at once. For additional explanation, search up "transformation matrices."

### Getting Position Based on Time
With the previous method implemented, this problem becomes trivial. We can use the method taught in class to get true anomaly at time=t, then convert it into real-world cartesian coordinates using the methods described above.

To summarize these methods, we first convert true anomaly from degrees into radians. Then, we convert this v initial into E initial using the formula from the formula sheet listed under "Orbit Prediction" and complete a half-plane check to ensure we got the right value of E initial. Next, we convert E initial into M initial using a formula from the same section. Convert this M value into the final M value by adding n(TOF) and looping the resulting value on the range (0,2pi), get E final by iterating M=E-e*sin(E), and quickly get the final true anomaly with the formula from the formula sheet. One final half-plane check, and we have the true anomaly at time=t.

Use the previously written method to convert this true anomaly to real-world coordinates, and we have a position that can be used for line of sight computations to estimate coverage of the points.

### Checking Coverage
This is a more complicated problem than it initially appears. What I ended up doing was calculating the combined period of the entire constellation. This is the time it takes for the entire system to return to its original state again, and can be calculated by multiplying Earth's period (24 hours) with the three satellites' periods. This product has each of the other periods as factors, thus each object is in its original state again at that time. 

From here we randomly sample some number (~100, but can be increased for greater accuracy at the cost of performance) of timestamps between t=0 and t=combined_period. 

Now, we just need to create a method of checking whether, at a given point in time, at least one satellite is within camera vision range (computed by (aperture * MIN_RESOLUTION) / (2.44 * min_wavelength) / 1000)). 

To do this, we first need to get the coordinates of each of the satellites and each of the points in real world coordinates. The satellites are easy, we already created methods for that in Orbit.py. To get the positions of each of the points, simple geometry intuitively yields the following steps:
-   Place each of the points at <~Earth_Radius, 0, 0>
-   Rotate each of the points about the y-axis by their latitude (just like inclination)
-   Rotate each of the points about the z-axis by -18.6 degrees (initial earth rotation determined experimentally in BORG by setting t=0, putting a satellite at arg-perigee=0 and v=0, and hovering over its ground track to get its longitude)
-   Rotate each of the points about the z-axis by their longitude (just like arg-perigee)
-   Rotate each of the points about the z-axis by t*(360/1day) to simulate the rotation of the Earth

Now that we have the locations of the satellites and points in real coordinates, we can use a ray-marching algorithm to determine whether any of the satellites actually see the points. First, we set up a scene with a sphere at <0,0,0> (to simulate the Earth) and a single satellite at its position, and a single point at its position. Then, we start at the satellite, calculate the minimum distance to any collideable object (i.e. the sphere or the terminal point) using the distance formula, then move that distance along the direction from the satellite to the point. Repeat this until the minimum distance reaches zero, and check whether we are at the target point. If not, we collided somewhere along the way and there is no clear line of sight. Finally, check if the distance between those two points is greater than the camera vision range, then it is also out of sight. Otherwise, we assume it must be in sight because there is line of sight and we are in range. For additional details on this portion, search details on the raymarching algorithm.

If we repeat this for every combination of satellite and target point, and determine what percentage of the points have at least one satellite that can see them. If we average the percentages from each time sample, we get a pretty good estimation of the percent coverage for the whole constellation. All formulas and calculations for this portion of the computations can be found in the Scoring.py file. Sufficient comments are provided that they should make sense.

## Note:
All of the code for this project is included in the submission, including an extreme amount of comments to make the formulas and processes used clear to even non-programmers. Additionally, some computations are grouped together with explanations through a Jupyter notebook, which is a python execution environment that allows formatted comments written in markdown. MSII_Base_Orbit_Determination.ipynb is where I actually calculated and reasoned my way through the orbit design we used. MSII.ipynb is where I went through the checklist. Both of these are essential reads to understand this program.
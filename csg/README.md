
CSG allows to create complex shapes using geometrical primitives

Let's start with spheres only to simpliofy things (only one ray-intersection, lighting better visible without rotation)
<br/><br/>

# Step 1. Ray-sphere intersections

Keywords: _ray-sphere intersection_, _ray casting_

The most fundamental thing in this project will be finding an intersection between a ray and a sphere. There are two main approaches - analytical and geometric. They are both explained quite well e.g. on [www.scratchapixel.com](https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection.html).

Basically, you want your function to take a ray (origin and direction) and a sphere (position and radius), and return 2 numbers - the distance between the ray origin and the two intersection points. You also need some indicator whether the ray does actually intersect the sphere. In theory you may also have a single intersection point when the ray is tangent to the sphere, but in practice it shouldn't matter that much. It might be the easiest to treat it as a "no intersection".

Now we are able to create a basic ray caster. The idea is simple - for every screen pixel cast a ray, and if it intersects the sphere - calculate the resulting color and draw a pixel. What is the resulting color? To start, you can draw a white pixel when there is an intersection, and a black one if there isn't. This should result in a white circle on your sceen. If you don't, then you may want to check your intersection function, see if the distance between rays for neighboring pixels is not too small or too big, and that your ray and sphere are properly oriented (e.g. the ray is not pointing away from the sphere).

Having this, we can do something more interesting, and make the color a function of the distance to the intersection point. Typically you would want smaller distances yield brighter pixels.

Note that ray casting is pretty computationally intensive. To facilitate working on the next steps I suggest to add some optimizations:

* use bigger "pixel" size: split the screen into, say, 4x4 regions. Cast a single ray per region, and fill the whole region with a calculated color. Add an option to dynamically increase/decrease "pixel" size.

* only perform raycasting when the scene changes

Finally, you may want to add zoom in/out feature.

<details>
  <summary>Hint</summary>
  The bigger the distance between the neighboring rays, the smaller the sphere will look.
</details>

<br/><br/>

# Step 2. Lightning

Keywords: _ambient light_, _directional light_, _diffuse lighting_, _sphere normal vector_, _shading models_, _Phong model_

Now we will add some lightning, so that our scene looks more realistic. Lightning can be a bit confusing at the beginning, as there are many different aspects: different types of lights (ambient, directional, point, ...), and shading models () and components (ambient, diffuse, specular). I suggest to use a single ambient and directional lights, and only ambient and diffuse components. While you can also add specular highlights now, it might be easier to see whether they look as expected later on, when we will have multiple objects and option to rotate the scene.

In general, you will need a normal (vector) to the sphere at the intersection point, and the vector pointing in the direction of the light. Fortunately for us, they are both super easy to calculate.

<br/><br/>

# Step 3. Scene loading

Let's now add scene loading from a file. You want to be able to define multiple lights (of every type) and multiple spheres (with different positions, radii, and colors). You will also need to adjust your ray casting routine to find intersections with all the spheres in the scene.

<br/><br/>

# Step 4. CSG interval arithmetic

The next 2 steps constitute a core (and the most interesting part) of this project, so buckle up!

In CSG one first finds intersections (represented as intervals) with all the geometrical primitives in the scene, and then goes up the tree and combine them together based on a given node binary operation. Note that this interval arithmetic might be slightly tricky to get right. For example, union of intervals $(2, 4)$ and $(3, 5)$ is not $(2, 5)$ (as it would be in the "classical interval arithmetic"), but a set $`{(2, 4), (3, 5)}`$. Additionaly, in order to properly color the object you will need to calculate the normals, which means that you will need to keep track of the spheres corresponding to the interval ends (and notice that the ends of a single interval may correspond to different spheres).

I suggest to take pen and paper and draw some circles (together with the corresponding binary operations) and rays. Now consider the starting intervals, and what should be the result of different combinations of operations. Union and intersection should be relatively easy to figure out, so you may want to start with them.

I would also suggest to implement this as a library and add a lot of unit tests for different cases. It is really easy make a mistake here!

<details>
  <summary>Hint (subtraction)</summary>
  When subtracting two sets of intervals you may notice some weird issues, for example ending up with multiple copies of the same interval. Would it be simpler if you would consider the inverse of the second set?
</details>

<details>
  <summary>Solution (subtraction)</summary>
  $A - B$ is the same as $A intersection inv(B)$.
</details>

<br/><br/>

# Step 5. Raycasting CSG objects

We are now ready to 

First, you need to add a tree definition to your scene file. Internal nodes will specify the binary operation, and leaves - a single geometrical primitive. As you already have a list of primitives defined, you can simply use their indices when defining a tree. (I suggest to use as simple format for defining the tree as possible, at least for now. Later on we will work on a more efficient method.)

Now, for every casted ray you will need to find intersections with all the primitives. Then you can climb up the tree, at every node combining intervals from the child nodes using the specified operation. Once you get to the root you have a final set of intervals, so you only need to find the closest interval. It will give you the distance to the closest intersection, and the index of the corresponding primitive - which is all you need!

<br/><br/>

# Step 6. Rotation

In this step we will add controls for rotating our scene. There is a number of ways to achieve this. Probably the most intuitive one is to rotate the objects' positions. While this would work well for spheres, it can be problematic later on, when we will add more shapes. In particular, cuboids are often defined to be axis aligned (which simplifies their representation, as you only need their center and side lengths), and when you rotate them - well, they are no longer axis aligned (but of course nothing can stop from trying it out, it may give you some nice results). You can also work with oriented cuboids, but the math to find the intersection becomes more complex.

So, instead of rotating the objects you may choose to rotate the ray itself. One way would be to have the ray origin orbit around your object, and change its direction to always point towards the world coordinate system origin. Another method would be to rotate not the ray origin, but its direction. For this you would keep a local coordinate system (i.e. 3 vectors, pointing up, right, and forward) representing ray orientation (and having the orientation you can easily calculate the desired ray origin position). Disadvantage of these methods is that, depending on your exact implementation, it may make controling the rotation a bit counterintuitive, and you may get a gimbal lock.

Once you have the rotation working it will be much easier to position your object for a nice screenshot, and to test whether the lightning works as expected. And, of course, you will be able to create a nice animation!

<br/><br/>

# Step 7. Cubes

Keywords: _Axis-aligned bounding box (AABB)_, _Oriented bounding box (OBB)_,

As a next step we will add support for another geometric primitives - cuboids. This will let you create much more interesting objects.

Note that in computer graphics nomenclature cuboids are often referred to as bounding boxes. Many algorithms (for example ray-cube intersection) are designed for the specific case when the cuboid sides are aligned with the world coordinate system axes (axis-aligned bounding box, AABB), as opposed to cuboids in general (oriented bounding box, OBB).

Your first step should be to write a ray-cuboid intersection function. The CSG tree calculations remain mostly unchanged. Finally, you will need to calculate proper normals at the intersection point. While this is easy for spheres (you only need the intersection point and the sphere's origin), for cuboids you need to know which face the ray intersected.

<br/><br/>

# Step 8. Optimizing CSG tree definition

Let's now take a step back and look at your CSG tree definition. Chance is that you used a human friendly like JSON. While this is fine for simple scenes, it may quickly become unwieldy if you want to add more and more objects due to its verbosity. Thus, it might be practical to employ a more compact format. I suggest a recursive definition, in which a node is represented either by index of the geometric primitive (for leave nodes), or by the sign of the operation (e.g. +, -, *), followed by the definition of the left and right subtrees (for the internal nodes). For example, $+ 2 * 0 1$ would represent a union of primitive 2 with the intersection of primitives 0 and 1. You can also use some other existing notation (for example Reverse Polish notation), or try to come up with your own.

In either case, being able to define the scene quickly and quickly rearrange the tree if needed will make experimenting much easier.

# Next steps:

That's it! We have a fully functioning (even if simple) CSG raycaster. Here are some ideas for the next steps:
* add other geometric primitives. This will allow you to generate even more interesting objects. A very useful list of ray-intersection related resources can be found [here](https://www.realtimerendering.com/intersections.html),
* what about rendering a Sierpiński cube? You can create interesting things using only spheres and/or cubes. Use repeating patterns, randomness, or recursion to define your scene programmaticaly,
* optimize your program. Calculating intersections is very expensive, and you are doing a lot of that. You can speed up your program significantly by being smarter about which objects you run the calculations for. You could use general space partitioning methods (such as octree) to quickly filter out primitives which are too far from the ray. Another - and more interesting - approach is to create bounding boxes for your leave nodes, and use the CSG tree to calculate the boundig boxes for all internal nodes.
* make the program more responsive by increasing the resolution iteratively. In the first iteration, you cast a single ray, and use the resulting color to fill the whole screen. In the second iteration you use 4 rays, and fill 4 screen quadrants, then 16 rays, and so on, until you get to the resolution matching your screen's pixel size. This process should be immediately restarted e.g. when the object is rotated.
* depending on your implementation, you might be using orthogonal projection, in which all the rays are parallel to each other. For more realistic results you can switch to the perspecive projection, where all rays start from a single point.
* add reflections (right now we are doing ray _casting_, where we only look at the intersected object. By _tracing_ the reflected ray you can check which - if any - object would be visible in a reflection on the original object. Now you just need to combine the colors of the original and the "reflected" objects. This is a simple technique, but it really adds a lot of depth to the resulting images.
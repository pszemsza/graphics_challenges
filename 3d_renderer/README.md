We will create a simple 3D renderer using only one graphical function - drawing a single pixel.

# Step 1. Drawing a Line

Our first building block will be a function drawing a line between two given points: (x1, y1) and (x2, y2).

## Lines with small slopes (i.e. horizontalish)

To begin, let's focus on lines with gentle slopes, like from (10, 10) to (60, 20). For every X-coordinate between 10 and 60 we need to draw exactly one pixel. The challenge lies in determining the corresponding Y-coordinate.

<details>
  <summary>Hint 1</summary>
  How can we calculate the Y-coordinate at the midpoint between x1 and x2? What about 25% along the line? 37%? x%?
</details>

<details>
  <summary>Hint 2</summary>
  What's the average change in Y-coordinate as we move from x to x+1? Knowing this we should be able to calculate the Y-coordinate for each X.
</details>

<details>
  <summary>Hint 3</summary>
  You can calculate the Y coordinates analyticaly (i.e. calculate the value for every X individually), or do it iteratively. For example, if the average Y-coordinate change is 0.2, then every 5 horizontal pixels require a "shift" of one pixel upward.
</details>

At this stage, you should be able to get something like this:

![screenshot_000593](https://github.com/pszemsza/graphics_challenges/assets/65168262/8d3cbfff-5ba5-4264-bd73-d98471455694)


## Lines with large slopes (i.e. verticalish)

If you try to draw a line with very large slope it may work similarly to this:

![screenshot_000149](https://github.com/pszemsza/graphics_challenges/assets/65168262/e20edf0a-22cc-43d4-bd56-e10f9d3287f9)

What is happening? Well, we are drawing only one pixel per X, which is clearly not sufficient to make a continuous line. We need more pixels!

<details>
  <summary>Hint 1</summary>
  Consider flipping the labels on the X and Y axes.
</details>

<details>
  <summary>Hint 2</summary>
  Think about this as a drawing a line along the Y axis. Now, for each y in the (y1, y2) range  you will need exactly one pixel at the appropriate X coordinate.
</details>

## Edge cases

Once we have this working we should make sure that we handle all the edge cases. What if x1 == x2, or x2 < x1?
What should happen when any coordinate is smaller than 0?

Think about different edge cases and make sure you algorithm handles them correctly. Also, it might be helpful to draw a bunch of random or structured lines, e.g. like this:

![screenshot_000376](https://github.com/pszemsza/graphics_challenges/assets/65168262/10580700-33e7-4dbe-800d-fb5ca66e34b0)

You can also make the lines move around the screen or react to the mouse moves.

## Further reading

Line drawing is such a fundamental problem that a lot of research went into it. See e.g. the
[Line drawing algorithms](https://en.wikipedia.org/wiki/Line_drawing_algorithm) wikipedia page or just google around if you are interested.


# Step 2. Drawing an object

In this step we will create and render some objects as a wireframe. Typically objects in 3D graphics are represented as sets of triangles. Why triangles and not other polygons, like quads? Well, triangles are the simplest 2D polygons and they are always convex, which makes them the easiest to work with.

A good starting point is a basic object like a cube or tetrahedron. First, you will need a data structure to store the triangles representing your object. In the simplest approach you could just keep some sort of a list of individual triangles. But, you will quickly notice that every vertex of your object is shared by multiple triangles. Can we optimize this so that we don't have duplicated vertices?

<details>
  <summary>Hint</summary>
  Objects are commonly represented as lists of vertices and sets of vertex index triples. For example, you could represent a 2D square like this:

```
vertices = [[0, 0], [10, 0], [10, 10], [0, 10]]
indices = [[0, 1, 2], [0, 2, 3]]
```

</details>

To draw an object, iterate over all its triangles and draw them one by one. There is just one problem - our vertices are 3D points, and our screens (and the line drawing function that we created in Step 1) are 2D. Hence, we need a way to _project_ our 3D vertices into 2D pixels. This is usually done with a _projection matrix_, but for now I suggest to keep it simple and use a no-math-required approach: disregarding the third dimension, so that a point (x, y, z) will be represented by a pixel (x, y).

For example, drawing a cube yields a result like this (note that it looks like a square, not like a cube - this is because we ignored the 3rd dimension, effectively flattening the object and losing the perspective): 

![screenshot_000073](https://github.com/pszemsza/graphics_challenges/assets/65168262/6f6974ef-2e94-4db1-b6eb-8a2ba6cd4706)


# Step 3. Rotation and translation

Keywords: _vector_, _matrix_, _matrix-vector multiplication_, _matrix-matrix multiplication_, _matrix transformations_,  _rotation matrix_, _translation matrix_, _orthogonal projection matrix_

In this step we will add some dynamism to our scene by enabling object rotation. This requires basic algebraic operations like matrix-vector and matrix-matrix multiplications. There are probably some existing libraries for doing this in your language, but you are also free to implement them by yourself if you want to have a better understanding of what is going on.

The core principle involves representing vertices as 4D vectors and transforming them by multiplying with specialized 4x4 matrices, known as transformation matrices. Two common examples are translation and rotation matrices. For example, multipliyng a vector by a 30-degree Y-axis rotation matrix will give you a vector representing your point after, you guessed it, rotation by 30 degrees around the Y axis. 

Why do we need 4 dimensions, when our objects are 3D? In fact, 3x3 matrics would be sufficient for rotation (and some other operations, like scaling), but we need 4 dimensions to make a translation matrix. This may seem a bit counterintuitive at first - translation is a trivial operation, why would you need to use a matrix transformation for this? The reason is that by using matrices for all transformations we can easily chain transformations together. Because A(Bv) is the same as (AB)v, we can represent a series of transformations with a single matrix (it also makes the translation look much more serious).

Ok, let's rotate some objects! 
Transformations may be a bit tricky if you've never used them before, so I suggest to start with small steps. First you should modify your objects so that vertices are represented by 4D vectors. Then, create a rotation matrix for a small angle around the Z axis. Each animation frame, multiply all vertices of your object by the matrix, and draw your object as before. You should see your object rotating, albeit it might not be moving the way you would expect.

## Common pitfalls
- the rotation matrix rotates the points around the global coordinate system axis. Thus, if your object is located far away from your global coordinate system center it might be orbiting around the (0, 0) pixel (and at times disappear from the screen) rather than around the object's center, as you could expect. To make the object rotate around its center translate it to the center of the global coordinate system, rotate it, and then move it back.

- the order of transformations matters. Translation followed by a rotation usually yield a different result than a rotation followed by a translation. If your object's movement seems weird double check that you chain the transformations in a correct order.

Finally, with matrix multiplication implemented we can now use a proper projection matrix. The equivalent of the "ignore the 3rd dimension" trick is an orthogonal projection. You should be able to figure out the form of the corresponding matrix, but you are always free to just look it up. In one of the future steps we will introduce a perspective projection which will give our objects a more realistic look.

<details>
  <summary>Hint 1 (orthogonal projection matrix)</summary>
  Remember that you all you need to do is to zero the Z-coordinate, without changing the other coordinates.
</details>


<details>
  <summary>Hint 2 (orthogonal projection matrix)</summary>
  In our case this will be a diagonal matrix.
</details>

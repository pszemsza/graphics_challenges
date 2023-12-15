We will create a simple 3d renderer using only one graphical function - drawing a single pixel.

## Step 1. Drawing a line

Our first building block will be a function drawing a line between points (x1, y1) and (x2, y2).

### Line with a small slope (i.e. horizontalish one)

To start, it might be the simplest to consider a line with a small slope, e.g. (10, 10) to (60, 20). Now, for every X-coordinate between 10 and 60 we need
to put exactly one pixel - all we need is to figure out the corresponding Y-coordinate.

<details>
  <summary>Hint 1</summary>
  How to calculate the Y coordinate at the midpoint between x1 and x2? What about 25% along the (x1, x2) interval? 37%? x%?
</details>

<details>
  <summary>Hint 2</summary>
  What is the average Y-coordinate change when we move from x to x+1? Knowing this, we should be able to calculate the Y coordinate for every X value.
</details>

<details>
  <summary>Hint 3</summary>
  You can calculate the Y coordinates analyticaly (i.e. calculate the value for every X individually), or do it iteratively. For example, if the average
  Y-coordinate change is 0.2, then we need to "move" our line one pixel up every 5 horizontal pixels.
</details>

At this stage, you should be able to get something like this:

![screenshot_000593](https://github.com/pszemsza/graphics_challenges/assets/65168262/8d3cbfff-5ba5-4264-bd73-d98471455694)


### Line with a large slope (i.e. verticalish one)

If you try to draw a line with very large slope it may work similarly to this:

![screenshot_000149](https://github.com/pszemsza/graphics_challenges/assets/65168262/e20edf0a-22cc-43d4-bd56-e10f9d3287f9)

What is happening? Well, we are drawing only one pixel per X, which is clearly not sufficient to make a continuous line. We need more pixels!

<details>
  <summary>Hint 1</summary>
  What if you would switch labels on the X and Y axes?
</details>

<details>
  <summary>Hint 2</summary>
  You can think about this as a drawing a line along the Y axis - now, for every y in the (y1, y2) you will need exactly one pixel at a proper X coordinate.
</details>

### Edge cases

Once we have this working we should make sure that we handle all the edge cases. What is x1 == x2? What if x2 < x1?
What should happen when any coordinate is smaller than 0?

Think about different edge cases and make sure you algorithm handles them correctly. Also, it might be helpful to draw a bunch of random or structured lines,
e.g. like this:

![screenshot_000376](https://github.com/pszemsza/graphics_challenges/assets/65168262/10580700-33e7-4dbe-800d-fb5ca66e34b0)

You can also make the lines move around the screen or react to the mouse moves.

### Further reading

Line drawing is such a fundamental problem that a lot of research went into it. See e.g. the
[Line drawing algorithms](https://en.wikipedia.org/wiki/Line_drawing_algorithm) wikipedia page or just google around if you are interested.

Julia sets are named after the French mathematician Gaston Julia, who first studied them in the early 20th century. They are formed by applying a specific mathematical formula, such as $z^2+c$ to complex numbers (here $c$ is a constant which will characterize the fractal shape). This formula generates a sequence of numbers starting from any initial point z_0​ on the complex plane. First, you apply the formula to $z_0$​ to get a new number $z_1$​. Then, you repeat this process to get $z_2$​, $z_3​$, and so on. As you iterate, these numbers may either grow infinitely large, or remain bounded. A Julia set is simply a set of points $z_0$ for which the sequence remain bounded.

In practice, we limit the number of iterations and check the magnitude of obtained numbers as a proxy for being bounded. If the magnitude exceeds a certain threshold, we consider the point to have escaped to infinity, i.e. not belonging to the Julia set.

# Step 1. Complex numbers arithmetic
We will need to perform complex number addition and multiplication, so ensure you're familiar with these operations.

# Step 2. Mapping between complex numbers and a screen
Of course, we'll also need to display complex numbers on a screen, requiring a mapping between these two spaces. A common approach is to use the X-axis of the screen to represent the real part of the number and the Y-axis for the imaginary part. In the Julia set, points typically cluster around the center of the coordinate system with a magnitude less than 2, so your mapping should consider this distribution.

# Step 3. Drawing the fractal
Let's dive into rendering our first fractal! Start by selecting your parameter $c$ (a good starting point could be c = 0.33 + 0.12i). Then, for each pixel on the screen, map it to its corresponding complex number and apply the Julia set formula iteratively. If the magnitude of the resulting number exceeds a certain threshold, e.g. 2, halt the iteration. When reaching the maximum number of iterations, mark the point as part of the Julia set by drawing a pixel.

# Step 4. Choosing parameter $c$
Now experiment with different values of a parameter $c$. You can use mouse click position to set the new value. 

# Step 5. Shading
Let's now add more depth and detail to our renders by incorporating shading. You can use the number of iterations needed for the sequence to escape to infinity as a guide for coloring the fractal. For example, you could draw the Julia set with black, and its surrounding area with a linear gradient of a chosen color.

# Step 6. Zooming in and out
To better study the fractal nature of the Julia sets it is useful to have a capability to zoom in into a chosen area. Use mouse and/or keyboard controls to zoom in and out,  centering the image around the selected point, and moving it up/down/left/right.

# Next steps

- enhance coloring. You could use a multi-color gradient to add more contrast and depth to your images

- Experiment with alternative fractal formulas - you can try using formulas, for example $z^2+z-c$ or $z^3+c$ to generate different fractal patterns and structures

- Adapt for GPU - drawing Julia sets can be computationally intensive, especially with larger screens and higher iteration counts. Consider implementing parallelization or utilizing GPU acceleration to accelerate the rendering process.

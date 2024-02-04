# Edge detection

To simplify things, I suggest to work with grayscale images in this project.

# Step 1

First, ensure you can read an image and modify its pixels. Find a suitable test image, such as Lena, peppers, or cameraman, or use your own grayscale photo.

Next, manipulate its pixels in some way. You can add noise, adjust brightness, or perform other transformations, and then draw the modified image.

# Step 2

Keywords: _convolution filter_, _kernel_

In this step we will process our image with an edge detection convolution filter. Let's begin with a simple vertical edge detection filter:

$$ \begin{bmatrix} 
   1 & 0 & -1 \\
   1 & 0 & -1 \\
   1 & 0 & -1 \\
\end{bmatrix} $$

Apply this filter (or kernel) to every pixel of your image. To do this, center the filter over each pixel, multiply the covered pixels by the corresponding values, and sum them together.

Make sure to properly handle the pixels at the edges of your image. You can treat the out-of-bounds pixels as zeros, duplicate or average values from their neigbors, or skip them entirely (which will make the resulting image slightly smaller than the original).

# Step 3

Let's now add more filters and allow the user to choose one. The filter in the previous step detects vertical edges, so you may want to add one for the horizontal or diagonal edges as well. There are also filters e.g. for bluring and sharpening.

# Next steps

Edge detection is a fundamental topic in the image processing. Hence, it has received a lot of attention, and multiple algorithms have been proposed. For example, the Sobel edge detector consists of a pair of convolution filters that are combined together. Canny's algorithm goes even furthen, combining multiple convolution filters and other operations in a multi-step process.Feel free to explore and implement these algorithms if you're interested.

An interesting follow-up project is to extend your program to work with videos. Extract individual frames, apply edge detection, and then combine the modified frames together.
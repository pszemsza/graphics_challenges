# Edge detection

To simplify things, I suggest to work with gray scale images in this project.

# Step 1

First you need to be able to read an image and modify its pixels. So, first you will need to find a good test image (some of the classic reference images used in many image processing are Lena, peppers, or camera man), or use your own photo (just convert it to the grayscale first).

Then, do something with its pixels (you can add some noise or make it darker/brighter, for example) and draw it.

# Step 2

Keywords: _convolution filter_, _kernel_

In this step we will process our image with an edge detection convolution filter. While you could construct your filter in many different ways (you will explore them in the next step), for now let's use a simple vertical edge detection:

$$ \begin{bmatrix} 
   1 & 0 & -1 \\
   1 & 0 & -1 \\
   1 & 0 & -1 \\
\end{bmatrix} $$

You will need to apply this filter (or kernel) to every pixel of your image. You simply "center" the filter over your pixel, multiply the covered pixels by the corresponding values, and sum them together.

Make sure to properly handle the pixels at the edges of your image. You can treat the out-of-bounds pixels as zeros, duplicate or average values from their neigbors, or just skip them entirely (which will make the resulting image slightly smaller than the original).

# Step 3

Let's now add more filters and allow the user to choose one. The filter in the previous step detects vertical edges, so you may want to add one for the horizontal or diagonal edges as well. There are also filters e.g. for bluring and sharpening.

# Next steps

Edge detection is an important topic in the image processing. Hence, it has received a lot of attention, and multiple algorithms were proposed. For example Sobel edge detector consists of a pair of convolution filters which are then combined together. Canny's algorithm goes even furthen, combining a number of convolution filters and other operations in a multi step process. Feel free to read more about and/or implement them if you are interested.

An interesting follow up project is to extend your program to work on videos. You would extract all individual frames, apply the edge detection, and then put the new frames together.

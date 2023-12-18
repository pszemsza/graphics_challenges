
I suggest to start with a simple attractor with the general form:

$x = a * sin(b*y) + c * cos(d*x)$

$y = a * sin(b*x) + c * cos(d*y)$

where $a$, $b$, $c$, and $d$ are constant parameters.

# Step 1
To draw the attractor you start with a random point $(x, y)$. In every iteration you put a pixel at the (x, y) point, and calculate new coordinates using the attractor equation.
There is a couple of practical considerations before we start implementing this simple algorithm.

First, how to choose the parameter values? Unfortunately, not all values will yield a nice looking attractor. In the next step we will make it easier to explore the parameter
space and find good parameters; for now you can use a=1.19, b=1.195, c=1.4, d=1.365. What about the starting values for x and y? Here the choice is not that important - after all,
we are working with attractors, so our points should eventually converge. Just note that some values (e.g. (0, 0) or (1, 1)) will yield degenerative solution. But as long
as $x\neq y$ you should be good. Of course, you can just randomize the starting values.

Secondly, we need to map between our attractor (x, y) values and the rendering window coordinates. Our (x, y) values would be approximately in the (-2, 2) range, so you should
ensure that values from this range will be visible in your window.

Lastly, getting a clearly visible attractor pattern may require at least thousands of points to be drawn. Thus, I suggest to draw O(100s) points in every frame - significantly fewer
than that and it will take a long time for the attractor to become clear, significantly more - and it may become oversatured quickly.

The table below shows how the rendering changes with the increasing number of iterations.

<table>
  <tr>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/33321b99-fd9a-4cc1-bb06-9cc3da54a46a" width=200px height=200px></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/f132c989-4e15-4813-bf5f-90b86bc7e434" width=200px height=200px></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/0cca6a05-e6b5-48b4-95ae-dbfc3b0cf03d" width=200px height=200px></td>
  </tr> 
  <tr>    
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/81fb1ebd-f308-49bf-a888-e8c2c41061fe" width=200px height=200px></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/a9d23eb7-a3fd-451e-b49e-1c1ee002f9b2" width=200px height=200px></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/bcde8c47-8398-40e4-8735-78ee3d05561b" width=200px height=200px></td>
  </tr> 
</table>

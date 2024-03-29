

# Step 1. Drawing a simple attractor
Keywords: _strange attractors_

To draw the attractor you will draw pixels one by one. You start with a random (x, y) point, and calculate new coordinates (x', y') using the attractor equation. I suggest to start with a simple attractor with the general form:

$`x' = a * sin(b*y) + c * cos(d*x)`$

$`y' = a * sin(b*x) + c * cos(d*y)`$

where $a$, $b$, $c$, and $d$ are constant parameters.

There are a couple of practical considerations before we start implementing this simple algorithm.

First, how do we choose the parameter values? Unfortunately, not all values will yield a nice-looking attractor. In the next step we will make it easier to explore the parameter
space and find good parameters; for now you can use a=1.19, b=1.195, c=1.4, d=1.365. What about the starting values for x and y? Here the choice is not that important - after all,
we are working with attractors, so our points should eventually converge. Just note that some values (e.g. (0, 0) or (1, 1)) will yield degenerative solution. But as long
as $x\neq y$ you should be good. Of course, you can just randomize the starting values.

Secondly, we need to map between our attractor (x, y) values and the rendering window coordinates. Our (x, y) values would be approximately in the (-2, 2) range, so you should ensure that values from this range will be visible in your window.

Lastly, getting a clearly visible attractor pattern may require thousands of points to be drawn. Thus, I suggest drawing O(100s) points in every frame - significantly fewer
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

<br/><br/>

# Step 2. Changing parameters in real time
Keywords: _drag'n'drop_

You should be able to get an attractor drawn for specific parameters. To make it easy to explore different shapes yielded by different parameters it will be helpful to be able to modify the params in real time. It would be quite easy to use keyboard or sliders, so we will do something else instead. We'll employ draggable circles to represent pairs of parameters (a, b), positioned at the point (x, y). In this setup, the parameter _a_ (_b_) will be encoded using the x (y) coordinate of the circle. This will allow us to modify 2 parameters at the same time, and it will make it a bit easier to visualize the change of parameters in time, which we will add in the following steps. Of course, you will need multiple circles to represent your parameters if you have more than 2. Remember to refresh your screen after each parameter adjustment. 

Additionally, as in the previous step, you'll need to map values from pixel coordinates to the parameter space.

![screenshot_000173](https://github.com/pszemsza/graphics_challenges/assets/65168262/0244a7a6-c5b0-4e59-ae61-ebd99ff1a017)

<br/><br/>

# Step 3. Adding colors
Keywords: _HSV color model_

Let's add a few different color modes. For a solid color, let's do black-on-white, white-on-black and color-on-black. How can we expand our color palette further? One approach is to use a point "velocity", which is defined as the distance between the current and previous (x, y) coordinates. This will give you a scalar that can be easily translated into a colorful gradient using the HSV color model.

<table>
  <tr>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/e720cb06-2bbb-418e-9bc4-47373f25439c" width=200px height=200px></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/09a172ef-01fa-47dd-823e-533f30f030dd" width=200px height=200px></td>

  </tr> 
  <tr>    
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/c687752e-7564-4d64-a993-46b8d4fa1800" width=200px height=200px></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/3b4fca40-76d0-493e-8012-1cd63e93a66b" width=200px height=200px></td>

  </tr> 
</table>

<br/><br/>

# Step 4. Animation - smooth parameters change
Keywords: _Bezier curve_, _spline curve_, _C1 continuity_

Now that we've achieved generating appealing static images, our next endeavor is to create smooth animations. This involves rendering a sequence of attractors with slight parameter adjustments and then combining these individual frames into a video. In this step we will work on a smooth parameters change.

The simplest approach would be to change each param by a small constant value. The problem is that eventually the parameters will grow large (in absolute terms), which typically yields less interesting attractors. Ideally, we want the parameters to change smoothly within a reasonable range.

Another approach could be to express parameters as functions of time - for example, one parameter could be defined as $a=1.7sin(t/20)$, where $t$ represents elapsed seconds/minutes or the current frame number. While this would give us smooth and bounded parameters, it lacks fine control over the evolution of parameters.

To address these issues we can use geometric shapes like Bezier curves. These curves are defined by a series of points (typically four for cubic curves), where each point influences the shape of the curve. The curve starts at the first point and ends at the last one, with the intermediate points serving as magnets shaping the curve. Each point on the curve can be calculated using a simple formula which depends only on the points themselves and a single parameter $t$.

In the previous step we used a circle to represent a pair of parameters.  Now, we'll extend this concept by employing Bezier curves. For example, if our attractor has eight parameters, we could define four 2D Bezier curves or a single 8-dimensional curve (and to visualize it you could simply display 4 circles representing pairs of coordinates: $`(x_1, x_2), ..., (x_7, x_8)`$).

Note: for this step I suggest to start a new sketch instead of expanding the code from the previous step, especially if you haven't worked with Bezier curves before. It will make things simpler, as you will only need to think about the curves, and it will make implementation and debugging easier.

So, let's get to work. First you'd define your curve(s). I suggest to display the control points and lines connecting them, and outline the curve itself (e.g. calculate and draw the points for $`t=0.0, 0.05, 0.1, ..., 0.95, 1.0`$). Once you have this, you may want to animate a point sliding along the curve (i.e. draw a point at $`t=0.0`$ in the first frame, at  $`t=0.002`$ in the second etc.).

![Untitled](https://github.com/pszemsza/graphics_challenges/assets/65168262/6f9581ed-fff9-4e33-b330-7bd83abc7010)


We should also allow the curve to "continue" after we reach its end, i.e. when $`t>1.0`$. For this, we can simply generate new control points and repeat the whole procedure. An important consideration here is the geometric continuity - you should use the last point of the old curve as the first point of the new one, otherwise you will have a sudden jump to an entirely different position. But even with this the transition between the 2 curves won't be entirely smooth, as you are most likely to have a sharp change of direction. To combat this you may use one of the properties of the Bezier curves: a curve defined by points $`P_1, P_2, P_3, P_4`$ is tangent to the line $`(P_3, P_4)`$ at the point $`P_4`$. Now, you want your new curve to be tangent to the same line at the new point $`P'_1`$. For this, you can simply reflect $`P_3`$ over $`P_4`$ and use it as $`P'_2`$. Formally, you can say that the first derrivative of your curve is now continuous, which gives you a C1 continuity. The other points can be completely random.

<table>
  <tr>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/1f1faccb-a5e0-421c-a0fa-fa6b761ffa95" width=200px height=200px><p>C0 continuity</p></td>
    <td><img src="https://github.com/pszemsza/graphics_challenges/assets/65168262/09d573d0-8d51-4695-810f-af99a39c707a" width=200px height=200px><p>C1 continuity</p></td>
  </tr> 
</table>

<br/>

And voilà! You now should be able to generate an infinite smooth curve!
<br/>

https://github.com/pszemsza/graphics_challenges/assets/65168262/1947e678-3c7b-485b-baf9-bfe133b0b1ff

<br/>
The last thing to do is to expand your curve to as many dimensions as you have parameters (or simply use multiple 2D curves). At this point the visualization might get somewhat crowded. This is an example of what it might look like with 6 parameters:

https://github.com/pszemsza/graphics_challenges/assets/65168262/d8fbe5d9-174b-4265-927d-c3c6c4763b82

<br/><br/>

# Step 5. Putting it all together

Now it is time to combine our single frame drawing with smooth parameter change. 

If you are feeling lucky you may use randomized control points, but you are risking getting degenerated attractors for some of the parameters, resulting in a not-that-attractive animation. A better idea might be to provide a series of fixed parameter sets that will guide the animation (you can obtain them by playing with your code from the Step 3 and writing down the parameter values for which you get a nice drawing). You could provide all control points in the successive Bezier curves (which would give you a total control, but would require more work), or just the first and the last ones, randomizing the intermediate ones. In the latter solution you may want to generate random points that are not too far from the end points so that you will obtain a smooth, gently curved line, instead of a "loopy" one.

I suggest to use a "dev" mode, in which you significantly reduce the number of iterations per frame, increase $t$ parameter changes and use a smaller resultion. This will allow you to quickly generate a preview of the animation. Once you are satisfied with the results you can readjust the values to get a high quality animation.

https://github.com/pszemsza/graphics_challenges/assets/65168262/b62e9d15-6712-488f-bfca-251a4f89a839

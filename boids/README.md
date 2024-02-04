# Step 1. Drawing a Boid


Let's begin by drawing a single boid. While any shape could technically be used, opting for something "pointy" (an isosceles triangle is a frequent choice) makes it easier to discern the boid's direction. Make sure to consider the boid's rotation when drawing!

<br/>![screenshot_0049](https://github.com/pszemsza/graphics_challenges/assets/65168262/f432d2f0-98af-4403-9712-a31583208dc1)


# Step 2. Basic Movement
Keywords: _screen wrap_

In this step, we will add basic random movement. There are 2 main options to work with the movement:
* velocity vector
* movement angle and speed

In the following steps, we will make heavy use of vectors, so the former option might be easier. Whichever option you choose, remember to add some random changes so that you get a natural-looking movement.

To keep things simple, let's employ a wrapped screen mechanism for now. This means that when a boid traverses e.g. the screen's right edge, it reappears on the left side.


https://github.com/pszemsza/graphics_challenges/assets/65168262/dfa38df3-140b-4cd9-ae56-493ee2f154dd


<br/>

# Step 3. Flock

Now, it's time to assemble a complete flock. We can use the code from a previous step, except we want to have multiple boids.


https://github.com/pszemsza/graphics_challenges/assets/65168262/5ab522bb-95ea-496c-a198-4cd590011925



<br/>

# Step 4. Flocking Behavior
Keywords: _boids_, _flocking simulation_

Here's where things get interesting - we'll implement the actual flocking behavior! Traditionally, boids adhere to three rules:

* Separation: move away from other boids that are too close,
* Cohesion: move towards the center of mass of nearby neighbors,
* Alignment: match velocity with neighboring boids.

These simple rules are sufficient to yield natural-looking, emergent behavior.

It is important to note that boids have limited vision, only seeing other boids within a certain distance. The basic algorithm is as follows: for every boid, find all other boids within the visual range and find their center of mass and average velocity. Additionally, find all boids that are within a boid's personal space, and calculate an avoidance vector (i.e. a vector pointing away from them).

You can treat these 3 components as velocities. For example, you can convert neighbors' center of mass to a vector from the boid's position to the neighbors' center of mass. Additionally, it might be a good idea to add a small random velocity change. Now all you need to do is combine these individual velocities (a linear combination) to get the new boid's velocity. You will likely need to play a bit with the weights of the components to find reasonable values. There should be a relative balance between the rules. For example, if you put a very large weight on the cohesion component, it might completely upstage the boid's separation rule. You should also tune the visibility and personal space ranges. Proper tuning can be a bit tricky at first, so it might be easiest to add an option to change the parameter values in real-time and do the tuning while observing the flock behavior.

At this stage, it might also be a good idea to clamp the speed to a predefined range (or to add an upper bound, at least). This will prevent boids from changing direction too rapidly and should yield smoother movement.



https://github.com/pszemsza/graphics_challenges/assets/65168262/994912ae-8766-4561-a8ec-2b9d6e3ae434



<br/>

# Step 5. Walls

You may observe a weird behavior when a part of the flock moves over the screen edge. Although conceptually forming a single flock, boids on opposite sides may not be within each other's visual range. Consequently, some may alter their course before crossing the screen edge and split from the original group, potentially disrupting the flock's cohesion. It might also happen that a single boid will pass the screen's edge only to fly right into the middle of a peacefully cruising dense flock on the other side, creating a huge disruption as the boids will try to keep their distance from the intruder.

To address this, let's introduce an additional rule for boids - screen edge avoidance.


https://github.com/pszemsza/graphics_challenges/assets/65168262/cfb2d862-78b0-4ebf-971c-72d36c51c301



<br/>

# Step 6. Predators

At this stage, we have basically replicated the core boids algorithm. Now we can expand it a bit, for example by adding predators. I'll leave it to you to come up with the rules for their behavior. You can get different effects depending on whether the maximum predator speed is higher or lower than that of the prey's. You should also consider what should happen when a predator catches its prey. In the simplest case, you can just remove the caught boid.


<details>
  <summary>Hint</summary>
  Predators typically aim to catch prey. You have a few options here - maybe try to move towards the center of mass of the neighboring boids, where the likelihood of catching something might be the highest? Or maybe try to always catch the closest boid in the visual range? Or, once spotting a prey, maybe keep pursuing it (indefinitely, or maybe for a specified duration, after which the predator gives up) ignoring other boids?

  <br/>

  You may also consider adding a separation rule for predators.
  <br/>

  Conversely, prey should instinctively move away from predators, akin to the separation rule for boids, albeit with a higher weight.
</details>

https://github.com/pszemsza/graphics_challenges/assets/65168262/f5ee5ecc-49e9-4e40-a2b8-721f8643cbc7

<br/>

# Step 7. Final touches and new features

At this stage, you should have a compelling boids simulation with multiple rules in place. Thus, it is a good point to take a step back and smooth all rough edges. For example, if you look closely at the movie in the previous step, you may notice that the screen edge margins are clearly visible, as the boids suddenly jerk when they move past them. The reason for this is that I'm applying a constant shift to the velocity vector when a boid moved past the margin. It would be better to apply proportional shift based on how much into the margin territory the boid has flown.

Similarly, often the separation rule is implemented by taking the (average) vector to the neighbors and adding (after scaling) to the velocity vector. When implemented naively, it means that the velocity change is larger when the neighbors are far away and smaller when they are close. This is clearly not how it should work.

Note that this is implementation dependent, so you may not have such an issue in your simulation; in any case, I encourage you to look again at your animation and see if there are any artifacts or things that could be improved. If you haven't done that already, it is useful to allow adding prey/predators at a selected location in real-time, e.g. by clicking a mouse button.

Another potential issue might be caused by direct velocity vector modification, which allows for drastic changes of direction and/or speed. Instead, one might interpolate between the current and expected velocity vector, making the movement smoother.

Lastly, you can introduce new features. Here are some ideas:
* add fixed or floating food sources that would attract boids (and make a nice feeding spot for predators),
* add various obstacles,
* make min/max speed different for different boids,
* add fatigue attribute to the prey (or predators), so that their speed would decrease with time,
* add the gravity force,
* try to simulate as many boids as possible (you may want to simplify rendering, and e.g., represent a boid with a single pixel) using some code optimizations,
* create 3 species of boids forming a rock-paper-scissors type prey/predator relationships between them, and watch the ensuing chaos.

<br/>

In my case, I simply fixed the velocity calculations, which gave me a much more natural-looking movement:

https://github.com/pszemsza/graphics_challenges/assets/65168262/3574b799-3400-46e1-b62c-3a92b9a0527a

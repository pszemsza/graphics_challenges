

<br/>

# Step 1. Drawing a boid

Let's start with drawing a single boid. In principle you can use any shape, but it might be easier to see what is going on if you'd use something "directional", so that you can tell which direction a boid is facing. An isosceles triangle is a common choice.

Make sure to consider boid's rotation when drawing!

<br/>![screenshot_0049](https://github.com/pszemsza/graphics_challenges/assets/65168262/f432d2f0-98af-4403-9712-a31583208dc1)


# Step 2. Basic movement
Keywords: _screen wrap_

In this step we will add a basic random movement. There are 2 main options to work with the movement:
* velocity vector
* movement angle and speed

In the following steps we will make a heavy use of vectors, so the former option might be easier. Whichever option you choose remember to add some random changes so that you get a natural looking movement.

To keep things simple I suggest to use a wrapped screen for now. This means that e.g. when your boid moves over the right edge of the screen it will reappear on the left side.


https://github.com/pszemsza/graphics_challenges/assets/65168262/dfa38df3-140b-4cd9-ae56-493ee2f154dd


<br/>

# Step 3. Flock

Now it is time to create a whole flock. We can use the same code as before, except we want to have multiple boids.



https://github.com/pszemsza/graphics_challenges/assets/65168262/5ab522bb-95ea-496c-a198-4cd590011925



<br/>

# Step 4. Flocking behavior
Keywords: _boids_, _flocking simulation_

Now things start to become interesting - we will add the actual flocking behavior! Traditionally there are 3 rules that each boid follows:

* separation: move away from other boids that are too close,
* cohesion: move towards the center of mass of your neighbors,
* alignment: match velocity with your neighbors.

These simple rules are sufficient to yield natural looking, emergent behavior.

It is important to note that boids have a limited vision, and can only observe other boids within a certain distance. The basic algorithm is as follows: for every boid find all other boids within the visual range, and find their center of mass and average velocity. Additionally, find all other boids that are within a boid's personal space, and calculate a vector pointing away from them.

You can treat these 3 components as velocities. For example, you can convert neighbors' center of mass to a vector from the boid's position to the neighbors' center of mass. Additionally, it might be a good idea to add a small random velocity change. Now all you need to do is combine these individual velocities (a linear combination) to get the new boid's velocity. You will likely need to play a bit with the weights of the components to find reasonable values. There should be a relative balance between the rules. For example, if you would put very large weight to the cohesion component, it might completely upstage the boid's separation rule. You should also tune the visibility and personal space ranges. A proper tuning can be a bit tricky to get at first, so it might be the easiest to add an option to change the parameter values in real time and do the tuning while observing the flock behavior.

At this stage it might also be a good idea to clamp the speed to a predefined range (or to add an upper bound, at least). This will prevent boids from changing the direction too rapidly, and should yield a smoother movement.



https://github.com/pszemsza/graphics_challenges/assets/65168262/994912ae-8766-4561-a8ec-2b9d6e3ae434



<br/>

# Step 5. Walls

If your boids still use wrapped screen you may observe a weird behavior when a part of the flock moves over the screen edge. While boids on both sides of the screen visually still form a single flock, they are actually outside of each other visual range. Thus, there is a chance that a part of the flock will change the direction before passing the screen edge, and effectively will split from their group. Alternatively, it might happen that a single boid will pass the screen's edge only to fly right into a middle of a peacefully cruising dense flock on the other side, starting a separation rule violation chain reaction.

This might be fine for you, in which case you can feel free to skip this step. Otherwise, let's add an additional boid's rule - screen edge avoidance.




https://github.com/pszemsza/graphics_challenges/assets/65168262/cfb2d862-78b0-4ebf-971c-72d36c51c301



<br/>

# Step 6. Predators

At this stage we have basically replicated the core boids algorithm. Now we can expand it a bit, for example by adding predators. I'll leave coming up with the new rules to you. You can get different effects depending on the whether the maximum predator speed is higher or lower than than the prey's. You should also consider what should happen when a predator catches its prey. In the simplest case you can just remove the caught boid.


<details>
  <summary>Hint</summary>
  Predators should probably try to catch a prey (i.e. boids). You have a few options here - maybe try to move towards the center of mass of the neighboring boids, where the likelihood of catching something might be the highest? Or maybe try to always catch the closest boid in the visual range? Or, once spotted a prey, maybe keep pursuiting it (indefinitely, or maybe for a specified duration, after which the predator gives up) ignoring other boids?

  <br/>

  You may also consider adding a separation rule for predators.
  <br/>

  Behavior for prey should be rather obvious - they should try to move away from the spotted predators. Thus, this is basically the same as a separation rule for boids, except you may want to give it a higher weight.
</details>



https://github.com/pszemsza/graphics_challenges/assets/65168262/f5ee5ecc-49e9-4e40-a2b8-721f8643cbc7



<br/>

# Step 7. Final touches


https://github.com/pszemsza/graphics_challenges/assets/65168262/3574b799-3400-46e1-b62c-3a92b9a0527a



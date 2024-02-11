This project differs slightly in nature, as it focuses on simulation visualization rather than computer graphics. Nonetheless, it certainly makes for an interesting project!

# Basic assumptions

## Time representation
We have two main choices: continuous or discretized time. In the former case, you have total control over time intervals. For example, you can easily randomize the movement and stowing baggage speed for every passenger by sampling from a normal distribution. In the latter, you have lower granularity of time intervals, but overall time management will likely be much easier. Note also that we can still simulate continuous time with discrete units by using larger values. If it takes 2 units of time to move by one row, then your closest options are 1 and 3, which would show an exaggerated difference. However, if it takes 2000 time units, then you have a wide range of reasonable values.

## Agent vs global planning
Another significant consideration is whether you want to manage passenger movement globally or let them be autonomous agents that observe their local surroundings to decide on their next action. Both approaches have their advantages, so choose whichever you prefer.

# Plane representation
While you can keep your passengers in a separate structure, it might be useful to have a representation of the plane (both seats and the aisle), that would allow for a quick lookup whether a given seat is occupied (and by whom) or not. I suggest representing  every seat as a single cell, with the adjoining fragment of the aisle also being a single cell.

The simplest representation is probably a 2D array. In a 3-by-side plane, each row would have 6 elements, with indices 0-2 corresponding to the left plane side and 3-5 to the right. One issue here is that you would need to use the number of seats on each side to get your indices and handle the left and right plane sides separately, which might make the code a bit cumbersome and less readable.

Another approach is to use a 3D array, with one of the dimensions representing the two sides of the plane. This way, indexing is more consistent, as index 0 in the row dimension can always represent the aisle seat.

It might be useful to add a few 'dummy' rows in front of the plane so that passengers don't suddenly appear in the first row. In my opinion, it looks much better in the visualization.

# Simulation
The basic idea is rather simple, with every passenger executing the same algorithm. First, move toward your row, waiting whenever someone is in front of you. When you finally make it to your row, stow your baggage. Then either seat (if no other passenger is sitting between you and your seat) or wait for them to vacate their seats and let you pass by.

# Boarding Zones
I suggest starting with random seat assignment for simplicity. Once everything is working, you may want to add different boarding zones.

One way to achieve this is to add a boarding zone attribute to every seat. You can then shuffle all seats randomly and sort them (in place) by the boarding zone. This should guarantee a random distribution of the seats while preserving the boarding zones' order.

# Boarding Methods Comparison
We can now compare the times required for complete boarding when different methods are employed. You can simply run the simulation 1000 times and calculate the mean or plot the distribution.

# Visualization
Now we can move to the core of the project, which is visualizing the boarding. You can do this either in parallel with running the simulation or save the simulation progress to a file and run visualization separately. To do this, you will need to save the current state throughout the simulation to a file. I think it is easiest and most compact if these checkpoints are made per passenger. This means that you would keep a history of actions for every passenger.

As a final touch, you may want to add a boarding zones legend, display boarding completion rate, and color code the passenger states, etc.

# Sample code
For the sample code for both the simulations and the visualization please see the [plane boarding repo](https://github.com/pszemsza/plane_boarding).

# Sample visualization

https://github.com/pszemsza/plane_boarding/assets/65168262/281f82f3-f9af-48ff-b16f-e264ff6e0c60

https://github.com/pszemsza/plane_boarding/assets/65168262/007e2465-bbcc-4318-a38f-57f55ea2a8b4

https://github.com/pszemsza/plane_boarding/assets/65168262/c6347151-4f33-409e-81ad-2828d4ec9ed6

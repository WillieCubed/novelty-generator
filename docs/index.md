# Willie's Novelty Generator Docs
*Because why not?*

## Overview
For a better understanding of the problem, see the [novelty](./novelty.md)
definition page.

## Ideas for implementation:
### Stage 0: Baseline Novelty
  - Modify the environment in random ways
    - Probably will not scale well in more complex or open-world environments.
  - Choose random things that affect/reduce/expand the action space?
    - Example: in CartPole, what if the cart randomly starts moving on its own?
  - Use probability distribution to find least likely thing to change?

### Stage 1: Intelligent Rewards
1) Find which things have most affect on reward and modify those
2) Find some mechanism to ensure that learning isn't stuck on a downward spiral

### Stage 2: Adversarial Novelty
1) Take inspiration from adversarial generative networks
2) Create an environment that's almost like the existing one, but engineered to
be a little bit different
   - Almost like taking snapshots of previous states?
   - Like the environment is trying to stop the agent from succeeding, but not
     entirely
      - Likely keep track of internal reward
      - Maybe a penalty imposed for challenges that are too hard
      - Or a small bonus for challenges that are just the right length
      - Use RL to determine reward for novel features changed?

## More possible ideas
  - Store the state of every object in the world and literally just modify
    their state when they become important for novelty
      - Probably not that scalable
      - How is importance determined?

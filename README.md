# Flappy Bird AI

## Description
Using the library `pygame`, I've recreated the game `Flappy bird`, keeping the core mechanics the same as in the original, but altering the bird functionality by giving it a virtual brain.

### The brain
The birds' brains work by trying to imitate real life neuron connections, using the branch of `Machine Learning` called `Neural Networks` ([More Information](https://www.ibm.com/topics/neural-networks)).

#### How do they work?
They take 3 inputs from the game environment (input layer):
- The distance to the next pipe
- The distance to the bottom point of the top pipe
- The bird's velocity

Initially, these input layer values undergo transformation via the sigmoid function, ensuring they fall within the range of 0 to 1 for subsequent node utilization.

Upon gathering information from the environment, the data proceeds to the hidden layer, where matrix multiplications occur based on genetic factors. Subsequently, the hidden layer transmits to the output layer, where additional mathematical computations ensue, yielding an output within the range of 0 to 1. If the resulting prediction surpasses 0.5, the bird executes a jump action.
### Genetic Algorithm
Every bird has a variable called fitness, representing how good it is perfoming
After each bird has died, the genes from the best perfoming bird are stored, and then spread to some new birds with some mutations.
When the bird gets a very good fitness, the mutation multiplier decreases, and when the bird isn't good at all, the multiplier increases.
This results in the birds actually learning from each other and trying to perform better each time

### The result

![Example](assets/Screenshot_3.png)
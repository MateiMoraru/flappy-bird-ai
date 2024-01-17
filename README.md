# Flappy Bird AI

## Description
Using the library `pygame`, I've recreated the game `Flappy bird`, keeping the core mechanics the same as in the original, but altering the bird functionality by giving the bird an actual brain.

### The brain
The birds' brains work by trying to imitate real life neuron connections in the brain, using the branch of `Machine Learning` called `Neural Networks` ([More Information](https://www.ibm.com/topics/neural-networks)).

#### How do they work?
They take 3 inputs from the game environment (input layer):
- The distance to the next pipe
- The distance to the bottom point of the top pipe
- The bird's velocity
At first, we transform the input layer values in order to be 0 > a > 1 by applying the sigmoid function (`1/(1 + -e^-x)`).

After collection information from the environment, it passes on to the hidden layer where each hidden layer gets the value <math display="block">
  <msub>
    <mi>y</mi>
    <mi>j</mi>
  </msub>
  <mo>=</mo>
  <munderover>
    <mo data-mjx-texclass="OP">&#x2211;</mo>
    <mrow data-mjx-texclass="ORD">
      <mi>i</mi>
      <mo>=</mo>
      <mn>1</mn>
    </mrow>
    <mrow data-mjx-texclass="ORD">
      <mi>n</mi>
    </mrow>
  </munderover>
  <msub>
    <mi>w</mi>
    <mrow data-mjx-texclass="ORD">
      <mi>j</mi>
      <mi>i</mi>
    </mrow>
  </msub>
  <mo>&#x22C5;</mo>
  <msub>
    <mi>x</mi>
    <mi>i</mi>
  </msub>
</math>


![Example](assets/Screenshot_3.png)
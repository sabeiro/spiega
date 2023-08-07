# agent naming environment

In this project we create an agent able to distinguish and name object on the environment

## Breakout

Similar to [keras article](https://keras.io/examples/rl/deep_q_network_breakout/) we create a model to parse the input image from atari games and decide how to interact with the environment: i.e. how to move.

![breakout](../f/f_gen/breakout_atari.png "breakout atari") 
_using openai gym to train an agent to play breakout_

To understand how the agent is learning the enviroment we create a visualization to focus on the main step of learning.

![attention_init](../f/f_gen/attention_init.png "attention map") 
_visualization to monitor the development of the learning process_

The visualization consists in:

* **scores**: loss and reward
* **inputs**: batch average of the states (frames) and velocity (frame difference)
* **actions**: distribution of moves over time
* **attention map**: where the model is focusing the attention

Based on the reward (bricks crushed by the ball) the agent learns how to behave in such environment

### implementation

Compared to the [original implementation of the game](https://www.deepmind.com/publications/playing-atari-with-deep-reinforcement-learning) we performed few differences:

* velocity and collision (velocity change) instead of a stack of 4 consecutive images (dropped acceleration because rearly happens on the same pixel)
* batch of 64 consecutive states (I didn't get the advantage of randomizing) and use of `deque`
* treaning each 16 actions
* genetic selection of algorithm considering the fitness
* feedback loop between actions (actions are both input and output of the model with -1 time difference)
* output classes based on break down of the interaction function

For [more references](https://github.com/fg91/Deep-Q-Learning/blob/master/DQN.ipynb)

![attention_init](../f/f_gen/collision.png "collision") 
_velocity and collision as input parameters_

The model outputs different classes defined by measurable interaction with the environment, mainly: myself, tool, walls, info, dangers...

### attention

The attention map tells a lot about the key challanges of this exercise

* **who am I?**: different parts are moving, what is the part of the picture I control?
* **tools**: what parts of the environemnt I can use
* **walls**: what parts define the boundary of the environment
* **danger**: what parts harm my entity
* **reward**: what is a benefit for me
* **info**: what is the outside of the environment just providing information

Compared to other games breakout has a lot of interesting challanges in the understanding of causality.

### causality

In this game you get the reward the moment the ball hits the bricks but you control only the paddle. 
In the eyes of the agent I first see a clear **correlation**:

* **score**: for each reward a digit change: 100% correlation, 0% causality
* **hit**: for each reward a brick disappears: 100% correlation, long rage causality -> effect
* **ball**: multiple bounces -> mean
* **paddle**: complete control through actions -> cause

![attention_init](../f/f_gen/attention_evolution.png "attention map") 
_evolution of attention over time, the focus on digits drops over time, the agent is then learning to avoid losing life focusing on the bottom._

# Deep learning concepts

## batch

The total number of examples for each iteration

## cost function

A function that evaluates the error between the fit function and the variable to predict

Squared error:

$$ F(x,y) = \sum_i (y_i - w_i x)^2 / N $$

Logistic function

$$ F(x,y) = \sum_i log(1 + e^{-y_i(w_i^T x+b_i)} )$$

## optimizer

The optimizer suggest the direction for the minimization of the cost function

$$ min_x F(x) := \sum_i f_i(x) $$


Minimize the cost function $f(x,y)$, first order optimizers use the gradient, the second the Hessian.

* gradient
  * first derivative of the cost function
  * move the parameters a step towards the steepest descent with a momentum $\eta$
  $$ \eta \grad F(x) $$
  
* Hessian
  $$ H^2 := \sum_{j} \grad f_{ij} (x_j) \grad f_{ij} (x_j)^T $$

* Preconditioner
  $$ B := diag H $$

* gradient descent
  * gradient on a random point
  $$ x_{t+1} = x_t - \eta \grad F(x_i) $$

* stochastic gradient descent
  * gradient on a random batch
  $$ x_{t+1} = x_t - \eta_t \grad f(x_i) $$
  
* [adagrad](http://akyrillidis.github.io/notes/AdaGrad)
  * better performances after some step threshold, more stable
  * independent on $\eta$
  $$ x_{x+1} = x_t - \eta B_t^{-1} \grad f_i (x_t) $$
  

### feed forward

The flow of information is in the forward direction, supervised without feedback.

We take a matrix $X$ on $nxm$ dimensions and a prediction variable $y$ of $k$ elements.
We select a weight vector $w_1$ with $l_1$ entries and a ReLU function $g_1: \mathbb{R}^l \to \mathbb{R}^l $ so that

$$ (g_1(y)) = max{y_i,0} \qquad z_1 = g_1(w_1\beta + b) $$

The second and third layers have: 

$$ z_2 = g_2(w_2 z_1 + b_2) \qquad z_3 = g_3(w_3 z_2 + b_3) $$

and finally the predicted variable:

$$ \hat y_i = softmax_i(z_3) = \frac{e^{(z_3)_i}}{\sum_j e^{(z_3)_i}}  $$ 

We have therefore to set the parameters: ${w_1, w_2, w_3, b_1, b_2, b_3}$ 


## dense - flatten

*Flatten* From matrix to array

dense(16) + input(5,3) = output(5,16)

input(5,3) + flatten() = input(15) + dense(16) = output(16)

## dropout

Cuts connections when the weight is low, helps against overfitting.

Binary classification

Not performant, dropout 20:

![dropout_20](f/f_lernia/dropout_20.png "dropout_20")

Just about right, dropout 30:

![dropout_30](f/f_lernia/dropout_30.png "dropout_30")

Overfitting, dropout 50:

![dropout_50](f/f_lernia/dropout_50.png "dropout_50")



## history interpretation

Train sistematically above test (overfitting)

## activation functions

Sigmoid / Logistic
Advantages

    Smooth gradient, preventing “jumps” in output values.
    Output values bound between 0 and 1, normalizing the output of each neuron.
    Clear predictions—For X above 2 or below -2, tends to bring the Y value (the prediction) to the edge of the curve, very close to 1 or 0. This enables clear predictions.

Disadvantages

    Vanishing gradient—for very high or very low values of X, there is almost no change to the prediction, causing a vanishing gradient problem. This can result in the network refusing to learn further, or being too slow to reach an accurate prediction.
    Outputs not zero centered.
    Computationally expensive
	
	
TanH / Hyperbolic Tangent
Advantages

    Zero centered—making it easier to model inputs that have strongly negative, neutral, and strongly positive values.
    Otherwise like the Sigmoid function.

Disadvantages

    Like the Sigmoid function
	
	
ReLU (Rectified Linear Unit)
Advantages

    Computationally efficient—allows the network to converge very quickly
    Non-linear—although it looks like a linear function, ReLU has a derivative function and allows for backpropagation

Disadvantages

    The Dying ReLU problem—when inputs approach zero, or are negative, the gradient of the function becomes zero, the network cannot perform backpropagation and cannot learn.
	
	
Leaky ReLU
Advantages

    Prevents dying ReLU problem—this variation of ReLU has a small positive slope in the negative area, so it does enable backpropagation, even for negative input values
    Otherwise like ReLU

Disadvantages

    Results not consistent—leaky ReLU does not provide consistent predictions for negative input values.
	
	
Parametric ReLU
Advantages

    Allows the negative slope to be learned—unlike leaky ReLU, this function provides the slope of the negative part of the function as an argument. It is, therefore, possible to perform backpropagation and learn the most appropriate value of α.
    Otherwise like ReLU

Disadvantages

    May perform differently for different problems.
	

Softmax
Advantages

    Able to handle multiple classes only one class in other activation functions—normalizes the outputs for each class between 0 and 1, and divides by their sum, giving the probability of the input value being in a specific class.
    Useful for output neurons—typically Softmax is used only for the output layer, for neural networks that need to classify inputs into multiple categories.
	
	
Swish

	Swish is a new, self-gated activation function discovered by researchers at Google. According to their paper, it performs better than ReLU with a similar level of computational efficiency. In experiments on ImageNet with identical models running ReLU and Swish, the new function achieved top -1 classification accuracy 0.6-0.9% higher.


## weight decay

[weight decay](https://towardsdatascience.com/this-thing-called-weight-decay-a7cd4bcfccab)

### bias/variance

* bias (underfitting)
* variance (overfitting)

## data augmentation

[data augmentation](https://towardsdatascience.com/data-augmentations-in-fastai-84979bbcefaa)


## batch normalization

[batch normalization](https://machinelearningmastery.com/batch-normalization-for-training-of-deep-neural-networks/)

## GAN

[GAN](https://github.com/eriklindernoren/Keras-GAN)



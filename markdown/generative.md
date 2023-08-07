# Generative neural network

![generative](../f/f_gen/gen_cover.jpg "generative cover")
_painting with ML_


We can construct a class of encoders to transform pictures deciding what transformation we want to have as input and what as output. 

## Model

The model is a gan as per [ref](https://machinelearningmastery.com/how-to-implement-pix2pix-gan-models-from-scratch-with-keras/), [ref1](https://github.com/williamFalcon/pix2pix-keras/), [ref2](https://blockgeni.com/implementing-pix2pix-gan-models-from-scratch-with-keras/), [ref3](https://github.com/hanwen0529/GAN-pix2pix-Keras), [ref4](https://affinelayer.com/pix2pix/), [ref5](https://learnopencv.com/paired-image-to-image-translation-pix2pix/) and further described down below

![gan](../f/f_gen/model_exp.png "gan model")
_sketch of the gan_

## Face cut

We first take a bunch of pictures with people on it. 

![panisperna](../f/f_gen/panisperna.jpg "panisperna")
_I ragazzi di via Panisperna_

We use opencv to detect faces with Haar cascades and we cut and reshape pictures to the size of 360x480.

![panisperna](../f/f_gen/panisperna_face.png "panisperna")
_Face detection and rescaling_

Haar cascade is faulty, one face is not correct, the eyes cascade is even worse

![cascade](../f/f_gen/eye_cascade.png "cascade")
_Faulty eye cascade_

## Filters

For each picture we run a routine to collect metadata and apply different filters: 

* color binary thresholds
* color contours
* color Canny
* gray

![filter](../f/f_gen/image_filter.png "filter")
_series of image filters per image_



## Transformations

In the following we run multiple sequences of training to realize different type of encoders

### autoencoder

First we run an autoencoder (same picture as input and output) to see whether the generative network is good enough to describe the final result

![autoencoder](../f/f_gen/autoencoder.jpg "autoencoder")
_visual result of the autoencoder_

The finaly picture is a bit blurry but fit for the purpose


### gray to colors

First of all we realize our pictures are gray but we want colors. 
The first transformation we apply is to take a set of pictures and train a model from the gray version to the colored one. 

![train_history](../f/f_gen/train_history.png "train history")
_train history for the gray to color transformer_

We run the gray transformer to 200 epochs of 64 batches each.

So we can finally color the b/w pictures

![colored](../f/f_gen/colored.jpg "colored")
_black and white pictured colored_

### color binary thresholds

We apply 3 rgb binary layers and learn the encoder towards the original picture

![bin_color](../f/f_gen/bin_color.png "bin color")
_outputs of the color binary encoder_


### color contours

In this case we add 4 contours per color using 50,100,150,200 as thresholds. 
We see at first that the contours are pretty visible

![color_contour](../f/f_gen/color_contour.jpg "color contour")
_first batches of color contour transformation_

After few hundreds of epochs the effect is nicely smoothed out

![color_contour](../f/f_gen/color_contour2.jpg "color contour")
_late batches of color contour transformation_

### color Canny

A Canny filter doesn't provide enough information as input

![color_contour](../f/f_gen/canny_start.jpg "Canny contour")
_first batches of Canny contour transformation_

After many epochs the results are still poor

![color_contour](../f/f_gen/canny_end.jpg "Canny contour")
_late batches of Canny contour transformation_

### average

We take different subsets of people and compute the average face/expression morphing every picture into another one in the same subset

<video width="320" height="256" controls>
  <source src="../f/f_gen/cat.mp4" type="video/mp4">
</video>

The outcomes converge to an overall average

![average_pic](../f/f_gen/average_pic.png "average pic")
_After few iterations all results look the same_

### noise

We use as input random noise and see what the model has learned as pure generator

## Further trials

[Here](https://intertino.it/viaggi/p/ai_gen.html) is a gallery of notable outcomes from the generators.

[![gen_output](../f/f_gen/gen_output.png "generated output")](https://intertino.it/viaggi/p/ai_gen.html)
_Gallery of notable faces_

## super resolution

[ref](https://dev.to/manishdhakal/super-resolution-with-gan-and-keras-srgan-38ma)


## Model

The model is a gan divided into a **discriminator** and a **generator** which is designed as a autoencoder with different convolution layers

An **autoencoder** is defined by an **encoder** and a **decoder** which are used for image compression and decompression. 

An **encoder** reduces the dimensionality of a picture trying to extract the most relevant information without losing the essential features of the picture. The decoder works in the opposite direction because an encoded picture won't be intelligible. 

The encoder is made of different layers where each comprise the local information into averaged pixels. The typical operation is a **convolution** which convolutes different kernels on a correspondent pixel square (usually 3x3) times the color channels. A cube of 3x3x3 after convolution is represented by a single pixel and the next cube is analyzed moving by few pixels (called stride, usually 2x2).

The subsequent layer can be a **pooling** where the image is downsampled, usually with a maxpooling which is taking the maximum value within the square downsampled.

We introduce additional layers to perform some regularization such as batch normalization to provide a proper scale to the batch in use. Another important habit to prevent overfitting is to use dropout randomly removing connections from the neurons.

The discriminator works as an encoder until it flattens into a categorical axis where to each category a probability is assigned. 



![generator](../f/f_gen/gen_model.png "generator_model")
_sketch of the generator model_

The discriminator takes the image as input and quatify the fakeness of it

![discriminator](../f/f_gen/disc_model.png "discriminator model")
_sketch of the discriminator model_

The gan combines the generator and the discriminator in an adversarial fashion [ref](https://machinelearningmastery.com/how-to-implement-pix2pix-gan-models-from-scratch-with-keras/)

![gan](../f/f_gen/gan_model.png "gan model")
_sketch of the gan_

All the pictures have been resized to 256x320 which is not quite 3/4 but it contains many powers of two (2^8 x 2^6*5) and allows our network to go a bit deeper with the convolution.


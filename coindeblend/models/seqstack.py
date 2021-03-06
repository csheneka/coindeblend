from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import BatchNormalization
from keras.layers import Activation


__all__ = [
    'SeqStack',
    'SeqStack_modular',
    ]


def SeqStack(input_shape):
    """
    Stacked Sequential model
    """
    kernel_size = (3, 3)
    
    
    model = Sequential()

    #Block1 
    model.add(Conv2D(10, kernel_size, activation='relu', padding="same", input_shape=input_shape))
    model.add(MaxPool2D()) 

    #Block2
    model.add(Conv2D(10, kernel_size, activation='relu', padding="same")) 
    model.add(MaxPool2D()) 

    #Block3
    model.add(Conv2D(25, kernel_size, activation='relu', padding="same")) 
    model.add(MaxPool2D()) 

    #Block4
    model.add(Conv2D(25, kernel_size, activation='relu', padding="same"))
    model.add(MaxPool2D()) 

    #Block5
    model.add(Conv2D(100, kernel_size, activation='relu', padding="same")) 

    # To transform a 3D tensor into a vector
    # one needs to flatten it
    model.add(Flatten()) 
    model.add(Dense(256, activation='selu'))
    model.add(Dense(256, activation='selu'))
    model.add(Dense(2, activation='linear'))

    return model



def SeqStack_modular(input_shape,filt_size,depth,
                     filt_dense,depth_dense,
                     activation='relu',activation_dense='selu',
                     kernel_size=(3, 3)):
    """  
    Stacked Sequential model  
    """

    model = Sequential()

    #Encode
    for d in range(0, depth):
        fsize = filt_size * 2 ** d
        model.add(Conv2D(fsize, kernel_size, activation=activation, padding="same", input_shape=input_shape,name='block%d_conv1' % d))
        model.add(MaxPool2D())

        model.add(Conv2D(fsize, kernel_size, activation=activation, padding="same",name='block%d_conv2' % d))
        model.add(MaxPool2D())

    #Middle Layer
    model.add(Conv2D(filt_size * 2 ** depth, kernel_size, activation=activation, padding="same", input_shape=input_shape,name='midblock_conv1'))

    #Dense Layers
    model.add(Flatten())

    for dd in range(0, depth_dense): 
        model.add(Dense(filt_dense, activation=activation_dense,name='dblock%d_conv1' % dd))

    model.add(Dense(2, activation='linear'))    

    return model

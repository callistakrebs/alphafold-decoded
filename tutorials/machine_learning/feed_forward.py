import torch
from torch import nn
import math


def affine_forward(x, W, b):
    """ 
    Implements the forward propagation step of a linear layer.

    Calculates the ouptut of a linear layer by performing a matrix 
    multiplication and bias addition.

    Args:
        x (torch.tensor): Input tensor of shape (N, c_in), 
            where N is the batch size and d is the input dimension.
        W (torch.tensor): Weight matrix of shape (c_out, c_in), 
            where c is the output dimension.
        b (torch.tensor): Bias vector of shape (c_out).

    Returns:
        tuple: A tuple containing:
            * torch.tensor: Output of the layer of shape (N, c_out).
            * tuple: A cache of all values necessary for backpropagation.
    """

    out = None
    cache = None

    ##########################################################################
    # DONE: Implement the forward pass for the affine layer (W*x + b).       #
    #       Consider using torch.einsum to handle the batch dimension.       #
    #       Think about which values you'll need to cache for                #
    #       backward propagation.                                            #
    ##########################################################################

    out = torch.einsum('ni,oi->no', x, W) + b
    cache = (x, W, b)

    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return out, cache


def affine_backward(dout, cache):
    """ Computes the backward pass of a linear layer.

    Args:
        dout (torch.tensor): The upstream gradient of shape (N, c_out).
        cache (tuple): Values for backpropagation, cached during 
            the forward pass.

    Returns:
        tuple: A tuple containing:
            * dx (torch.tensor): Gradient of the input, shape (N, c_in).
            * dW (torch.tensor): Gradient of the weights, shape (c_out, c_in).
            * db (torch.tensor): Gradient of the bias, shape (c_out).
    """

    dx = None
    dW = None
    db = None

    ##########################################################################
    # DONE: Implement the backward pass for the affine layer. Using          #
    #       torch.einsum can simplify the calculations. Pay close attention  #
    #       to the input and output shapes to guide your implementation.     #
    ##########################################################################

    x, W, b = cache
    dx = torch.einsum('ij,nj->ni', W.t(), dout)
    dW = torch.einsum('ni,nj->ij', dout, x)
    db = torch.sum(dout, dim=0)

    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return dx, dW, db


def relu_forward(x):
    """
    Computes the element-wise, out-of-place ReLU function.

    Args:
        x (torch.tensor): Input tensor of any shape.

    Returns:
        tuple: A tuple containing:
            * torch.tensor: Output tensor of the same shape as 'x'
            * tuple: All values needed for backpropagation through the layer.
    """

    out = None
    cache = None

    ##########################################################################
    # DONE: Implement the forward pass for the ReLU layer (max(0, x)).       #
    #       Think about which values you'll need to cache for                #
    #       backward propagation.                                            #
    ##########################################################################

    out = torch.max(x, torch.tensor(0))
    cache = x

    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass through the ReLU function.

    Args:
        dout (torch.tensor): Upstream gradient of the same shape 
            as the sigmoid output.
        cache (tuple): Values for backpropagation, cached 
            during the forward path.

    Returns:
        torch.tensor: Gradient of the input, same shape as 'dout'.
    """

    dx = None

    ##########################################################################
    # DONE: Implement the backward pass for the ReLU layer.                  #
    #       Remember that the function is equal to f(x) = x for positive     #
    #       input and f(x) = 0 for negative input.                           #
    #       We will assume a slope of 0 for the kink at x=0.                 #
    ##########################################################################

    x = cache
    dx = dout * (x > 0).float()

    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return dx


def sigmoid_forward(x):
    """ Computes the element-wise sigmoid function.

    Args:
        x (torch.tensor): Input tensor of any shape.

    Returns:
        tuple: A tuple containing:
            * torch.tensor: Output tensor of the same shape as 'x'
            * tuple: All values needed for backpropagation through the layer.
    """

    out = None
    cache = None

    ##########################################################################
    # TODO: Implement the forward pass for the sigmoid layer.                #
    #       Think about which values you'll need to cache for                #
    #       backward propagation.                                            #
    ##########################################################################

    out = torch.divide(1,(1 + torch.exp(-x)))
    cache = out

    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return out, cache


def sigmoid_backward(dout, cache):
    """Computes the backward pass through the sigmoid function.

    Args:
        dout (torch.tensor): Upstream gradient of the same shape as the 
            sigmoid output.
        cache (tuple): Values for backpropagation, cached during the 
            forward path.

    Returns:
        torch.tensor: Gradient of the input, same shape as 'dout'.
    """

    dx = None

    ##########################################################################
    # TODO: Implement the backward pass for the sigmoid layer.               #
    #       For this, make use of the property                               #
    #       sigmoid'(x) = sigmoid(x) * (1-sigmoid(x))                        #
    #       of the sigmoid function.                                         #
    ##########################################################################
    
    sig_x = cache
    dx = sig_x * (1 - sig_x) * dout
    
    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return dx


def l2_loss(y, y_hat):
    """
    Computes the L2-loss. 

    Args:
        y (torch.tensor): Inferred output, shape (N, num_classes).
        y_hat (torch.tensor): Ground-truth labels, shape (N,).

    Returns:
        tuple: A tuple containing the following values:
            * float: The L2-loss of the inference.
            * torch.tensor: The gradient of y, shape (N, num_classes).
    """

    loss = None
    dy = None

    ##########################################################################
    # DONE: Implement the L2-loss as 1/N * sum((y-y_hat)**2),                #
    #        where N is the batch-size. The labels y_hat are provided        #
    #        as class indices. To be used in the loss formulation,           #
    #        they need to be one-hot encoded. You can use                    #
    #        nn.functional.one_hot for this. In addition to the loss,        #
    #        compute the gradient of the loss w.r.t. y.                      #
    ##########################################################################

    loss = torch.divide(torch.sum((y - nn.functional.one_hot(y_hat, y.shape[1]))**2), y.shape[0])
    dy = 2/y.shape[0] * (y - nn.functional.one_hot(y_hat, y.shape[1]))
    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return loss, dy


def calculate_accuracy(model, input_data, labels):
    """
    Calculates the mean accuracy of the model on the input data.

    Args:
        model: The model that is being tested.
        input_data (torch.tensor): Input tensor of shape (N, c_in)
        labels (torch.tensor): Class labels of shape (N,)

    Returns:
        float: The mean accuracy.
    """

    accuracy = None

    ##########################################################################
    # DONE: Compute the forward pass through the model and calculate the     #
    #        class with highest value in the output. Compute how many times  #
    #        the label agreed with the inferred class on average.            #
    ##########################################################################
    out, _ = model.forward(input_data)
    accuracy = torch.mean((torch.argmax(out, dim=1) == labels).float())

    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

    return accuracy


class TwoLayerNet:

    def __init__(self, inp_dim, hidden_dim, out_dim):
        """
        Initialize a new feed-forward network with two layers.

        Args:
            inp_dim (int): Size of the input.
            hidden_dim (int): Size of the hidden dimension.
            out_dim (int): Size of the output.
        """
        self.params = dict()
        self.grads = dict()

        ##########################################################################
        # DONE: Initialize the weights and biases for the network and add        #
        #        them to self.params. Use the following initialization:          #
        #        * Initialize b1 and b2 as zeros.                                #
        #        * Initialize W1 with He initialization with                     #
        #           std dev sqrt(2/c_in).                                        #
        #        * Initialize W2 with Xavier initialization with                 #
        #           std dev sqrt(2/(c_in+c_out)).                                #
        ##########################################################################

        self.params['b1'] = torch.zeros((hidden_dim,))
        self.params['b2'] = torch.zeros((out_dim,))

        self.params['W1'] = torch.randn((hidden_dim, inp_dim)) * math.sqrt(2/inp_dim)
        self.params['W2'] = torch.randn((out_dim, hidden_dim)) * math.sqrt(2/inp_dim)

        ##########################################################################
        #               END OF YOUR CODE                                         #
        ##########################################################################

    def forward(self, x):
        """
        Computes the forward pass through the model.

        Args:
            x (torch.tensor): Input of shape (N, d).

        Returns:
            A tuple with consiting of the following entries:
                * The output of the model.
                * A cache of all the values necessary for backpropagation.
        """
        
        cache = None
        out = None
        ##########################################################################
        # DONE: Compute the forward pass through the model as follows:           #
        #        Affine - ReLU - Affine - Sigmoid                                #
        #        Collect all the caches in a singular cache for backprop.        #
        ##########################################################################

        out, hidden_cache = affine_forward(x, self.params['W1'], self.params['b1'])
        out, relu_cache = relu_forward(out)
        out, out_cache = affine_forward(out, self.params['W2'], self.params['b2'])
        out, sigmoid_cache = sigmoid_forward(out)

        cache = (hidden_cache, relu_cache, out_cache, sigmoid_cache)
        ##########################################################################
        #               END OF YOUR CODE                                         #
        ##########################################################################

        return out, cache

    def backward(self, dout, cache):
        """
        Computes the backward pass through the model.

        Args:
            dout (torch.tensor): Gradient of the model's output, shape (N, c_out)
            cache (tuple): A tuple consisting of the cached values for backprop.
        """

        ##########################################################################
        # DONE: Implement the backward pass through the model. Store the         #
        #        gradients of the parameters in the grads dict using the same    #
        #        keys as for the parameters.                                     #
        ##########################################################################
        hidden_cache, relu_cache, out_cache, sigmoid_cache = cache
        dx = sigmoid_backward(dout, sigmoid_cache)
        dx,  self.grads['W2'], self.grads['b2'] = affine_backward(dx, out_cache)
        dx = relu_backward(dx, relu_cache)
        dx, self.grads['W1'], self.grads['b1'] = affine_backward(dx, hidden_cache)
        ##########################################################################
        #               END OF YOUR CODE                                         #
        ##########################################################################


def train_model(model, train_data, train_labels, validation_data, validation_labels, n_epochs, learning_rate=1e-3, batch_size=16):
    """
    Optimize a model using gradient descent.

    Args:
        model: The model to optimize. 
        train_data (torch.tensor): Tensor of shape (N, d) 
            containing the data for training.
        train_labels (torch.tensor): Tensor of shape (N,) 
            containing the labels for trainng.
        validation_data (torch.tensor): Tensor of shape (N, d) 
            containing the data for validation.
        validation_labels (torch.tensor): Tensor of shape (N,) 
            containing the labels for validatiovalidation
        n_epochs (int): The number of epochs.
        learning_rate (float, optional): The learning rate 
            for the optimization. Defaults to 1e-3.
        batch_size (int, optional): The batch size 
            for the optimization. Defaults to 16.
    """
    N, d = train_data.shape

    ##########################################################################
    # TODO: Build a training loop for the model with the following steps:    #
    #        * truncate the training data and the labels, so that their      #
    #           size is a multiple of the batch size.                        #
    #        * use torch.split to split the data into batches                #
    #        * loop for n_epochs iterations, in every loop:                  #
    #           - Loop through all batches.                                  #
    #               * compute the forward pass.                              #
    #               * compute the loss and output gradient with l2_loss.     #
    #               * compute the backward pass.                             #
    #               * loop through the models params and update them         #
    #                  based on their gradient.                              #
    #        * compute the accuracy on the training and validation set       #
    #           and print them.                                              #
    ##########################################################################

    length = batch_size * (N // batch_size)
    data_batches = train_data[:length].split(batch_size)
    label_batches = train_labels[:length].split(batch_size)

    for i in range(n_epochs):
        for i,batch in enumerate(data_batches):
            out,cache = model.forward(batch)
            loss,dout = l2_loss(out, label_batches[i])
            model.backward(dout, cache)

            for key, param in model.params.items():
                grad = model.grads[key]
                param -= grad * learning_rate

    train_acc = calculate_accuracy(model, train_data, train_labels)
    val_acc = calculate_accuracy(model, validation_data, validation_labels)

    print(f"Train Accuracy: {train_acc}")
    print(f"Val Accuracy: {val_acc}")
    ##########################################################################
    #               END OF YOUR CODE                                         #
    ##########################################################################

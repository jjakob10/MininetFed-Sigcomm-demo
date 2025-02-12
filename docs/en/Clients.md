# Default Client

## Switching between Trainers

In the client provided with MiniNetFED, one of the features is the ability to choose between the sample Trainers or implement your own Trainer for experiments.

To switch between trainers, access the following file:

```
./client/trainer/__init__.py
```

Edit the name of the file from which you want to import the Trainer and the name of the implemented class.

Example:

```python
from .trainerhar import TrainerHar as Trainer
```

**Important notes:** Do not change **as Trainer**. It ensures that, for any chosen Trainer, other client components will recognize it correctly.

Note also that, as shown, new trainers implemented must be contained in the /client/trainer directory.

## Implementing New Trainers

To create a customized Trainer, it is recommended to use one of the sample Trainers as a base and modify its model, dataset, and data manipulations as desired.

For MiniNetFED to recognize the Trainer as a valid Trainer, at least the following methods must be implemented in the created class:

```python
def __init__(self, ext_id, mode) -> None:
    """
    Initializes the Trainer object with the external ID and operation mode.
    """

def set_args(self, args):
    """
    Defines arguments for the Trainer object when they are passed from the config.yaml file.
    """

def get_num_samples(self):
    """
    Returns the number of training data samples.
    """

def split_data(self):
    """
    Loads the data and divides it into training and test sets.
    Returns the training and test data in the following format:

    return x_train, y_train, x_test, y_test
    """

def train_model(self):
    """
    Trains the model on the training data.
    """

def eval_model(self):
    """
    Evaluates the model on the test data.
    Returns the accuracy of the model as a value between 0 and 1.
    """

def all_metrics(self):
    """
    Evaluates the model on the test data.
    Returns a dictionary of all metrics used by the model.
    """

def get_weights(self):
    """
    Returns the model weights. They can be in any format, provided it matches the aggregation function chosen and the implementation of the update_weights function
    """

def update_weights(self, weights):
    """
    Updates the model weights with the given weights. They can be in any format, provided it matches the aggregation function chosen and the implementation of the get_weights function.
    """

def set_stop_true(self):
    """
    Sets the stop flag of the TrainerHar object to True.
    """
    self.stop_flag = True

def get_stop_flag(self):
    """
    Returns the stop flag of the TrainerHar object.
    """
    return self.stop_flag
```
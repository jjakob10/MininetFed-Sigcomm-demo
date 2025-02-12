# Dependencies Details

## env MiniNetFED

The clients and server provided with the MiniNetFED are as follows:

- numpy
- scikit-learn
- keras
- pandas
- paho-mqtt
- tensorflow

Note, however, that there are many other dependencies. For more details, consult the _requirements.txt_ file in the /scripts folder.

These can be modified according to new Trainers and selection or aggregation functions implemented. For example, if it is necessary to install pytorch for the execution of a new Trainer, you should add the dependency to the requirements.txt file within the scripts folder, delete (if existing) the current _env_, and execute the script again for creating the MiniNetFED client env.

## Analysis Script env

The main dependencies are as follows:

- pandas
- scikit-learn
- matplotlib

**Attention**, this script also includes the necessary dependencies to instantiate a trainer (e.g., tensorflow, keras) in order to make the analysis of data distribution between clients. Therefore, if it is necessary to include some new dependency for the implementation of a new Trainer (e.g., pytorch), it will be necessary to add it also to the analysis tool dependencies if you want to perform the analysis of class distribution of that trainer. In this case, it is necessary to add the new dependency to the _requirements.txt_ file within the /analysis folder, delete the _/env_analysis_ folder and create again that using the script of env creation of the analyzer.
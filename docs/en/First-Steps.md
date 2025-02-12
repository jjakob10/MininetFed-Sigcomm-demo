# First Steps with MiniNetFED

> **Important Note**
> If you're using the OVA file on VirtualBox, skip directly to [Executing MiniNetFED with an example](#executing-mininetfed-with-an-example)

## Cloning the MiniNetFED repository

```bash
git clone -b development https://github.com/lprm-ufes/MininetFed.git
```

## Prerequisites

### Installing ContainerNet

MiniNetFED requires ContainerNet. Before installing it, install its dependencies using the following command:

```bash
sudo apt-get install ansible git aptitude
```

#### Tested version of ContainerNet (recommended)

The recommended version for all MiniNetFED features can be found in the following repository:

```bash
git clone https://github.com/ramonfontes/containernet.git
```

### Installing Docker Engine

Access the official documentation and follow the steps for installing Docker Engine:

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

#### Other versions (not recommended)

If you want to install ContainerNet from other sources, it can be found in the following repositories:

##### Official

```bash
git clone https://github.com/containernet/containernet.git
```

It's essential to use the "Bare-metal installation" method for MiniNetFED to work properly. The installation steps for this version can be found at: https://containernet.github.io/

After installation, skip to the step _Generating Docker images_

#### Installation script (if you're installing the recommended version)

Once you've selected your preferred installation location, clone or decompress the containernet files and follow these commands:

```bash
cd containernet
```

```bash
sudo util/install.sh -W
```

## Generating Docker Images

MiniNetFED also depends on some pre-configured Docker images.

Use the following commands to create these images:

```bash
cd MininetFed
```

```bash
sudo ./docker/create_images.sh
```

## Creating the environment with dependencies

To create the environments with dependencies for running an example, use the script to manage environments. Environments will be created for the server, clients, and analysis script, installing all necessary dependencies. The resulting environments will be in the `envs/` folder.

Creating environments for containerized devices:

```bash
sudo python scripts/envs_manage/create_container_env.py -c envs_requirements/container/client_tensorflow.requirements.txt envs_requirements/container/server.requirements.txt -std
```

Creating environment for analysis script:

```bash
sudo python scripts/envs_manage/create_container_env.py -l requirements/local/analysis.requirements.txt -std
```

## Executing MiniNetFED with an example

To test if everything is working correctly, you can run one of the configuration files in the **exemplos** directory. Choose a file from the examples folder and execute it.

```bash
sudo python3 main.py examples/<example name>/config.yaml
```

> ### Example Trainer Har with fed_sec_per and fed_avg
>
> ```bash
> sudo python3 main.py examples/har_fed_sec_per/config.yaml
> ```

If everything is working, the experiment should start executing, opening the following windows:

- Broker MQTT
- Server
- Network monitor
- N clients, where N is the number of clients in the experiment

After the experiment finishes running, a new folder named **experiments** will be created inside the example folder containing the experiment's results.

# Analyzing the first experiment

Inside the example folder, there is an **analysis.yaml** file. To run it, activate the environment for the analysis script first:

```bash
. env_analysis/bin/activate
```

Modify and execute the following command:

```bash
python3 analysis.py examples/<example name>/analysis.yaml
```

> ### Example Trainer Har with fed_sec_per and fed_avg
>
> ```bash
> python3 analysis.py examples/har_fed_sec_per/analysis.yaml
> ```

Note: This translation is based on the provided text. If you need any adjustments or have specific requirements, please let me know.
# Support Scripts

MiniNetFED is distributed with some support scripts. The function of each will be explained below.

## clean.sh

```bash
scripts/clean.sh
```

If the MiniNetFED execution is interrupted incorrectly, Containernet or Docker may leave behind instances of network elements or Docker containers respectively. If another execution of MiniNetFED is initiated, there may be errors or warnings. In this case, the clean.sh script deletes all active Docker containers and performs Containernet cleanup.

**Note**: The script will delete all instantiated Docker containers, so if there's another application on the machine using Docker containers, it may be affected. In this case, it is recommended to manually delete the containers instantiated by MiniNetFED, and then use the following command only to clean up Containernet:

```bash
sudo mn -c
```

## Environment Manager

```bash
sudo python3 scripts/envs_manage/create_container_env.py [-c|-l] req/folder|exemplo.requirements.txt ... -std|image_name
```

The `-c` flag indicates that the environment will be created to run in a container, and `-l` for execution on the local machine. You can then pass either the path to a folder or the paths to multiple requirement files. Finally, pass the `-std` flag to use the default container image or the name of the image.

**Important**: The file must end with `.requirements.txt`. For example: `meu_env.requirements.txt`.

The purpose of this script is to assist in creating Python environments used by MininetFed.

MininetFed already follows some `requirements.txt` files within the `envs_requirements/local` folder for local machine execution and `envs_requirements/container` for container execution.

The default destination folder is `envs/`.

During MininetFed setup, it's interesting to instantiate the `clients.requirement` environments.

To instantiate all local environments provided, you can execute the following command:

```bash
sudo python3 scripts/envs_manage/create_container_env.py -l envs_requirements/local -std
```

To instantiate your own environments with additional dependencies for the algorithms you implemented, you can run the script as follows:

```bash
sudo python3 scripts/envs_manage/create_container_env.py -c meu/req/exemplo.requirements.txt -std
```
# Configurações da execução

A maior parte das configurações do experimento são passadas para o MininetFed por meio do arquivo `topology.py` que segue o padrão do Mininet.

```jsx
sudo python3 topology.py
```

É possível editar o arquivo deixado na pasta do MininetFed como exemplo ou criar seu próprio.

Alguns elementos básicos que existem relacionados com o MininetFed são os seguintes

```python
from federated.node import Server, Client
from federated.net import MininetFed
```

## MininetFed

Instancia uma rede Mininet com alguns componentes básicos já incluidos. Esses são os seguintes:

- broker mqtt (mosquitto)
- monitor de rede
- autostop
- controlador de experimento

### broker mqtt

Busca por padrão o arquivo de configurações `mosquitto.conf` na pasta raiz do MininetFed

### monitor de rede

Consome dados da rede para gerar um log que pode ser usado durante a análise do experimento

### autostop

Utilitário que sincroniza a execução dos dispositivos durante o aprendizado federado, garantindo que a execução do código principal `topology.py`.

---

### _broker_image:_

Imagem que será utilizada para instanciar um container docker para o broker MQTT. É recomendado usar a imagem padrão já fornecida com o MiniNetFED, mas é possível criar o seu próprio broker mqtt customizado modificando essa opção.

### _experiments_folder:_

Onde são criadas as pastas de cada experimento.

## Experiment

```jsx
experiment:
  new_experiment: (true ou false)
  experiment_name: (string)
  trainer_mode: (string)
  max_n_rounds: (int)
  stop_accuracy: (float tal que 0 <= n <= 1)
  min_trainers: (int)
```

### _new_experiment:_

Define se deseja que o MiniNetFED crie automaticamente uma nova pasta para o experimento ou continue a preencher a pasta de um experimento já existente

**True:**

Busca ou cria um diretório para o experimento da seguinte forma:

```bash
(experiments_folder)/YYYY_MM_DD_(experiment_name)
```

**False:**

Busca o diretório do experimento pelo nome.

Note que nesse caso o diretório não existir, o MiniNetFED apresentará erro.

```bash
(experiments_folder)/(experiment_name)
```

### _experiment_name:_

O nome do experimento para referenciar a pasta onde será colocado os resultados dele.

### _trainer_mode:_

Essa opção é entregue diretamente ao Trainer. Seleciona modos pré-definidos de divisão dos dados e modos de operação do Trainer.

### _max_n_rounds:_

Essa opção é passada para o server para definir o número máximo de rounds de comunicação entre o servidor e o cliente, definindo uma condição de parada.

### _stop_accuracy:_

Essa opção define uma condição de parada baseada na acurácia média do modelo gerado pela combinação dos modelos gerados por cada trainer.

### _min_trainers:_

Define o número mínimo de clientes conectados antes de inicializar o treinamento.

### Nota:

A condição de parada que for atingida primeiro será a responsável por interromper a execução. A causa da parada será registrada no log de treinamento.

## Network

```jsx
network_monitor_script: string;
network_monitor_image: string;
network_components: int;
```

### _network_monitor_script_

Endereço do script do monitor de rede. Use o script padrão deixado no arquivo de exemplo ou modifique para criar um monitor customizado.

### _network_monitor_image_

Imagem utilizada no container do monitor de rede. Use a imagem padrão deixada no arquivo de exemplo ou modifique para criar um monitor customizado.

### _network_components_

Número de switch na rede para a criação de topologias de rede complexas. Em uma rede simples, deixe o valor como “1”

## Server

```jsx
  memory: (int)m
  vCPU_percent: (int 0 - 100)
  image: (string)
  volume: (string)
  conection: (int)
  script: (string)
```

### _memory:_

Quantidade de memória máxima a ser usada pelo docker do server

### _vCPU_percentage:_

Porcentagem do poder de processamento disponível dediada ao sever. Para mais detalhes, consulte a seção sobre vCPU na documentação

### _image:_

Imagem docker a ser usada no servidor. Use a imagem padrão deixada no arquivo de exemplo ou modifique para criar um servidor customizado.

### _Connection:_

Define à qual switch você deseja conectar o servidor. O valor é um número de 1 a N que representa o id do swtich. Essa opção é utilizada para criar topologias de rede mais complexas.

### _Script:_

Endereço do arquivo de execução do servidor.

## Clients

Essa opção é dedicada à definir um ou mais tipos de clientes para serem instanciados durante o experimento.

A estrutura de _clients_ compreende uma lista com os tipos de clientes

```jsx
Clients:
-   amount: (int)
    name: (string)
    memory: (string)m
    vCPU_percent: (int 0 - 100)
    image: (string)
    script:(string)
    connection: (int)
    loss: (float 0 <= n <= 1)
    delay: (int)ms
    bw: (int)

  - (outro tipo de cliente)
...
```

### _amount_

Quantidade de clientes do tipo atual que serão instanciados durante a execução do experimento

### _name_

Nome do tipo de cliente. Não use espaço ou caracteres especiais. Em caso de problemas durante a instanciação, cheque se não foi utilizado um nome com caracteres proibidos.

### _memory_

Quantidade de memória máxima a ser usada pelo docker do server

### _vCPU_percentage:_

Porcentagem do poder de processamento disponível dediada a cada instância de cliente. Para mais detalhes, consulte a seção sobre vCPU na documentação

### _image:_

Imagem docker a ser usada no cliente. Use a imagem padrão deixada no arquivo de exemplo ou modifique para criar um cliente customizado.

### _Script:_

Endereço do arquivo de execução do cliente do tipo atual.

### _Connection:_

Define à qual switch você deseja conectar o cliente do tipo atual. O valor é um número de 1 a N que representa o id do swtich. Essa opção é utilizada para criar topologias de rede mais complexas. Por exemplo, um tipo de cliente pode ser conectado ao switch 1, e um outro tipo pode ser conectado ao switch 2, e entre o switch 1 e o 2 existe um delay, um bandwidth, e um loss pré definido.

### _loss_

É a porcentagem de perda de dados entre o cliente e o switch no qual ele está conectado.

### _delay_

É o delay em milisegundos que a conexão entre o switch e o cliente terá

### _bw_

Largura de banda entre o cliente e o switch ao qual ele está conectado. A unidade padrão é Mbps.

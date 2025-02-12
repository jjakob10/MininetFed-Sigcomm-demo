# Primeiros passos com o MiniNetFED

> **Nota importante**
> Caso esteja utilizando o arquivo OVA no VitrualBox, pule diretamente para [Executar o MiniNetFED com um exemplo](#executar-o-mininetfed-com-um-exemplo)

## Clonando o repositório do MiniNetFED

```
git clone -b development https://github.com/lprm-ufes/MininetFed.git
```

## Pré requisitos

<!-- ### Instalar o docker engine

Acesse a documentação oficial e siga os passos para a instalação do docker engine:

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository -->

### Instalar ContainerNet

O MiniNetFED necessita do ContainerNet. Antes de instala-lo, instale as suas dependências usando o seguinte comando

```
sudo apt-get install ansible git aptitude
```

#### Versão do ContainerNet testada (recomendado)

A versão recomendada para o uso de todas as funcionalidade do MininetFed pode ser encontrada no seguinte repositório:

```
git clone https://github.com/ramonfontes/containernet.git
```

<!-- A versão usada do ContainerNet está em um arquivo .zip na pasta **containernet** do repositório do MiniNetFED. Copie esse arquivo .zip e cole ele no lugar onde deseja instalar o ContainerNet na sua máquina -->

<!-- > #### Outras versões (não recomendado)
>
> Caso deseje instalar o ContainerNet de outras fontes, ele pode ser encontrado nos seguintes repositórios
>
> ##### Oficial
>
> ```
> git clone https://github.com/containernet/containernet
> ```
>
> É importante que o método de instalação seja "Bare-metal installation" para que o MiniNetFED funcione adequadamente
> Os passos de instalação dessa versão podem ser encontrados no seguinte link: https://containernet.github.io/
> Após a instalação, pule para o passo _Gerando as imagens docker_ -->

#### Script de instalação (caso você estiver instalando a versão recomendada)

<!-- FALTA INCLUIR COMANDOS PARA A INSTALAÇÃO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

Uma vez selecionado o local de instalação de sua preferência, clone ou decompacte os arquivos do containernet e siga com os seguintes comandos

```shell
cd containernet
```

```shell
sudo util/install.sh -W

```

## Gerando as imagens docker

O MiniNetFED também depende de algumas imagens docker pré configuradas.

Utilize os comandos a seguir para criar essas imagens.

```bash
cd MininetFed
```

<!-- ```bash
sudo docker build --tag "mininetfed:broker" -f docker/Dockerfile.broker .
sudo docker build --tag "mininetfed:client" -f docker/Dockerfile.container .

``` -->

```bash
sudo ./docker/create_images.sh
```

<!-- "mininetfed:broker", "mininetfed:container", "mininetfed:client" e "mininetfed:server" são os nome das imagens. -->

## Criando o env com as respectivas dependências

Para criar os _envs_ com as dependências para executar o exemplo, utilize o script de gerenciamento de ambientes. Serão criados os ambientes que serão utilizados pelo servidor, pelos clientes, e pelo script de análise, instalando todas as dependências necessárias. Os _envs_ resultantes estarão na pasta `envs/`.

<!-- Criando os _envs_ para os dispositivos conteinerizados:

```bash
sudo python scripts/envs_manage/create_container_env.py -c envs_requirements/container/client_tensorflow.requirements.txt envs_requirements/container/server.requirements.txt -std
``` -->

Criando _env_ para o script de análise:

```bash
sudo python scripts/envs_manage/create_container_env.py -l requirements/local/analysis.requirements.txt -std
```

<!-- # Executar o MiniNetFED com um exemplo

Para testar se tudo está funcionando adequadamente, é possível executar um dos arquivos de configuração do diretório **exemplos**. Escolha um dos exemplos da pasta e execute.

```
sudo python3 main.py examples/<nome do exemplo escolhido>/config.yaml

```

> ### Exemplo Trainer Har com fed_sec_per e fed_avg
>
> ```
> sudo python3 main.py examples/har_fed_sec_per/config.yaml
> ```

Se tudo estiver funcionando, o experimento deve começar a executar abrindo as seguintes janelas:

- Broker MQTT
- Servidor
- Monitor de rede
- N clientes, onde N é o número de clientes do experimento

Após a execução do experimento, é esperado que haja uma nova pasta dentro de **experiments** contendo os resultados do experimento.

# Fazendo a análise do primeiro experimento

Dentro da pasta do exemplo, há o arquivo **analysis.yaml**. Para executa-lo, primeiramente ative o ambiente python do script de análise

```
. env_analysis/bin/activate
```

modifique o comando a seguir e execute-o:

```
python3 analysis.py examples/<nome do experimento>/analysis.yaml
```

> ### Exemplo Trainer Har com fed_sec_per e fed_avg
>
> ```
> python3 analysis.py examples/har_fed_sec_per/analysis.yaml
> ``` -->

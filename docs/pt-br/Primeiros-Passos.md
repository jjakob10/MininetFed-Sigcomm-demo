# Primeiros passos com o MiniNetFED

> **Nota importante**
> Caso esteja utilizando o arquivo OVA no VitrualBox, pule diretamente para [Executar o MiniNetFED com um exemplo](#executar-o-mininetfed-com-um-exemplo)

## Clonando o repositório do MiniNetFED

```
git clone -b development https://github.com/lprm-ufes/MininetFed.git
```

## Pré requisitos

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

#### Script de instalação (caso você estiver instalando a versão recomendada)

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

```bash
sudo ./docker/create_images.sh
```

## Criando o env com as respectivas dependências

Para criar os _envs_ com as dependências para executar o exemplo, utilize o script de gerenciamento de ambientes. Serão criados os ambientes que serão utilizados pelo servidor, pelos clientes, e pelo script de análise, instalando todas as dependências necessárias. Os _envs_ resultantes estarão na pasta `envs/`.

Criando _env_ para o script de análise:

```bash
sudo python scripts/envs_manage/create_container_env.py -l requirements/local/analysis.requirements.txt -std
```

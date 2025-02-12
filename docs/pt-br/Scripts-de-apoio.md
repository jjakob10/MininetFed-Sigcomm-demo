# Scripts de apoio

O MiniNetFED é distribuido com algum scripts de apoio. A seguir a função de cada um será explicada

# clean.sh

```bash
scripts/clean.sh
```

Caso a execução do MiniNetFED seja interrompida indevidamente, o Containernet ou o docker poderão deixar instâncias de elementos de rede ou containers dockers para trás respectivamente. Se outra outra execução do MiniNetFED for iniciada, pode haver erros ou avisos. Nesse caso, o script clean.sh deleta todos os containers docker ativos e executa a limpeza do Containernet.

**Atenção**: O script irá deletar todos os containers docker instanciados, portanto se houver outra aplicação na máquina que utilize containers dockers, ela possivelmente será afetada. Nesse caso é recomendado a deleção manual dos containers instanciados pelo MiniNetFED, e após usar o comando a seguir para apenas limpar o Containernet.

```bash
sudo mn -c
```

# Gerenciador de environments

```bash
sudo python3 scripts/envs_manage/create_container_env.py [-c|-l] req/folder|exemplo.requirements.txt ... -std|image_name
```

A flag `-c` indica que o ambiente será criado para rodar em um container, e `-l` para se executado na máquina local. Em seguida pode ser passado ou o endereço de uma pasta, ou o endereço de múltiplos arquivos de requirements. Por último, é passada a flag `-std` para utilizar a imagem padrão do container ou o nome da imagem.

**Importante**: Para ser reconhecido, o arquivo deve terminar com `.requirements.txt`. Exemplo: `meu_env.requirements.txt`.

O objetivo desse script é auxiliar na criação dos _environments_ python usandos pelo MininetFed.

O MininetFed acompanha já alguns arquivos de `requirements.txt` dentro da pasta `envs_requirements/local` para ambientes executados pela máquina locao e `envs_requirements/container` para ambientes executados em containers.

A pasta destino é por padrão `envs/`.

Durante o setup do MininetFed, é interessante instanciar os ambientes `clients.requirement`

Para instanciar todos os ambientes locais fornecidos, pode se executar o seguinte comando

```bash
sudo python3 scripts/envs_manage/create_container_env.py -l envs_requirements/local -std
```

Para instaciar os seus próprios ambientes contendo dependências adicionais para os algoritmos que você implementou, você pode executar o script da seguinte forma

```bash
sudo python3 scripts/envs_manage/create_container_env.py -c meu/req/exemplo.requirements.txt -std
```

<!-- # create_env.py

```bash
sudo python3 scripts/create_env.py <imagem docker usada para o cliente> <requirements.txt>
```

O script que cria o _env_ instancia um container docker usando a imagem do cliente do MiniNetFED para que os clientes sejam compatíveis com o _env_ criado. Como o _env_ é criado partindo de um container, não é necessário ter instalado na máquina o _venv_ para python. O script também recebe o arquivo _requirements.txt_, o qual também está na pasta /scripts.

# env_analysis.sh

Assim como o script anterior, esse script cria um _env_ python, mas há algumas diferenças. Nele o _env_ é criado pela e para a própria máquina em que é executado, e não é necessário fornecer nenhuma informação adicional. Ele já busca automaticamente o arquivo de requirements.

Um ponto importante é que esse script necesita do _venv_ para python, e se o mesmo não estiver disponível, ele será autimaticamente instalado.

```bash
./scripts/env_analysis.sh
``` -->

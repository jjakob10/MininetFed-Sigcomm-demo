# Passos de reprodutibilidade

**Requisitos**

- Ubuntu LTS +20.04 (22.04 - preferable)
- Containernet - https://github.com/ramonfontes/containernet
- +6.0.0 kernel
- MininetFed - https://github.com/lprm-ufes/MininetFed/tree/development

## Instalação do MininetFed

Siga o passo-a-passo descrito na documentação para instalar o MininetFed na máquina local com a versão do Containernet recomendada.

<!-- > Atenção: Vá até antes da seção "Executar o MininetFED com um exemplo". A versão atual do MininetFed **não** é retrocompatível com o sistema de .yaml e os exemplos antigos ainda não foram atualizados. -->

<!-- > Note: Para fazer o git clone do reposeitório, use o comando a seguir ao invez do sugerido na documentação
>
> ```shell
> git clone -b development https://github.com/lprm-ufes/MininetFed.git
> ``` -->

- [Primeiros Passos](docs/pt-br/Primeiros-Passos.md)

## Executando experimentos

## Seleção de Todos os Clientes (all)

Executar o arquivo topology_all.py utilizando o script de execução conforme mostrado a baixo

```shell
sudo python3 topology.py [--case_all|--case_random|--case_energy]
```

Após executar o comando, a rede e os dispisitivos serão instanciados. Após alguns segundos, múltiplas janelas do Xterm serão abertas como na figura a seguir

<img align="center" src="https://github.com/lprm-ufes/MininetFed-LoWPAN/blob/topology-unico/images/terminais.png" width="600" alt=""/>

No terminal onde o comando foi executado, aparecerá a mensagem _Waiting for messages_ que indica que o Mininetfed está esperando pela mensagem de finalização do experimento.

<img src="https://github.com/lprm-ufes/MininetFed-LoWPAN/blob/topology-unico/images/terminal.png" alt=""/>

Após finalizar a execução do experimento, os seguintes arquivos estarão no diretório `sbrc/sbrc_mnist_select_[all|random|energy]`

<img src="https://github.com/lprm-ufes/MininetFed-LoWPAN/blob/topology-unico/images/arquivos.png" alt=""/>

## Gráfico de Consumo de Energia Acumulado

```shell
. envs/analysis/bin/activate
```

```shell
python analysis.py casos_de_uso/sbrc_2025/energia_all.yaml casos_de_uso/sbrc_2025/energia_random.yaml casos_de_uso/sbrc_2025/energia_energy.yaml
```

## Gráfico do Impacto no Desempenho do Treinamento

> Caso tenha pulado o passo anterior
>
> ```shell
> . envs/analysis/bin/activate
> ```

```shell
python analysis.py casos_de_uso/sbrc_2025/desempenho.yaml
```

# Solução de problemas

Caso algum problema ocorra durante a execução, use o seguinte comando para deletar os containers e limpar o mininet:

```shell
./script/clean.sh
```

Após a limpeza, tente executar novamente.

> Aviso importante: O script de limpesa possivelmente afetará outros containers docker em execução na mesma máquina que **não** tem relação com o MininetFed.
>
> Garanta de antemão que não há nada importante executando em containers antes de prosseguir com a execução do script.

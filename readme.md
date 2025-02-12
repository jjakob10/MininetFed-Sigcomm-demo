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

## Seleção de Todos os Clientes (all)

Executar o arquivo topology_all.py utilizando o script de execução conforme mostrado a baixo

```shell
sudo ./main.sh casos_de_uso/sbrc_2025/topology_all.py
```

Os resultados da execução estarão no diretório `sbrc/sbrc_mnist_select_all`

## Seleção Aleatória (random)

```shell
sudo ./main.sh casos_de_uso/sbrc_2025/topology_random.py
```

Os resultados da execução estarão no diretório `sbrc/sbrc_mnist_select_random`

## Seleção Considerando o Consumo de Energia (energy)

```shell
sudo ./main.sh casos_de_uso/sbrc_2025/topology_energy.py
```

Os resultados da execução estarão no diretório `sbrc/sbrc_mnist_select_energy`

## (Alternativa) Executar os 3 de uma só vez

```shell
sudo ./main.sh casos_de_uso/sbrc_2025/topology_all.py casos_de_uso/sbrc_2025/topology_random.py casos_de_uso/sbrc_2025/topology_energy.py
```

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

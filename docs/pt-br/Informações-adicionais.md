# Detalhamento das dependências

## env MiniNetFED

Os clientes e o server fornecidos juntos com o MiniNetFED são as seguintes

- numpy
- scikit-learn
- keras
- pandas
- paho-mqtt
- scikit-learn
- tensorflow

Note, no entanto, que há muitas outras dependências. Para mais detalhes consulte o arquivo _requirements.txt_ na pasta /scripts.

As mesmas podem ser modificadas de acordo com novos Trainers, e funções de seleção ou agregação implementadas. Por exemplo, se for necessário a instalação do pytorch para a execução de um novo Trainer, deve-se adicionar a dependência ao arquivo de requirements.txt dentro da pasta scripts, deletar (se existir) o _env_ atual, e executar novamente o script de criação de _env_ para o cliente MiniNetFED.

## env script de análise

As principais dependências são as seguintes:

- pandas
- scikit-learn
- matploylib

**Atenção**, esse script também inclue as dependências necessárias para instanciar um trainer (ex.: tensorflow, keras) para poder fazer a análise da distribuição dos dados entre os clientes. Logo, se for necessário incluir alguma nova dependências para a implementação de um novo Trainer (ex.: pytorch), será necessário inclui-la também nas dependências do analisador se for desejado fazer a análise da distribuição de classes desse trainer. Nesse caso, é necessário incluir a nova dependência no arquivo _requirements.txt_ dentro da pasta **/analysis**, apagar a pasta _/env_analysis_ e criar novamente essa utilizando o script de criação de env do analisador.

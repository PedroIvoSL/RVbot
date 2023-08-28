# Guia de Instalação e Configuração do RVbot

Este guia irá auxiliá-lo na instalação e configuração do RVbot para automatizar processos envolvendo web scraping e manipulação de dados. O RVbot é desenvolvido em Python e depende de várias bibliotecas e dependências.

## Pré-requisitos

Antes de continuar com a instalação, certifique-se de ter os seguintes pré-requisitos instalados em seu sistema:

- **Python**: Certifique-se de ter o Python instalado. Você pode baixá-lo no site oficial [Python](https://www.python.org/downloads/).

## Passos de Instalação

1. **Clonar o Repositório**: Abra um terminal ou prompt de comando e navegue até o diretório onde deseja instalar o RVbot. Execute o seguinte comando para clonar o repositório:

   ```sh
   git clone https://github.com/PedroIvoSL/RVbot
   ```
Substitua seu-nome-de-usuário pelo seu nome de usuário da SINQIA e seu-repo-rvbot pelo nome do seu repositório
## Instalar as Dependências
Instale as dependências necessárias a partir do arquivo 'requisitos.txt':

   ```sh
   pip install -r requisitos.txt
```
## Configurar o Bot
Abra o arquivo seu-script-rvbot.py em um editor de texto. Considere renomear o arquivo para um nome mais descritivo.

## Fornecer Credenciais
No script, localize a função credencial e forneça suas credenciais de login para o site relevante:
   ```python
   credencial('SeuNomeDeUsuário', 'Usr')
   credencial('SuaSenha', 'Pwd')
```
# Uso
## Executar o Bot
No terminal ou prompt de comando, ainda no diretório do projeto, execute o script:
```sh
 python RV2.0.py
```
## Escolher uma Opção
### O bot apresentará um menu com opções. Escolha a opção relevante com base nos seus requisitos:
Opção 1: Inicia o código principal para processamento de dados.

Opção 2: Lista os códigos RV disponíveis.

Opção 3: Encerra o programa.

# Conclusão
Você instalou e configurou com sucesso o RVbot. Agora você pode usá-lo para automatizar tarefas de web scraping e manipulação de dados.

# Projeto_FacensTCC_2020
Esse projeto é um TCC sobre jogo da forca usando Libras, com objetivo de ensina o alfabeto de Libras apartir da gameficação.

-----------------------------------

## Recursos necessários:
 1. Uma *webcam*;
 2. Python 3.6.8;
 3. As bibliotecas de python que pode ser encontrado no *requirements*, não é necessario as duas biblioteca ao mesmo tempo;
    - requirements.txt para utilizar a Rede Neural via CPU
    - requirements_gpu.txt para utilizar a Rede Neural via GPU
 4. Fundo Branco (pode ser um pano branco ou uma parede branca);
 5. Luva com os dedos coloridos, conforme a imagem abaixo.
 
 **Imagem**
 
-----------------------------------

## Estrutura do codigo
A estrutura dos script pode se organizado em duas categorias:
 - **Jogo da forca** (o objetivo principal deste projeto)
 - **Rede Neural** (script de treinamento, coleta de dados, testes com a rede neural e etc...)

### Jogo da forca
**JogoDaForca/JogoDaForca.py:** O codigo principal do jogo, ele deve ser [execultado para iniciar o jogo.]

**JogoDaForca/CameraDeduz.py:** Um codigo auxilia sado pelo JogoDaForca/JogoDaForca.py, utilizado para enviar uma resposta da rede neural, no caso qual sinal do alfabeto de Libras foi representado na camera. 

**JogoDaForca/imagens/..:** Imagens utilizadas no jogo.

### Rede Neural

**redeNeural/Treinamento.py:** Script do treinamento da Rede Neural (SqueezeNet) e o local onde será localizado o arquivo da Rede Neural, incluido graficos de perca e accuracia.

**salvaDataset.py:** Captura as imagens utilizadas para o treinamento da Rede Neural e já realiza a organização dela.

**predict.py:** Prediz o resultado da imagem, usado afins de teste exclusivamente para Rede Neural.

**matrix.py:** Um script para gerar uma matrix de confusão, afins de avaliar a rede neural.

-----------------------------------

## Como jogar:
Antes de iniciar verifique se o arquivo **RedeNeural/CORRIGIRONOME** se encontra no local, caso não esteja descopacte **RedeNeural/RedeNeural_CORRIGIRONOME** dentro da pasta RedeNeural.

Para iniciar deve ser execultado o **JogoDaForca/JogoDaForca.py**.

### Menu Principal:
O Menu principal do jogo, onde o usuario terá duas escolhas:
- Sortia uma palavra pelo sistema. 
- Digita uma palavra, pode ser utilizado para teste e/ou como um segundo jogador, após o click, a palavra deve ser digitado no console. É recomendando uma palavra com no maximo 10 letras, não deve ser inserido letras com acentos e Ç.

**IMAGEM**

### Jogo: VERIFICARNOME
Nesta tela, o usuario poderá vizualizar suas tentativas (pela imagem), quais letras acerto ou errou. Quando usuario for tenta deduzir uma letra, deve ser apertado o botão **NOME**, que irá direciona o usuario para tela Tentativa.

**IMAGEM**

O usuario pode desistir da partida apertando "Escape".

### Tentativa:
Nesta tela, o usuario realiza o sinal do alfabeto de Libras, é necessario que o usuario mantenha o sinal até ser confirmado a letra escolhida.

**IMAGEM**

--------------
- [ ] Coloca imagens e gifs
- [ ] Ajeita nomes
- [ ] Creditos

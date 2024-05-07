# Explicação

## Decisão da arquitetura utilizada

Bom, a princípio decidi separar o código em 3 frentes:
- Core: Códigos utilizados como base do programa, nesta pasta estão classes ligadas
ao chat, modelos de IA e utilitários;
- Database: Códigos relacionados diretamente á construção e utilização do banco
de dados;
- GUI: Códigos relacionados a construção e utilização da interface;

Além disso, algumas decisões foram tomadas:
- Construir meu próprio controlador de Chat: Preferi não utilizar nenhuma biblioteca
nesta parte para não construir um gargalo ou instalar mais dependências desnecessárias.
Nessa parte eu considera a lógica trivial, então optei por implementar meu próprio
esquema de chat e histórico.
- Utilizar modelos localmente: Apesar do Whisper e do Llama serem modelos moderadamente
pesados, eu optei por usá-los por não possuir nenhuma chave de alguma API externa
em que eu pudesses fazer requisiçoes. Se isso fosse possível, o sistema teria uma
complexidade muito menor e rodaria em qualquer máquina, o que infelizmente não é
o caso.
- Utilizar o modelo Llama3: Como andava experimentando com este modelo e seu lançamento
foi bem recente, decidi utilizá-lo, por uma simples vontade de explorar mais suas
capacidades, porém tendo completa noção que ele torna a execução do programa quase
impossível em certas máquinas. Em questão desse peso também, foi utilizado uma versão
menor do Llama3, que foi *quantizada* em 4 bits.
- Construir minha interface em Python: O projeto tem um escopo amplo, e creio que,
numa visão de produto e dia a dia o ideal é que a interface fosse construída em react 
ou outro framework que pudesse rodar em um servidor. Porém, com todo o peso do modelo
para rodar apenas uma conversa, decidi fazer um chat único e local. Assim não precisamos
sobrecarregar a máquina com um servidor rodando e possíveis múltiplas requisições de
usuários.

## Lista de bibliotecas de terceiros utilizadas

- mimetypes
- pytesseract
- pypdf
- moviepy
- chevron
- langchain
- hugginface_hub
- llama_cpp
- torch
- whisper
- customtkinter

## O que você melhoraria se tivesse mais tempo

Visando um objetivo de ser um projeto de escopo online, com mais tempo e a disponibilidade
de chaves para serviços externos, eu utilizar uma interface web e eliminaria algumas
preocupações, como por exemplo implementar meu próprio controlador de chat. Além disso, 
otimizaria a construção de banco de dados para operar em várias threads.

Os embeddings utilizados também poderiam ser melhorados, visto que usei um modelo
simples para a agilidade do processo (que já é lento por conta da transcrição do whisper).

Por último, adicionaria suporte para mais tipos de arquivos, já que o escopo dado
foi bem limitado.

## Quais requisitos obrigatórios que não foram entregues

Creio que, de todos requisitos obrigatórios, a única parte que não foi realmente
completa foi a análise da imagem. Com modelos que tem essa capacidade e respondem
em tempo viável (como o GPT-4 Turbo), poderíamos extrair o texto das imagens assim
como a descrição dos elementos ou qualquer outro detalhe presente. O implementado
foi uma simples extração de texto de uma imagem.
---
title: ABOUT PAGE
layout: template
filename: about.md
--- 

# Como rodar
## Instalaçoes necessárias
Primeiro, é necessário instalar o *Tesseract* para extração de textos em imagens. 
Isso pode ser feito com o seguinte comando: `sudo apt install tesseract-ocr`

Além disso, será necessário instalar o *ffmpeg* com o comando `sudo apt install ffmpeg`

Para uma melhor performance também é recomendado o nvcc: `sudo apt install nvidia-cuda-toolkit`
Seguido de uma instalação limpa do llama-cpp:`CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir`
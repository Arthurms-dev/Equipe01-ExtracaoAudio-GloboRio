# Equipe01-ExtracaoAudio-GloboRio

# Sistema de Extração de Áudio e Vídeo

## Visão Geral
Este projeto tem como objetivo desenvolver uma aplicação em **Python** para **extração e processamento de áudio e vídeo**, utilizando a ferramenta **FFmpeg**.  
Principais funcionalidades:
- Separação da trilha de áudio
- Remoção de ruídos

## Equipe
- **Desenvolvedores (5):** responsáveis pela implementação das funcionalidades
- **Product Owner (PO):** responsável por definir prioridades e backlog
- **Scrum Master:** garante a aplicação das práticas ágeis e remoção de impedimentos

## Tecnologias 
- [Python](https://www.python.org/) 
- [FFmpeg](https://ffmpeg.org/)
- Bibliotecas de apoio - os, subprocess e Flask

## Estrutura do Projeto
```bash
|--docs/ # Documentação do projeto
|--src/ # Código fonte principal
|--requirement.txt # Dependências do projeto
|--README.md
```

## Funcionalidades
- **Extração de áudio** arquivos de vídeo
- **Remoção de ruídos** utilizando filtros

## Metodologia de Trabalho
O projeto segue o framework **Scrum**, com:
- **Sprints** 
- **Sprint backlog** 
- **Backlog** 
- **Revisão e testes**

## Como rodar o projeto

## Opção 1:
### Acessando a aplicação web diretamente: 
_observação: não roda vídeos com mais de 1 minuto_
Link da aplicação web: https://equipe01-extracaoaudio-globorio.onrender.com


## Opção 2: passo a passo de como clonar o repositório (MAIS INDICADO)
### 1. Clonar o repositório
```bash
git clone https://github.com/Arthurms-dev/Equipe01-ExtracaoAudio-GloboRio
```

### 2. Baixar os arquivos de mídia
Os vídeos e áudios não estão no repositório por serem muito grandes.

Baixe aqui:
https://drive.google.com/drive/folders/1zypQ6i7mgeIylsgEcT8MQN204_u1fjcF?hl=pt-br

### 3. Organizar as pastas
Após baixar, coloque as pastas na raiz do projeto:
```
Equipe01-ExtracaoAudio-GloboRio/
│
├── src/
├── ── templates/ 
├── ── integracaocompleta.py
├── ── render.yaml  
├── LICENSE
├── README.md
└── requirements.txt

 ...
```
### 4. Executar o projeto
Agora é só rodar normalmente que seu vídeo será baixado na sua máquina local.

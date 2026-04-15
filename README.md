# Equipe01-ExtracaoAudio-GloboRio

# Sistema de Extração de Áudio e Vídeo

## Visão Geral
Este projeto tem como objetivo desenvolver uma aplicação em **Python** para **extração e processamento de áudio e vídeo**, utilizando as ferramentas **MoviePy** e **FFmpeg**.  
Principais funcionalidades:
- Segmentação da fala
- Remoção de ruídos
- Separação da trilha de áudio

## Equipe
- **Desenvolvedores (5):** responsáveis pela implementação das funcionalidades
- **Product Owner (PO):** responsável por definir prioridades e backlog
- **Scrum Master:** garante a aplicação das práticas ágeis e remoção de impedimentos

## Tecnologias 
- [Python](https://www.python.org/) 
- [MoviePy](https://zulko.github.io/moviepy/) 
- [FFmpeg](https://ffmpeg.org/)
- Bibliotecas de apoio

## Estrutura do Projeto
```bash
|--docs/ # Documentação do projeto
|--src/ # Código fonte principal
|--tests/ # Testes 
|--requirement.txt # Dependências do projeto
|--README.md
```

## Funcionalidades
- **Extração de áudio** arquivos de vídeo
- **Segmentação da fala** análise detalhada
- **Remoção de ruídos** utilizando filtros
- **Separação de trilhas** (voz, música, etc)

## Metodologia de Trabalho
O projeto segue o framework **Scrum**, com:
- **Sprints** 
- **Sprint backlog** 
- **Backlog** 
- **Revisão e testes**

## Como rodar o projeto
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
├── videos_teste/
├── audios_extraidos/
├── src/
└── ...
```
### 4. Executar o projeto
Agora é só rodar normalmente. A pasta audios_extraidos vai começar vazia e a medida que você for rodando o código, espera-se que ela seja abastecida. 

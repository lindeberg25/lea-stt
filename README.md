# Transcrição e Diarização de Arquivos de Áudio

## Visão Geral
Este projeto fornece um script Python para realizar transcrição e diarização em arquivos de áudio. O script utiliza os modelos whisper ([Robust Speech Recognition via Large-Scale Weak Supervision](https://github.com/openai/whisper)) para transcrever áudios e  pyannote-audio ([neural building blocks for speaker diarization](https://github.com/pyannote/pyannote-audio)) para identificar interlocutores nas gravações de áudio.

## Instalação
Para executar este projeto, crie um ambiente Conda usando o arquivo stt_environment.yaml fornecido. Esse ambiente contém todas as dependências necessárias para o funcionamento correto do script.

### Instalando o Conda

```
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh 
sh miniconda.sh -b -p /opt/conda 
rm miniconda.sh 
```

### Criando ambiente Conda
```
git clone https://gitlab.dpf.gov.br/transcricao-fala-texto/sis_stt.git
cd sis_stt/
conda env create -f stt_environment.yaml
conda activate stt

(stt) pip install pyannote-audio/  (instale este repositório local para executar offline)
```

Para configurar o PATH em um ambiente Linux, adicione a linha abaixo ao arquivo de configuração do shell, geralmente localizado em ~/.bashrc:

```
export PATH="/opt/conda/envs/stt/bin:$PATH"
source ~/.bashrc

```
Esse comando torna todas as dependências deste script de transcrição disponíveis em nível de sistema operacional. 

## Configuração
O script utiliza variáveis de ambiente para configuração. Defina as seguintes variáveis .env:

- `diarization_model`: Caminho para o modelo de diarização.
- `transcription_model`: Caminho para o modelo de transcrição.
- `log_file`: Caminho para o arquivo de log.
- `language` (opcional): Idioma para o modelo de transcrição


## Uso
Transcrever e diarizar um arquivo de áudio:
```
(stt) python sis_stt.py path/to/audio_file.wav
```
Substitua "path/to/audio_file.wav" pelo caminho para o arquivo de áudio que você deseja processar.

#### Exemplo de saída esperada
```
(0.0s - 1.0s)   HNI_1:  Oi, pai.
(1.0s - 7.0s)   HNI_2:  Oi, tô chegando.
(7.0s - 12.0s)  HNI_1:  Já estou aqui esperando.
(12.0s - 15.0s) HNI_2:  Tá bom.
(16.0s - 19.0s) HNI_1:  Quando chegar, avisa.
(29.0s - 30.0s) HNI_2:  Tá bom.
```
HNI = Humano não identificado 

## Referências 

[Robust Speech Recognition via Large-Scale Weak Supervision](https://github.com/openai/whisper)

[pyannote.audio: neural building blocks for speaker diarization](https://github.com/pyannote/pyannote-audio)
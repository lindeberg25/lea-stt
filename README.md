# Transcription and Diarization of Audio Files

## Overview
This project provides a Python script to perform transcription and diarization on audio files. The script uses the whisper model ([Robust Speech Recognition via Large-Scale Weak Supervision](https://github.com/openai/whisper)) for audio transcription and pyannote-audio ([neural building blocks for speaker diarization](https://github.com/pyannote/pyannote-audio)) for speaker diarization in the audio recordings.

To access further details, visit the following link: [ASR for intercepted audio in LEA](https://github.com/lindeberg25/lea-stt/blob/main/asr_lea.pdf)

## Installation
To run this project, create a conda environment using the provided stt_environment.yaml file. This environment contains all the dependencies for the script to work correctly

### Installing Conda

```
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh 
sh miniconda.sh -b -p /opt/conda 
rm miniconda.sh 
```

### Creating Conda Environment
```
git clone https://github.com/lindeberg25/lea-stt.git
cd lea_stt/
conda env create -f stt_environment.yaml
conda activate stt

(stt) pip install pyannote-audio/  (install this local repository to run offline)
```

 To eliminate the requirement of activating a conda environment, add the following line to the shell configuration file, usually located at ~/.bashrc: 

```
export PATH="/opt/conda/envs/stt/bin:$PATH"
source ~/.bashrc
```
This makes all dependencies available at the operating system level.

### To run the Whisper model (medium) locally

From "lea_stt/" directory, execute
```
wget https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt 
```

## Configuration
The script uses environment variables for configuration. Set the following .env variables:

- `diarization_model`: Path to the diarization model.
- `transcription_model`: Path to the transcription model.
- `log_file`: Path to the log file.
- `language` (optional): Language for the transcription model.


## Usage
To transcribe and diarize an audio file:
```
(stt) python sis_stt.py path/to/audio_file.wav
```
Replace "path/to/audio_file.wav" with the path to the audio file you want to process.

#### Example of Expected Output
```
(0.0s - 1.0s)   HNI_1:  Oi, pai.
(1.0s - 7.0s)   HNI_2:  Oi, tô chegando.
(7.0s - 12.0s)  HNI_1:  Já estou aqui esperando.
(12.0s - 15.0s) HNI_2:  Tá bom.
(16.0s - 19.0s) HNI_1:  Quando chegar, avisa.
(29.0s - 30.0s) HNI_2:  Tá bom.
```
HNI = Human not identified

## References 

[Robust Speech Recognition via Large-Scale Weak Supervision](https://github.com/openai/whisper)

[pyannote.audio: neural building blocks for speaker diarization](https://github.com/pyannote/pyannote-audio)
import os
import whisper
from pyannote.audio import Pipeline
from pyannote_whisper.utils import diarize_text
import logging
import time
import librosa
import numba
from dotenv import load_dotenv
import argparse

# Desabilitar a compilação JIT do Numba
numba.config.DISABLE_JIT = True
# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()
# Obter o valor da variável de ambiente 'diarization_model' e atribuí-lo a 'diarization_model'
diarization_model = os.environ.get('diarization_model')
# Obter o valor da variável de ambiente 'transcription_model' e atribuí-lo a 'transcription_model'
transcription_model = os.environ.get('transcription_model')
# Obter o valor da variável de ambiente 'log_file' e atribuí-lo a 'log_file'
log_file = os.environ.get('log_file')
# Obter o valor da variável de ambiente 'language' e atribuí-lo a 'language'
language = os.environ.get('language')
# Configurar o registro de logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')
# Carregar o modelo de diarização
pipeline = Pipeline.from_pretrained(diarization_model)
# Carregar o modelo de transcrição
model = whisper.load_model(transcription_model)

# Função que transcreve e diariza audios
def transcribe_diarization(audio_file):
    transcricao = ""
    if os.path.exists(audio_file):
        start = time.time()
        logging.info("Inicio da transcricao: {}".format(audio_file))
        
        array, sample = librosa.load(audio_file)
        duration = librosa.get_duration(y=array, sr=sample)
        
        asr_result = model.transcribe(audio_file, language=language)
        
        logging.info("Resultado da transcricao: {}".format(asr_result['text']))
        logging.info("Fim da transcricao: {}".format(audio_file))
        logging.info("Duração do audio: {:.1f} seconds".format(duration))
        logging.info("Duracao da transcricao: {:.1f} seconds".format((time.time() - start)))
        
        start = time.time()
        logging.info("Inicio da Diarizacao: {}".format(audio_file))
        
        diarization_result = pipeline(audio_file, num_speakers=2)
        
        logging.info("Fim da diarizacao: {}".format(audio_file))
        logging.info("Duracao da diarizacao: {:.1f} seconds".format((time.time() - start)))
        
        label_map = {'SPEAKER_00': 'HNI_1', 'SPEAKER_01': 'HNI_2'}
        diarization_result = diarization_result.rename_labels(label_map)
        
        final_result = diarize_text(asr_result, diarization_result)
        
        for seg, spk, sent in final_result:
            line = f'({seg.start:.1f}s - {seg.end:.1f}s) {spk}: {sent}'
            transcricao += line + os.linesep
        
    else:
        logging.info("O arquivo {} não existe".format(audio_file))


    return transcricao


def main():
    parser = argparse.ArgumentParser(description='Transcrever e diarizar arquivos de áudio.')
    parser.add_argument('audio_file', type=str, help='Caminho para o arquivo de áudio para processamento.')
    args = parser.parse_args()
    
    trancricao = transcribe_diarization(args.audio_file)

    print(trancricao)

if __name__ == "__main__":
    main()

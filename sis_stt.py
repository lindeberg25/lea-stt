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

# Disable Numba's JIT Compilation
numba.config.DISABLE_JIT = True
# Load environment variables from the .env file
load_dotenv()
# Get the value of the 'diarization_model' environment variable and assign it to 'diarization_model'
diarization_model = os.environ.get('diarization_model')
# Get the value of the 'transcription_model' environment variable and assign it to 'transcription_model'
transcription_model = os.environ.get('transcription_model')
# Get the value of the 'log_file' environment variable and assign it to 'log_file'
log_file = os.environ.get('log_file')
# Get the value of the 'language' environment variable and assign it to 'language'
language = os.environ.get('language')
# Configure the logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')
# Load the diarization model
pipeline = Pipeline.from_pretrained(diarization_model)
# Load the transcription model
model = whisper.load_model(transcription_model)

# Function that transcribes and diarizes audios
def transcribe_diarization(audio_file):
    transcricao = ""
    if os.path.exists(audio_file):
        start = time.time()
        logging.info("Transcription start: {}".format(audio_file))
        
        array, sample = librosa.load(audio_file)
        duration = librosa.get_duration(y=array, sr=sample)
        
        asr_result = model.transcribe(audio_file, language=language)
        
        logging.info("Transcription result: {}".format(asr_result['text']))
        logging.info("Transcript end: {}".format(audio_file))
        logging.info("Audio duration: {:.1f} seconds".format(duration))
        logging.info("Transcription duration: {:.1f} seconds".format((time.time() - start)))
        
        start = time.time()
        logging.info("Diarization start: {}".format(audio_file))
        
        diarization_result = pipeline(audio_file, num_speakers=2)
        
        logging.info("Diarization end: {}".format(audio_file))
        logging.info("Diarization duration: {:.1f} seconds".format((time.time() - start)))
        
        label_map = {'SPEAKER_00': 'HNI_1', 'SPEAKER_01': 'HNI_2'}
        diarization_result = diarization_result.rename_labels(label_map)
        
        # diarize_text function can be found here: https://github.com/yinruiqing/pyannote-whisper
        final_result = diarize_text(asr_result, diarization_result)
        
        for seg, spk, sent in final_result:
            line = f'({seg.start:.1f}s - {seg.end:.1f}s) {spk}: {sent}'
            transcricao += line + os.linesep
        
    else:
        logging.info("File {} not exist".format(audio_file))


    return transcricao


def main():
    parser = argparse.ArgumentParser(description='Transcribe and diarize audio files.')
    parser.add_argument('audio_file', type=str, help='Path to the audio file for processing.')
    args = parser.parse_args()
    
    trancricao = transcribe_diarization(args.audio_file)

    print(trancricao)

if __name__ == "__main__":
    main()

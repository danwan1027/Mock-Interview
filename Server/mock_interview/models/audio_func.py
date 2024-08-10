import pyaudio
import wave
import os
import time
import io
from google.oauth2 import service_account
from google.cloud import speech
import threading
import queue


# Set parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2

RECORDING_TIMES = 0
WORD_COUNT = []

stop_event = threading.Event()

# Set the path for the client file
client_file = 'instance/mock-interview.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials = credentials)

def record_chunk(p, stream, audio_queue, chunk_length=RECORD_SECONDS):
    global RECORDING_TIMES
    frames = []
    for _ in range(0, int(RATE / CHUNK * chunk_length)):
        if stream.is_active():
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        else:
            print("Stream is not open.")
            break
    audio_queue.put(b''.join(frames))
    RECORDING_TIMES += 1

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK)
    
    accumulated_transcript = []
    audio_queue = queue.Queue()

    def record(p, stream, audio_queue): 
        while not stop_event.is_set():
            record_chunk(p, stream, audio_queue)

    def transcribe_chunk(audio_queue, accumulated_transcript):
        while not stop_event.is_set():
            # Wait for audio data to be available
            while audio_queue.empty():
                time.sleep(1)
            audio_data = audio_queue.get()

            if audio_data is None:
                break
            audio = speech.RecognitionAudio(content=audio_data)

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code='cmn-Hant-TW',
                enable_automatic_punctuation=True
            )

            response = client.recognize(config=config, audio=audio)
            if response.results:
                recorded = response.results[0].alternatives[0].transcript
                print("Recorded Text: " + recorded)
                accumulated_transcript.append(recorded)
                WORD_COUNT.append(len(recorded))


    try:
        print("Start Recording...")
        record_thread = threading.Thread(target=record, args=(p, stream, audio_queue))
        transcribe_thread = threading.Thread(target=transcribe_chunk, args=(audio_queue, accumulated_transcript))

        record_thread.start()
        transcribe_thread.start()

        record_thread.join()
        transcribe_thread.join()

    except KeyboardInterrupt:
        print("Stoping...")
    finally:
        print("LOG:" + ''.join(accumulated_transcript))
        print("Word Count: " + str(WORD_COUNT))
        print("Total Words: " + str(sum(WORD_COUNT)))
        print("Total Recording Times: " + str(RECORDING_TIMES)) 
        print("End of Recording...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return {
            "accumulated_transcript": ''.join(accumulated_transcript),
            "word_count": WORD_COUNT,
            "total_words": sum(WORD_COUNT),
            "recording_times": RECORDING_TIMES
        }
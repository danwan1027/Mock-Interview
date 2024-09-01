import pyaudio
import wave
import os
import time
import io
from google.oauth2 import service_account
from google.cloud import speech
import threading
import queue
import asyncio


# Set parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

RECORDING_TIMES = 0
WORD_COUNT = []

stop_event = threading.Event()

# Set the path for the client file
client_file = 'instance/mock-interview.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials = credentials)

class AudioRecorder:
    def __init__(self):
        self.p = None
        self.stream = None
        self.frames = []
        self.recording_task = None
        self.stop_event = asyncio.Event()
        self.client = client # Initialize Google Speech API client

    async def record_async(self):
        while not self.stop_event.is_set():
            if self.stream.is_active():
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.frames.append(data)
            else:
                print("Stream is not open.")
                break
            await asyncio.sleep(0)  # Yield control to the event loop

        return self.frames

    async def start_audio_recording(self):
        self.p = pyaudio.PyAudio()
        self.frames = []

        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        self.recording_task = asyncio.create_task(self.record_async())

    async def stop_audio_recording(self):
        self.stop_event.set()  # Stop the recording loop

        if self.recording_task:
            await self.recording_task  # Wait for the recording to finish

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.p:
            self.p.terminate()

        # Process the audio using Google Speech-to-Text API
        audio_content = b''.join(self.frames)
        audio = speech.RecognitionAudio(content=audio_content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code='cmn-Hant-TW',
            enable_automatic_punctuation=True
        )

        response = self.client.recognize(config=config, audio=audio)
        if response.results:
            recorded = response.results[0].alternatives[0].transcript
            print("Recorded Text: " + recorded)
            return recorded
        
        return None
    

# def main():
#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, 
#                     channels=CHANNELS, 
#                     rate=RATE, 
#                     input=True, 
#                     frames_per_buffer=CHUNK)
    
#     accumulated_transcript = []
#     audio_queue = queue.Queue()

#     def record(p, stream, audio_queue): 
#         while not stop_event.is_set():
#             record_chunk(p, stream, audio_queue)

#     def transcribe_chunk(audio_queue, accumulated_transcript):
#         while not stop_event.is_set():
#             # Wait for audio data to be available
#             while audio_queue.empty():
#                 time.sleep(1)
#             audio_data = audio_queue.get()

#             if audio_data is None:
#                 break
#             audio = speech.RecognitionAudio(content=audio_data)

#             config = speech.RecognitionConfig(
#                 encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#                 sample_rate_hertz=RATE,
#                 language_code='cmn-Hant-TW',
#                 enable_automatic_punctuation=True
#             )

#             response = client.recognize(config=config, audio=audio)
#             if response.results:
#                 recorded = response.results[0].alternatives[0].transcript
#                 print("Recorded Text: " + recorded)
#                 accumulated_transcript.append(recorded)
#                 WORD_COUNT.append(len(recorded))


#     try:
#         print("Start Recording...")
#         record_thread = threading.Thread(target=record, args=(p, stream, audio_queue))
#         transcribe_thread = threading.Thread(target=transcribe_chunk, args=(audio_queue, accumulated_transcript))

#         record_thread.start()
#         transcribe_thread.start()

#         record_thread.join()
#         transcribe_thread.join()

#     except KeyboardInterrupt:
#         print("Stoping...")
#     finally:
#         print("LOG:" + ''.join(accumulated_transcript))
#         print("Word Count: " + str(WORD_COUNT))
#         print("Total Words: " + str(sum(WORD_COUNT)))
#         print("Total Recording Times: " + str(RECORDING_TIMES)) 
#         print("End of Recording...")
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#         return {
#             "accumulated_transcript": ''.join(accumulated_transcript),
#             "word_count": WORD_COUNT,
#             "total_words": sum(WORD_COUNT),
#             "recording_times": RECORDING_TIMES
#         }
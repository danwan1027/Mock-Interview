from flask import jsonify, redirect, render_template
import models.crud_example as crud

def init_routes(app):
    @app.route('/')
    def index():
        # return jsonify({'Employee Data': crud.read_employee_data()})
        return render_template('index.html')

    @app.route('/create', methods=['GET'])
    def create():
        employee_name = 'Jimmy'
        title = 'Jimmy'
        crud.create_employee(employee_name, title)
        return redirect('/')

    @app.route('/update', methods=['GET'])
    def update():
        employee_name = 'Jimmy'
        new_title = 'Jimmy update'
        crud.update_employee(employee_name, new_title)
        return redirect('/')
    
    # @app.route('/record', methods=['GET'])
    # def record():
    #     import cv2
    #     import time
    #     import pyaudio
    #     import wave

    #     # Function to record audio
    #     def record_audio(filename, duration):
    #         CHUNK = 1024
    #         FORMAT = pyaudio.paInt16
    #         CHANNELS = 1
    #         RATE = 44100

    #         audio = pyaudio.PyAudio()

    #         stream = audio.open(format=FORMAT, channels=CHANNELS,
    #                             rate=RATE, input=True,
    #                             frames_per_buffer=CHUNK)

    #         frames = []

    #         print("Recording audio...")
    #         for _ in range(0, int(RATE / CHUNK * duration)):
    #             data = stream.read(CHUNK)
    #             frames.append(data)

    #         print("Finished recording audio.")

    #         stream.stop_stream()
    #         stream.close()
    #         audio.terminate()

    #         waveFile = wave.open(filename, 'wb')
    #         waveFile.setnchannels(CHANNELS)
    #         waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    #         waveFile.setframerate(RATE)
    #         waveFile.writeframes(b''.join(frames))
    #         waveFile.close()

    #     # Video capture initialization
    #     cap = cv2.VideoCapture(0)
    #     fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (w,h))

    #     # Audio recording initialization
    #     audio_filename = 'output_audio.wav'
    #     audio_duration = 5  # Set the duration of audio recording in seconds

    #     # Start recording audio
    #     record_audio(audio_filename, audio_duration)

    #     start_time = time.time() # Record the start time
    #     while True:
    #         ret, frame = cap.read()
    #         if ret:
    #             out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
    #             # Check if 5 seconds have passed
    #             if time.time() - start_time > audio_duration:
    #                 break
    #         else:
    #             break

    #     # Release video capture and writer
    #     cap.release()
    #     out.release()
    #     cv2.destroyAllWindows()

    #     from moviepy.editor import VideoFileClip, AudioFileClip

    #     # Specify the paths to your video and audio files
    #     video_path = 'output.mp4'
    #     audio_path = 'output_audio.wav'

    #     # Load the video and audio files
    #     video_clip = VideoFileClip(video_path)
    #     audio_clip = AudioFileClip(audio_path)

    #     # Combine the video and audio
    #     final_clip = video_clip.set_audio(audio_clip)

    #     # Explicitly set the fps attribute of the final_clip
    #     final_clip.fps = 30 # Set the desired frame rate

    #     # Specify the output file path and save the combined video
    #     output_path = 'final_video.mp4'
    #     final_clip.write_videofile(output_path, fps=final_clip.fps)


    #     return redirect('/')

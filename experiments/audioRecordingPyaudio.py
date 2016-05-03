
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
#WAVE_OUTPUT_FILENAME = "output.wav"

class AudioRecording(object):
    
    filename = None
    recording = False
    stream = None
    frames = None
    
    def __init__(self):
        
        self.audio = pyaudio.PyAudio()
        
        self.stream = self.audio.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
    def setFilename(self, filename):
        self.filename = filename
        
    def startRecording(self):
        self.recording = True
        
        self.frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #while self.recording == True:
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        
    def stopRecording(self):
        self.recording = False
        
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

if __name__ == "__main__":
    c = AudioRecording()

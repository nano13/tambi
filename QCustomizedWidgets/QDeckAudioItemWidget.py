
from PyQt5.QtMultimedia import QAudioInput, QAudioFormat, QAudioDeviceInfo
from PyQt5.QtCore import QTimer, QFile, QIODevice

class QDeckAudioItemWidget(QAudioInput):
    
    audio_input = None
    outputFile = None
    
    def __init__(self):
        super().__init__()
        
    def initAudioInput(self, filepath):
        
        self.outputFile = QFile()
        self.outputFile.setFileName(filepath)
        self.outputFile.open(QIODevice.WriteOnly | QIODevice.Truncate)
        
        format = QAudioFormat();
        format.setSampleType(QAudioFormat.Float);
        format.setSampleRate(44100);
        format.setChannelCount(1);
        format.setSampleSize(32);
        format.setCodec("audio/pcm");
        format.setByteOrder(QAudioFormat.LittleEndian);
        
        print(format.codec())
        
        #self.audio_input = QAudioInput(QAudioDeviceInfo.defaultInputDevice(), format);
        
        self.audio_input = QAudioInput(format);
        
        print(self.audio_input.error())
        print(self.audio_input.state())
        
        #QTimer.singleShot(3000, self, 
        
    def start(self):
        self.audio_input.start(self.outputFile)
        
    def stop(self):
        self.audio_input.stop()
        self.outputFile.close()
        
    def suspend(self):
        self.audio_input.suspend()
        
    def resume(self):
        self.audio_input.resume()
        
if __name__ == "__main__":
    c = QDeckAudioItemWidget()
    c.initAudioInput()

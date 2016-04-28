
from PyQt5.QtMultimedia import QAudioInput, QAudioFormat, QAudioDeviceInfo

class QDeckAudioItemWidget(QAudioInput):
    
    audio_input = None
    
    def __init__(self):
        super().__init__()
        
    def initAudioInput(self):
        
        format = QAudioFormat();
        format.setSampleType(QAudioFormat.Float);
        format.setSampleRate(44100);
        format.setChannelCount(1);
        format.setSampleSize(32);
        format.setCodec("audio/pcm");
        format.setByteOrder(QAudioFormat.LittleEndian);
        
        info = QAudioDeviceInfo.defaultInputDevice();
        if not info.isFormatSupported(format):
            qWarning()<<"default format not supported try to use nearest";
            format = info.nearestFormat(format);
        
        print(format.codec())
        print(info.nearestFormat(format).codec())
        
        #self.audio_input = QAudioInput(QAudioDeviceInfo.defaultInputDevice(), format);
        
        self.audio_input = QAudioInput(format, self);
        
        print(self.audio_input.error())
        print(self.audio_input.state())
        
    def start():
        self.audio_input.start()
        
    def stop():
        self.audio_input.stop()
        
    def suspend():
        self.audio_input.suspend()
        
    def resume():
        self.audio_input.resume()
        
if __name__ == "__main__":
    c = QDeckAudioItemWidget()
    c.initAudioInput()

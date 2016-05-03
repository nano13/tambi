
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings

class QVoiceRecorder(object):
    def __init__(self):
        pass
    
    def initAudioInput(self, filepath):
        
        self.recorder = QAudioRecorder()
        
        self.settings = QAudioEncoderSettings()
        self.settings.setCodec("audio/vorbis")
        self.recorder.setContainerFormat("ogg")
        #self.settings.setQuality(QtMultimedia.HighQuality)
        
        self.recorder.setEncodingSettings(self.settings)
        
        url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filepath).absoluteFilePath())
        self.recorder.setOutputLocation(url)
        
    def start(self):
        self.recorder.record()
        
    def stop(self):
        self.recorder.pause()
        self.recorder.stop()
        self.recorder.stop()

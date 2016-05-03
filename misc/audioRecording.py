
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtMultimedia import QAudioEncoderSettings, QMediaRecorder, QMediaObject, QMediaContent, QAudioRecorder, QAudioInput

class RecordAudio(object):
    
    recorder = None
    
    def __init__(self):
        pass
    
    def record(self, filename):
        url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filename).absoluteFilePath())
        #content = QMediaObject(url)
        
        #self.recorder = QAudioRecorder()
        #source = QAudioInput()
        #source = QMediaObject()
        self.recorder = QAudioRecorder()
        
        settings = QAudioEncoderSettings()
        settings.setChannelCount(1)
        settings.setSampleRate(44100)
        settings.setBitRate(32)
        settings.setCodec("audio/vorbis")
        #settings.setEncodingMode(QtMultimedia.ConstantQualityEnconding)
        
        self.recorder.setContainerFormat("ogg")
        self.recorder.setEncodingSettings(settings)
        self.recorder.setOutputLocation(url)
        
        #container = None
        #self.recorder.setEncodingSettings(settings, container)
        
    def record(self):
        self.recorder.record()
        
    def stop(self):
        self.recorder.stop()

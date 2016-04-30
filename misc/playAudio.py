
from PyQt5 import QtCore, QtMultimedia

class PlayAudio(object):
    
    player = None
    
    def __init__(self):
        pass
    
    def play(self, filename):
        #url = QtCore.QUrl.fromLocalFile(filename)
        url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filename).absoluteFilePath())
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        
        self.player.play()
        
    def stop(self):
        self.player.stop()
        
if __name__ == "__main__":
    c = PlayAudio()
    c.play("./soldiers_joy.ogg")

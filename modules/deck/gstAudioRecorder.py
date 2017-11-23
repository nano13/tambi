
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, Gtk

class GstAudioRecorder(object):
    
    url = None
    codec = None
    
    def __init__(self):
        pass
    
    def setOutputLocation(self, url):
        self.url = url.path()
        
    
    def setEncodingSettings(self, settings):
        self.codec = settings.codec()
    
    def setContainerFormat(self, container):
        pass
    
    def record(self):
        self.recorder = RecorderThread(self.url, self.codec)
        self.recorder.start()
    
    def stop(self):
        
        try:
            self.recorder.quit()
            self.recorder.join()
        except AttributeError:
            """ nothing to do, we are just not recording yet """
            pass
        else:
            self.recorder.join()
        
        self.recorder = None

from threading import Thread
""" we are needing this thread, because otherwise the gstreamer-thread would freeze the whole thing """
class RecorderThread(Thread):
    
    def __init__(self, url, codec):
        super().__init__()
        
        self.url = url
        self.codec = codec
    
    def run(self):
        Gst.init(None)
        
        self.pipeline = Gst.Pipeline()
        
        autoaudiosrc = Gst.ElementFactory.make("autoaudiosrc", "autoaudiosrc")
        audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        
        if self.codec == 'audio/vorbis':
            enc = Gst.ElementFactory.make("vorbisenc", "vorbisenc")
            mux = Gst.ElementFactory.make("oggmux", "oggmux")
            print("..................", mux)
        elif self.codec == 'audio/mpeg':
            print("RECORDING MP3")
            enc = Gst.ElementFactory.make("lamemp3enc", "lamemp3enc")
            mux = Gst.ElementFactory.make("mp4mux", "mp4mux")
            print(mux)
        elif self.codec == 'audio/amr':
            enc = Gst.ElementFactory.make("voamrwbenc", "voamrwbenc")
            mux = Gst.ElementFactory.make("", "")
        else:
            """ audio/PCM / wav """
            enc = Gst.ElementFactory.make("wavpackenc", "wavpackenc")
            mux = Gst.ElementFactory.make("wavenc", "wavenc")
            print("WAV:", "\n", enc, "\n", mux)
        
        filesink = Gst.ElementFactory.make("filesink", "filesink")
        filesink.set_property("location", self.url)
        self.pipeline.add(autoaudiosrc)
        
        self.pipeline.add(audioconvert)
        self.pipeline.add(enc)
        self.pipeline.add(mux)
        self.pipeline.add(filesink)
        
        autoaudiosrc.link(audioconvert)
        audioconvert.link(enc)
        enc.link(mux)
        mux.link(filesink)
        
        self.pipeline.set_state(Gst.State.PLAYING)
    
    def quit(self):
        self.pipeline.set_state(Gst.State.NULL)
        
        while Gtk.main_level() > 0:
            Gtk.main_quit()
        
        self.join()


import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, Gtk

#TODO: implement this bullshit with pyaudio

class AudioRecorder(object):
    
    url = None
    
    def __init__(self):
        pass
    
    def setOutputLocation(self, url):
        self.url = url.path()
        
    
    def setEncodingSettings(self, settings):
        pass
    
    def setContainerFormat(self, format):
        pass
    
    def record(self):
        self.recorder = RecorderThread(self.url)
        self.recorder.start()
    
    def stop(self):
        print("try to stop")
        #Gtk.main_quit()
        
        try:
            print("calling shutdown")
            self.recorder.shutdown = True
            print("calling quit")
            self.recorder.quit()
            self.recorder.join()
        except AttributeError:
            """ nothing to do, we are just not recording yet """
            print(".....................")
            pass
        else:
            self.recorder.join()
        
        self.recorder = None

from threading import Thread
class RecorderThread(Thread):
    
    shutdown = False
    
    def __init__(self, url):
        super().__init__()
        
        self.url = url
    
    def run(self):
        #GObject.threads_init()
        Gst.init(None)
        
        self.pipeline = Gst.Pipeline()
        
        autoaudiosrc = Gst.ElementFactory.make("autoaudiosrc", "autoaudiosrc")
        audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        vorbisenc = Gst.ElementFactory.make("vorbisenc", "vorbisenc")
        oggmux = Gst.ElementFactory.make("oggmux", "oggmux")
        filesink = Gst.ElementFactory.make("filesink", "filesink")
        filesink.set_property("location", self.url)
        self.pipeline.add( autoaudiosrc)
        self.pipeline.add( audioconvert)
        self.pipeline.add( vorbisenc)
        self.pipeline.add( oggmux)
        self.pipeline.add( filesink)
        
        autoaudiosrc.link( audioconvert)
        audioconvert.link( vorbisenc)
        vorbisenc.link( oggmux)
        oggmux.link( filesink)
        
        self.pipeline.set_state(Gst.State.PLAYING)
        
    
    def __run(self):
        print("am arsch")
        #Gtk.main()
        #self.loop = GObject.MainLoop()
        #self.loop.run()
        pass
    
    def quit(self):
        print("trying even harder .... ")
        self.pipeline.set_state(Gst.State.NULL)
        #print(Gtk.main_level())
        #Gtk.main_quit()
        
        while Gtk.main_level() > 0:
            Gtk.main_quit()
            print(Gtk.main_level())

if __name__ == '__main__':
    c = AudioRecorder()
    c.setOutputLocation('1.ogg')
    
    c.record()
    
    import time
    time.sleep(2)
    c.stop()

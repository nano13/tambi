
from modules.gps.dbAdapter import DbAdapter

from xml.sax import make_parser, handler

class GpxParser(object):
    
    def __init__(self, dbpath):
        self.parser = make_parser()
        self.handler = GpxParserHandler(dbpath)
        self.parser.setContentHandler(self.handler)
    
    def parse(self, filepath):
        self.parser.parse(filepath)
    
    def getParsedData(self):
        return self.handler.getParsedData()

class GpxParserHandler(handler.ContentHandler):
    
    in_trkpt = False
    in_ele = False
    in_speed = False
    in_time = False
    
    lat = None
    lon = None
    alt = None
    speed = None
    time = None
    
    parsed = []
    
    def __init__(self, dbpath):
        self.dbAdapter = DbAdapter(dbpath)
    
    def startElement(self, name, attrs):
        if name == 'trkpt':
            self.in_trkpt = True
            self.lat = attrs['lat']
            self.lon = attrs['lon']
        elif name == 'ele':
            self.in_ele = True
        elif name == 'speed':
            self.in_speed = True
        elif name == 'time':
            self.in_time = True
    
    def characters(self, content):
        if self.in_ele:
            self.alt = content
        elif self.in_speed:
            self.speed = content
        elif self.in_time:
            self.time = content
    
    def endElement(self, name):
        if name == 'trkpt':
            self.in_trkpt = False
            self.parsed.append({'lat': self.lat, 'lon': self.lon, 'alt': self.alt, 'speed': self.speed, 'time': self.time})
            
            self.lat = None
            self.lon = None
            self.alt = None
            self.speed = None
            self.time = None
            
        elif name == 'ele':
            self.in_ele = False
        elif name == 'speed':
            self.in_speed = False
        elif name == 'time':
            self.in_time = False
    
    def getParsedData(self):
        return self.parsed

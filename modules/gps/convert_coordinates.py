
import math

class ConvertCoordinates(object):
    
    zoom = 10
    
    corners = {
        'nw' : None,
        'sw' : None,
        'ne' : None,
        'se' : None,
        }
    corners_mercator = {
        'nw' : None,
        'sw' : None,
        'ne' : None,
        'se' : None,
        }
    
    def __init__(self):
        pass
    
    def calculateCorners(self, zoom, x_min, x_max, y_min, y_max):
        self.corners['nw'] = self.tileNumberToDeg(zoom, x_min, y_min)
        self.corners['ne'] = self.tileNumberToDeg(zoom, x_min, y_max+1)
        self.corners['sw'] = self.tileNumberToDeg(zoom, x_max+1, y_min)
        self.corners['se'] = self.tileNumberToDeg(zoom, x_max+1, y_max+1)
        
        self.corners_mercator['nw'] = self.convertDegToWebMercator_(self.corners['nw'])
        self.corners_mercator['ne'] = self.convertDegToWebMercator_(self.corners['ne'])
        self.corners_mercator['sw'] = self.convertDegToWebMercator_(self.corners['sw'])
        self.corners_mercator['se'] = self.convertDegToWebMercator_(self.corners['se'])
        
        return self.corners_mercator
    
    def degToTileNumber(self, zoom, lat_deg, lon_deg):
        """ source: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y """
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)
    
    def tileNumberToDeg(self, zoom, xtile, ytile):
        """ source: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y """
        """ this will return the nw-corner of the tile """
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)
    
    def convertDegToWebMercator_(self, coords):
        return self.convertDegToWebMercator(coords[0], coords[1])
    
    def convertDegToWebMercator(self, lat, lon):
        """
        derived from the Java version explained here: http://wiki.openstreetmap.org/wiki/Mercator
        """
        RADIUS = 6378137.0 # in meters on the equator
        
        lat = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * RADIUS
        
        lon = math.radians(lon) * RADIUS
        
        return lon, lat
    
    """
    def convertDegToWebMercatorWithPyproj(self, pos):
        from pyproj import Proj, transform
        
        inProj = Proj(init='epsg:4326') # WGS-84, usually used by GPS
        outProj = Proj(init='epsg:3857') # web-mercator, used by virtually all major online map providers, including Google Maps, Bing Maps, OpenStreetMap, Mapquest, Esri, Mapbox, and many others
        longitude, latitude = transform(inProj, outProj, pos['longitude'], pos['latitude'])
        
        return longitude, latitude
    """
    
    def convertGeoToCanvas(self, scene_rect, lat, lon):
        from decimal import Decimal
        
        mapLatBottom = self.corners['se'][0]
        
        mapLonLeft = self.corners['nw'][1]
        mapLonRight = self.corners['se'][1]
        mapLonDelta = mapLonRight - mapLonLeft
        mapLatBottomRad = mapLatBottom * math.pi / 180
        lat_rad = lat * math.pi / 180;
        print("\n")
        print("SCENE", scene_rect)
        print(lat, lon)
        print(self.corners)
        print("D", mapLonLeft, mapLonRight)
        
        x = (lon - mapLonLeft) * (scene_rect.width() / mapLonDelta);

        worldMapWidth = ((scene_rect.width() / mapLonDelta) * 360) / (2 * math.pi);
        mapOffsetY = (worldMapWidth / 2 * math.log((1 + math.sin(mapLatBottomRad)) / (1 - math.sin(mapLatBottomRad))));
        print(mapOffsetY)
        y = scene_rect.height() - ((worldMapWidth / 2 * math.log((1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)))) - mapOffsetY);
        
        print("CANVAS", x, y)
        #x = x + 256
        #y = y + 256
        print("-----")
        print("GEO1", lat, lon)
        print("GEO2", self.convertCanvasToGeo(scene_rect, x, y))
        return x, y
    
    def convertCanvasToGeo(self, scene_rect, tx, ty):
        mapLonLeft = self.corners['nw'][1]
        mapLonRight = self.corners['sw'][1]
        mapLonDelta = mapLonRight - mapLonLeft
        mapLatBottom = self.corners['se'][0]
        mapLatBottomRad = mapLatBottom * math.pi / 180
        """ the radius since it's the map width or circumference divided by 2*PI  """
        worldMapRadius = scene_rect.width() / mapLonDelta * 360/(2 * math.pi);
        mapOffsetY = ( worldMapRadius / 2 * math.log( (1 + math.sin(mapLatBottomRad) ) / (1 - math.sin(mapLatBottomRad)) ));
        equatorY = scene_rect.height() + mapOffsetY;
        a = (equatorY-ty) / worldMapRadius;

        lat = 180/math.pi * (2 * math.atan(math.exp(a)) - math.pi/2);
        lon = mapLonLeft + tx / scene_rect.width() * mapLonDelta;
        return lat, lon

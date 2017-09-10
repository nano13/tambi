
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
    
    def convertToCanvas_(self, scene_rect, lat, lon):
        merc_lat, merc_lon = self.convertDegToWebMercator(lat, lon)
        
        max_lat = self.corners_mercator['sw'][0]
        max_lon = self.corners_mercator['nw'][1]
        min_lat = self.corners_mercator['nw'][0]
        min_lon = self.corners_mercator['ne'][1]
        
        lat_rad = lat * math.pi / 180
        lon_rad = lon * math.pi / 180
        
        
        
        return x, y
    
    def convertToCanvas(self, scene_rect, x, y):
        x, y = self.convertDegToWebMercator(y, x)
        
        max_lat = self.corners_mercator['sw'][0]
        max_lon = self.corners_mercator['nw'][1]
        min_lat = self.corners_mercator['nw'][0]
        min_lon = self.corners_mercator['ne'][1]
        
        """
        self.corners_mercator['nw'] => 0 | 0
        self.corners_mercator['ne'] => 256 | 0
        self.corners_mercator['sw'] => 0 | 256
        self.corners_mercator['se'] => 256 | 256
        
        x => 0 ... 256
        y => 0 ... 256
        
        nw.x / ne.x = x * 256
        nw.y / sw.y = y * 256
        
        
        (ne.x - nw.x) * a = 256
        x = x - nw.x * - 256 / (nw.x - ne.x)
        
        
        x = x * (ne.x / nw.x = x / 256)
        
        
        nw.x / ne.x = 0 / 256
        
        
        
        offset = ne.x - nw.x
        1 / 256 = 1 / (ne.x - offset)
        
        """
        #scene_rect = scene.itemsBoundingRect()
        
        print("\n")
        print("SCENE", scene_rect)
        print(x, y)
        x = x - min_lat
        y = y - min_lon
        print(x, y)
        print(self.corners_mercator)
        
        step_x = scene_rect.width() / (max_lat - min_lat)
        step_y = scene_rect.height() / (max_lon - min_lon)
        
        
        
        print("STEP", step_x, step_y)
        x = x * step_x
        y = y * step_y
        print(x, y)
        
        return x, y
    
    def convertCanvasToGeo(self, scene_rect, tx, ty):
        max_lat = self.corners['sw'][0]
        max_lon = self.corners['nw'][1]
        min_lat = self.corners['nw'][0]
        min_lon = self.corners['ne'][1]
        mapLonLeft = max_lon
        mapLonRight = min_lon
        mapLonDelta = mapLonRight - mapLonLeft
        if mapLonDelta == 0.0:
            mapLonDelta = 0.0000000000001
        mapLatBottomRadian = max_lat * math.pi / 180
        """ the radius since it's the map width or circumference divided by 2*PI  """
        worldMapRadius = scene_rect.width() / mapLonDelta * 360/(2 * math.pi);
        mapOffsetY = ( worldMapRadius / 2 * math.log( (1 + math.sin(mapLatBottomRadian) ) / (1 - math.sin(mapLatBottomRadian))  ));
        equatorY = scene_rect.height() + mapOffsetY;
        a = (equatorY-ty)/worldMapRadius;

        lat = 180/math.pi * (2 * math.atan(math.exp(a)) - math.pi/2);
        lon = mapLonLeft + tx / scene_rect.width() * mapLonDelta;
        return lat, lon

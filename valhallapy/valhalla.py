import requests
import json
from shapely.geometry import asLineString

class ValhallaRoute:
    def __init__(self,route_object):
        self.ro = route_object

    def instructions(self):
        return "\n".join( leg['instruction'] for leg in  self.ro['trip']['legs'][0]['maneuvers'])

    def distance(self):
        return self.ro['trip']['summary']['length']

    def time(self):
        return self.ro['trip']['summary']['time']

    def shape(self):
        return self.decode(self.ro['trip']['legs'][0]['shape'])

    def wkb(self):
        return asLineString(self.shape()).wkb

    def wkt(self):
        return asLineString(self.shape()).wkt
        
    def asGeoJSON(self, properties={}):
        return {'type': 'Feature','properties': properties, 'geometry': { 'type': 'LineString', 'coordinates': self.shape()}}

    def geoJSON(self, properties={}):
        return json.dumps(self.asGeoJSON(properties))

    def decode(self,point_str):
        '''Decodes a polyline that has been encoded using Google's algorithm
        http://code.google.com/apis/maps/documentation/polylinealgorithm.html

        This is a generic method that returns a list of (latitude, longitude)
        tuples.

        :param point_str: Encoded polyline string.
        :type point_str: string
        :returns: List of 2-tuples where each tuple is (latitude, longitude)
        :rtype: list

        '''

        # sone coordinate offset is represented by 4 to 5 binary chunks
        coord_chunks = [[]]
        for char in point_str:

            # convert each character to decimal from ascii
            value = ord(char) - 63

            # values that have a chunk following have an extra 1 on the left
            split_after = not (value & 0x20)
            value &= 0x1F

            coord_chunks[-1].append(value)

            if split_after:
                    coord_chunks.append([])

        del coord_chunks[-1]

        coords = []

        for coord_chunk in coord_chunks:
            coord = 0

            for i, chunk in enumerate(coord_chunk):
                coord |= chunk << (i * 5)

            #there is a 1 on the right if the coord is negative
            if coord & 0x1:
                coord = ~coord #invert
            coord >>= 1
            coord /= 1000000.0

            coords.append(coord)

        # convert the 1 dimensional list to a 2 dimensional list and offsets to
        # actual values
        points = []
        prev_x = 0
        prev_y = 0
        for i in xrange(0, len(coords) - 1, 2):
            if coords[i] == 0 and coords[i + 1] == 0:
                continue

            prev_x += coords[i + 1]
            prev_y += coords[i]
            # a round to 6 digits ensures that the floats are the same as when
            # they were encoded
            points.append((round(prev_x, 6), round(prev_y, 6)))

        return points

class Valhalla:

    def __init__(self,host='http://192.168.99.100:5432', api_key =""):
        self.host = host
        self.api_key = api_key

    def route(self,start,end, costing='auto'):
        points = {"locations": [start,end]}
        url = self.host+'/route?json='+json.dumps(points)+ "&costing="+costing+"&api_key="+self.api_key
        print url

        resp = requests.get(url)
        return ValhallaRoute(json.loads(resp.text))

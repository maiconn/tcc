class Coord:
    def __init__(self, lat, longit):
        self.lat = lat
        self.longit = longit
    
    def json_dump(self):
        return dict(lat=self.lat, longit=self.longit)

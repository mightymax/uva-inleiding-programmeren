import re

class CarRide:
    data_points = []
    keys = []
    
    def __init__(self, csv_line = None, keys_line = None):
        if (csv_line == None):
            CarRide.keys = keys_line.split(',')
            # fix an error in the data file: duplicate columns 2 & 3:
            CarRide.keys.insert(3, 'xxx')
        else:
            csv_line = csv_line.split(',')
            _timestamp = csv_line[0].split()
            csv_line[0] = _timestamp[0]
            csv_line.insert(1, _timestamp[1])
            c = 0
            # create a key => value list, see dict() documentation
            for key in CarRide.keys:
                val = csv_line[c]
                if re.search(r"^\-?\d+\.\d+$", val):
                    val = float(val)
                elif re.search(r"^\-?\d+$", val):
                    val = int(val)
                setattr(self, key, val)
                c += 1
            CarRide.data_points.append(self)
    
    def load_from_file(filename):
        content = open(filename)
        lines = content.read().splitlines()
        content.close()

        i = 0
        for line in lines:
            if i == 0:
                CarRide(keys_line = line)
            else:
                CarRide(csv_line = line)
            i += 1
        
    def kmph(self):
        return round(self.speed * 3600 / 1000, 1)
    
    def count():
        return len(CarRide.data_points)
        
    # get total distance in km
    def dist():
        dist = 0
        for _data in CarRide.data_points:
            dist += _data.speed
        return round(dist / 1000, 1)
    
    def get_data_list(key):
        the_list = []
        for _data in CarRide.data_points:
            the_list.append(getattr(_data, key))
        return the_list
        
    def get_maps_url():
        # Construct Google Map URL:
        url = 'https://www.google.com/maps/dir/?api=1'

        origin = "&origin=%s,%s" % (CarRide.data_points[0].lat, CarRide.data_points[0].long)
        destination = "&destination=%s,%s" % (CarRide.data_points[CarRide.count() - 1].lat, CarRide.data_points[CarRide.count() - 1].long)

        waypoints = "&waypoints="
        for i in range(1, CarRide.count() - 1, 50):
            waypoints += "%s,%s|" % (CarRide.data_points[i].lat, CarRide.data_points[i].long)
        waypoints = waypoints[0:-1]
        return url + origin + destination + waypoints
        

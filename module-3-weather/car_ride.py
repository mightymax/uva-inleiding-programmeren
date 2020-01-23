# Name: Mark Lindeman
#
# see https://progbg.mprog.nl/weather/dataprocessing
import matplotlib.pyplot as plt, numpy, re

class car_ride:
    data_points = []
    keys = []
    
    def __init__(self, csv_line = None, keys_line = None):
        if (csv_line == None):
            car_ride.keys = keys_line.split(',')
            # fix an error in the data file: duplicate columns 2 & 3:
            car_ride.keys.insert(3, 'xxx')
        else:
            csv_line = csv_line.split(',')
            _timestamp = csv_line[0].split()
            csv_line[0] = _timestamp[0]
            csv_line.insert(1, _timestamp[1])
            c = 0
            # create a key => value list, see dict() documentation
            for key in car_ride.keys:
                val = csv_line[c]
                if re.search(r"^\-?\d+\.\d+$", val):
                    val = float(val)
                elif re.search(r"^\-?\d+$", val):
                    val = int(val)
                setattr(self, key, val)
                c += 1
            car_ride.data_points.append(self)
    
    def load_from_file(filename):
        content = open(filename)
        lines = content.read().splitlines()
        content.close()

        i = 0
        for line in lines:
            if i == 0:
                car_ride(keys_line = line)
            else:
                car_ride(csv_line = line)
            i += 1
        
    def kmph(self):
        return round(self.speed * 3600 / 1000, 1)
    
    def count():
        return len(car_ride.data_points)
        
    # get total distance in km
    def dist():
        dist = 0
        for _data in car_ride.data_points:
            dist += _data.speed
        return round(dist / 1000, 1)
    
    def get_data_list(key):
        the_list = []
        for _data in car_ride.data_points:
            the_list.append(getattr(_data, key))
        return the_list
        
    def get_maps_url():
        # Construct Google Map URL:
        url = 'https://www.google.com/maps/dir/?api=1'

        origin = "&origin=%s,%s" % (car_ride.data_points[0].lat, car_ride.data_points[0].long)
        destination = "&destination=%s,%s" % (car_ride.data_points[car_ride.count() - 1].lat, car_ride.data_points[car_ride.count() - 1].long)

        waypoints = "&waypoints="
        for i in range(1, car_ride.count() - 1, 50):
            waypoints += "%s,%s|" % (car_ride.data_points[i].lat, car_ride.data_points[i].long)
        waypoints = waypoints[0:-1]
        return url + origin + destination + waypoints
        
    
def main():
    car_ride.load_from_file('AutoRitData.csv')
    dist = car_ride.dist()

    speed = car_ride.get_data_list('speed')
    time = numpy.arange(0, car_ride.count(), 1)
    plt.figure(1)
    plt.subplot(121)
    plt.plot(time, speed, 'b-')
    plt.xlabel('time (s)', fontsize = 10, color = '#999999')
    plt.ylabel('speed (km/h)', fontsize = 10, color = '#999999')
    plt.title(("total traveled distance: %0.1f km" % dist), color = '#999999', fontsize = 14)
    plt.subplot(122)


    #Step 1: print line in green
    color = 'g-'
    plt.plot(car_ride.get_data_list('long'), car_ride.get_data_list('lat'), color)

    lats = []
    longs = []

    # step 2: print red segments:
    for location in car_ride.data_points:
        if location.kmph() < 50:
            speed_color = 'r-'
        else:
            speed_color = 'g-'
    
        if color == speed_color and color == 'r-':
            lats.append(location.lat)
            longs.append(location.long)
        else:
            if (color == 'r-'):
                plt.plot(longs, lats, color)
            color = speed_color
            lats = []
            longs = []

    if len(lats) > 0:
        plt.plot(longs, lats, color)
    
    plt.xlabel('lat', fontsize = 10, color = '#999999')
    plt.ylabel('long', fontsize = 10, color = '#999999')

    # print(car_ride.get_maps_url())
    plt.show()

  
if __name__== "__main__":
  main()



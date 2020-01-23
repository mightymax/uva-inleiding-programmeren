# Name: Mark Lindeman
#
# see https://progbg.mprog.nl/weather/dataprocessing
import matplotlib.pyplot as plt, numpy

def mps2kmph(mps):
    mps = float(mps)
    return round(mps * 3600 / 1000, 1)
    
car_data = []

#Create a list of all lines in the CSV file:
content = open('AutoRitData.csv')
lines = content.read().splitlines()
content.close()

#build a dictionary:
i = 0
for line in lines:
    if i == 0:
        keys = line.split(',')
        # fix an error in the data file: duplicate columns 2 & 3:
        keys.insert(3, 'xxx')
    else:
        _data = {}
        #The CSV file is comma seperated, but the first column is not ...
        line = line.split(',')
        _timestamp = line[0].split()
        line[0] = _timestamp[0]
        line.insert(1, _timestamp[1])
        c = 0
        # create a key => value list, see dict() documentation
        for key in keys:
            _data[key] = line[c]
            c += 1
        car_data.append(_data)
    i += 1
    
speed = []
time = []
locations = []
dist = 0
lats = []
longs = []

for _data in car_data:
    cur_speed = mps2kmph(_data['speed'])
    speed.append(cur_speed)
    locations.append({'speed': cur_speed, 'lat': float(_data['lat']), 'lon': float(_data['long'])})
    lats.append(float(_data['lat']))
    longs.append(float(_data['long']))
    dist += float(_data['speed'])
    
time = numpy.arange(0, len(speed), 1)
plt.figure(1)
plt.subplot(121)
plt.plot(time, speed, 'b-')
plt.xlabel('time (s)', fontsize = 10, color = '#999999')
plt.ylabel('speed (km/h)', fontsize = 10, color = '#999999')
plt.title(("total traveled distance: %0.1f km" % (dist / 1000)), color = '#999999', fontsize = 14)

plt.subplot(122)

#Step 1: print line in green
color = 'g-'
plt.plot(longs, lats, color)

lats = []
longs = []

# step 2: print red segments:
for location in locations:
    if location['speed'] < 50:
        speed_color = 'r-'
    else:
        speed_color = 'g-'
    
    if color == speed_color and color == 'r-':
        lats.append(location['lat'])
        longs.append(location['lon'])
    else:
        if (color == 'r-'):
            plt.plot(longs, lats, color)
        color = speed_color
        lats = []
        longs = []

if len(lats) > 0:
    plt.plot(longs, lats, color)
    
plt.xlabel('lat', fontsize = 10, color = '#999999')
plt.ylabel('lon', fontsize = 10, color = '#999999')

plt.show()

# Name: Mark Lindeman
#
# see https://progbg.mprog.nl/weather/dataprocessing
import matplotlib.pyplot as plt, numpy
from CarRide import CarRide 
    
CarRide.load_from_file('AutoRitData.csv')
dist = CarRide.dist()

speed = CarRide.get_data_list('speed')
time = numpy.arange(0, CarRide.count(), 1)
plt.figure(1)
plt.subplot(121)
plt.plot(time, speed, 'b-')
plt.xlabel('time (s)', fontsize = 10, color = '#999999')
plt.ylabel('speed (km/h)', fontsize = 10, color = '#999999')
plt.title(("total traveled distance: %0.1f km" % dist), color = '#999999', fontsize = 14)
plt.subplot(122)


#Step 1: print line in green
color = 'g-'
plt.plot(CarRide.get_data_list('long'), CarRide.get_data_list('lat'), color)

lats = []
longs = []

# step 2: print red segments:
for location in CarRide.data_points:
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

print(CarRide.get_maps_url())
plt.show()



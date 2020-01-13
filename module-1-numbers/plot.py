# Name: Mark Lindeman
#
# This program plots a graph of the function f(x) = x^x between x=0 and x = 1.5 with steps of 0.01.
# see https://progbg.mprog.nl/numbers/plot

import matplotlib.pyplot as plt
import numpy

# the list of x-coordinates
x_coords = numpy.arange(0, 1.5, 0.01)

y_min = None

#calculate y-coords list and get the min value for y
y_coords = []
for x in x_coords:
    y = x ** x
    if y_min is None or y < y_min:
        y_min = y
        x_min = x
    y_coords.append(y)

txt = "(xmin, ymin) = (%0.2f, %0.2f)" % (x_min, y_min)

#get the middle of the Y-axis so we can display the text in the center of the plot
y_mid = y_min + ((max(y_coords) - y_min) / 2)

# plot points (y to x) with green circles
plt.plot(x_coords, y_coords, 'b-', [x_min], [y_min], 'ro')
plt.text(0.18, y_mid , txt, color = 'black', fontsize = 14)

#Make sure the x-axis starts at y=0:
plt.axis([0, 1.6, 0.6, 2.0])

plt.show()
plt.savefig('plot.png')

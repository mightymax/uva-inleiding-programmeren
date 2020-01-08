import matplotlib.pyplot as plt
import numpy

# the coordinates per point
x_coords = numpy.arange(0, 1.5, 0.01)

x_min = 0
y_min = 1.5

y_coords = []
for x in x_coords:
    y = x ** x
    if y < y_min:
        y_min = y
        x_min = x
    y_coords.append(y)


print(f"xmin = {x_min}, y_min = {y_min}")


#get the middle of the Y-axis so we can display the text in the center of the plot
y_mid = y_min + ((max(y_coords) - y_min) / 2)

# plot points (y to x) with green circles
plt.plot(x_coords, y_coords, 'b-', [x_min], [y_min], 'ro')
plt.text(0, y_mid , "(x_min, y_min) = (%0.2f, %0.2f)" % (x_min, y_min), color = 'black', fontsize = 14)

print("(x_min, y_min) = (%0.2f, %0.2f)" % (x_min, y_min))
plt.show()
# plt.savefig('plot.png')

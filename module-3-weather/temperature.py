import matplotlib
import matplotlib.pyplot as plt

from Temps import Temperature
    
Temperature.load_from_file('DeBiltTempMinOLD.txt', 'DeBiltTempMaxOLD.txt')

#Assignment 1: extreme temperatures
def assigment1():
    data = Temperature.get_min_max_temp()
    print("The highest temperature was %01.fºC and was measured at %s, on that day it was not colder than %0.1fºC." % (data['max'].max, data['max'].date_format(), data['max'].min))
    print("The lowest temperature was %01.fºC and was measured at %s, on that day it was not warmer than %0.1fºC." % (data['min'].min, data['min'].date_format(), data['min'].max))
    
# Assignment 2: cold colder coldest
def assigment2():
    streak = Temperature.get_coldest_streak()
    no_of_days = len(streak)
    start_streak = streak.pop(0)
    end_streak = streak.pop()
    print("The longest period of uninterrupted days that had freezing temperatures started on %s and ended on %s (%d days)." % (start_streak.date_format(), end_streak.date_format(), no_of_days))

# Assignment 3: Summer days and tropical days
def assigment3():
    data = Temperature.get_hot_days()
    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.xlabel('Year')
    plt.ylabel('Days')
    plt.title('Number of Summer & Tropical days per year')
    plt.plot(data['years'], data['summer_days'], "-y", label="Summer (t>%dºC)" % Temperature.summer_min_temp)
    plt.plot(data['years'], data['tropical_days'], "-r", label="Tropical (t>%dºC)" % Temperature.tropical_min_temp)
    plt.legend(loc="upper left")
    plt.show()
    
# Assignment 4: First heat wave
def assigment4():
    heat_wave = Temperature.get_heat_waves().pop(0)
    summer_day_count = len(heat_wave)
    tropical_day_count = 0
    for _temp in heat_wave:
        if _temp.is_tropical():
            tropical_day_count += 1
    y = heat_wave[0].date_format(get_year = True)
    start_date = heat_wave[0].date_format()
    end_date = heat_wave.pop().date_format()
    print("The first year in which a heat wave occurred was %d: from %s thru %s there were %d summer days (>%dºC) including %d tropical days (>%dºC)." % (y, start_date, end_date, summer_day_count, Temperature.summer_min_temp, tropical_day_count, Temperature.tropical_min_temp))

assigment1()
assigment2()
assigment4()
assigment3()





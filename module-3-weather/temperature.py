import matplotlib
import matplotlib.pyplot as plt

def parse_temparature_files ():
    content = open('DeBiltTempMinOLD.txt')
    lines_min_temps = content.read().splitlines()
    content.close()

    content = open('DeBiltTempMaxOLD.txt')
    lines_max_temps = content.read().splitlines()
    content.close()

    start = 0
    temperatures = []

    line_no = 0
    for line in lines_min_temps:
        if start == 0 and line.strip()[0:6] == 'STAID,':
            start = 1
        elif start == 1:
            _temp = {}
            _temp['date'] = int(line[14:22])
            _temp['min'] = int(line[23:28])
            _temp['max'] = int(lines_max_temps[line_no][23:28])
            temperatures.append(_temp)
        line_no += 1
    return temperatures
  
def date_format(yyyymmdd):
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    yyyymmdd = str(yyyymmdd)
    year = get_year(yyyymmdd)
    month_no = int(yyyymmdd[4:6])
    day = int(yyyymmdd[6:8])
    
    return "%d %s %d" % (day, months[month_no], year)
    
def get_year(yyyymmdd):
    yyyymmdd = str(yyyymmdd)
    return int(yyyymmdd[0:4])
    
#Assignment 1: extreme temperatures
def assigment1(temperatures):
    min_temp = {'date': 0, 'min': 100}
    max_temp = {'date': 0, 'max': -256}

    for temperature in temperatures:
        if temperature['min'] < min_temp['min']:
            min_temp = temperature
        if temperature['max'] > max_temp['max']:
            max_temp = temperature

    print("The highest temperature was %01.fºC and was measured at %s, on that day it was not colder than %0.1fºC." % (max_temp['max']/10, date_format(max_temp['date']), max_temp['min']/10))
    print("The lowest temperature was %01.fºC and was measured at %s, on that day it was not warmer than %0.1fºC." % (min_temp['min']/10, date_format(min_temp['date']), min_temp['max']/10))
    
# Assignment 2: cold colder coldest
def assigment2(temparatures):
    streek = []
    current_streek = []
    for temperature in temperatures:
        if temperature['max'] < 0 and len(current_streek) == 0:
            current_streek.append(temperature)
        elif temperature['max'] < 0 and temperature['date'] - 1 == current_streek[len(current_streek) - 1]['date']:
            current_streek.append(temperature)
        elif temperature['max'] < 0 and temperature['date'] - 1 != current_streek[len(current_streek) - 1]['date']:
            if len(current_streek) > len(streek):
                streek = current_streek
            current_streek = []
            current_streek.append(temperature)
    start_date = date_format(streek[0]['date'])
    end_date = date_format(streek[len(streek) - 1]['date'])
    no_of_days = len(streek)
    print("The longest period of uninterrupted days that had freezing temperatures started on %s and ended on %s (%d days)." % (start_date, end_date, no_of_days))

# Assignment 3: Summer days and tropical days
def assigment3(temparatures):
    years = []
    summer_days = []
    tropical_days = []
    ix = -1
    for temparature in temparatures:
        year = get_year(temparature['date'])
        if year not in years:
            years.append(year)
            summer_days.append(0)
            tropical_days.append(0)
            ix += 1
        if temparature['max'] >= 300:
            tropical_days[ix] += 1
        elif temparature['max'] > 250:
            summer_days[ix] += 1
            
    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.xlabel('Year')
    plt.ylabel('Days')
    plt.title('Number of Summer & Tropical days per year')
    plt.plot(years, summer_days, "-y", label="Summer (t>25ºC)")
    plt.plot(years, tropical_days, "-r", label="Tropical (t>30ºC)")
    plt.legend(loc="upper left")
    plt.show()
    
# Assignment 4: First heat wave
def assigment4(temperatures):
    streek = []
    current_streek = []
    for temperature in temperatures:
        if temperature['max'] > 250 and len(current_streek) == 0:
            current_streek.append(temperature)
        elif temperature['max'] > 250 and temperature['date'] - 1 == current_streek[len(current_streek) - 1]['date']:
            current_streek.append(temperature)
        elif temperature['max'] > 250 and temperature['date'] - 1 != current_streek[len(current_streek) - 1]['date']:
            if len(current_streek) > len(streek) and len(current_streek) >= 5:
                tropical_day_count = 0
                for _temp in current_streek:
                    if _temp['max'] >= 300:
                        tropical_day_count += 1
                if tropical_day_count >= 3:
                    streek = current_streek
                    break
            current_streek = []
            current_streek.append(temperature)
    y = get_year(streek[0]['date'])
    start_date = date_format(streek[0]['date'])
    end_date = date_format(streek[len(streek) - 1]['date'])
    summer_day_count = len(streek)
    
    print("The first year in which a heat wave occurred was %d: from %s thru %s there were %d summer days (>25ºC) including %d tropical days (>30ºC)." % (y, start_date, end_date, summer_day_count, tropical_day_count))
    
temperatures = parse_temparature_files()
assigment1(temperatures)
assigment2(temperatures)
assigment4(temperatures)
assigment3(temperatures)





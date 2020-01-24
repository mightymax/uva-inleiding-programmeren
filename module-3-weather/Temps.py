from datetime import datetime
import re, sys

class Temperature:
    
    data = []
    
    summer_min_temp = 25
    tropical_min_temp = 30
    
    def __init__(self, date = 19700101, tMin = 100, tMax = -256):
        self.date = Temperature.to_datetime(date)
        self.min = int(tMin)/10
        self.max = int(tMax)/10
    
    def to_datetime(yyyymmdd):
        match = re.search(r"^([1-2]\d{3})([0-1][0-9])([0-3][0-9])$", str(yyyymmdd))
        if not match:
            raise ValueError(f"Argument '{yyyymmdd}' is not a valid yyyymmdd format.")
        return  datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        
    def date_format(self, format = '%A %d %B %Y'):
        return self.date.strftime(format)

    def day_diff(self, compare_temperature_object):
        return self.yyyymmdd - compare_temperature_object.yyyymmdd
        
    @property
    def year(self):
        return int(self.date_format('%Y'))
            
    @property
    def yyyymmdd(self):
        return int(self.date_format("%Y%m%d"))
            
    def is_tropical(self, get_from_prop = 'max'):
        val = getattr(self, get_from_prop)
        return val >= Temperature.tropical_min_temp
        
    def is_summer(self, get_from_prop = 'max'):
        val = getattr(self, get_from_prop)
        return val > Temperature.summer_min_temp
        
    def load_from_file(filename_min_temps, filename_max_temps):
        content = open(filename_min_temps)
        lines_min_temps = content.read().splitlines()
        content.close()

        content = open(filename_max_temps)
        lines_max_temps = content.read().splitlines()
        content.close()

        start = 0
        line_no = 0
        temperatures = []
        for line in lines_min_temps:
            if start == 0 and line.strip()[0:6] == 'STAID,':
                start = 1
            elif start == 1:
                Temperature.data.append(Temperature(date=line[14:22], tMin = line[23:28], tMax = lines_max_temps[line_no][23:28]))
            line_no += 1
    
    def get_min_max_temp():
        min_temp = Temperature()
        max_temp = Temperature()

        for temperature in Temperature.data:
            if temperature.min < min_temp.min:
                min_temp = temperature
            if temperature.max > max_temp.max:
                max_temp = temperature

        return {'min': min_temp, 'max': max_temp}
        
    def get_coldest_streak():
        streak = []
        current_streak = []
        for temperature in Temperature.data:
            if temperature.max < 0 and len(current_streak) == 0:
                current_streak.append(temperature)
            elif temperature.max < 0 and temperature.day_diff(current_streak[len(current_streak) - 1]) == 1:
                current_streak.append(temperature)
            elif temperature.max < 0 and temperature.day_diff(current_streak[len(current_streak) - 1]) != 1:
                if len(current_streak) > len(streak):
                    streak = current_streak
                current_streak = []
                current_streak.append(temperature)
        return streak
        
    def get_heat_waves():
        heat_waves = []
        streak = []
        current_streak = []
        for temperature in Temperature.data:
            if temperature.is_summer() and len(current_streak) == 0:
                current_streak.append(temperature)
            elif temperature.is_summer() and temperature.day_diff(current_streak[len(current_streak) - 1]) == 1:
                current_streak.append(temperature)
            elif temperature.is_summer() and temperature.day_diff(current_streak[len(current_streak) - 1]) != 1:
                if len(current_streak) > len(streak) and len(current_streak) >= 5:
                    tropical_day_count = 0
                    for _temp in current_streak:
                        if _temp.is_tropical():
                            tropical_day_count += 1
                    if tropical_day_count >= 3:
                        heat_waves.append(current_streak)
                current_streak = []
                current_streak.append(temperature)
        return heat_waves
        
    def get_hot_days():
        years = []
        summer_days = []
        tropical_days = []
        ix = -1
        for temparature in Temperature.data:
            if temparature.year not in years:
                years.append(temparature.year)
                summer_days.append(0)
                tropical_days.append(0)
                ix += 1
            if temparature.is_tropical():
                tropical_days[ix] += 1
            elif temparature.is_summer():
                summer_days[ix] += 1
                
        return {'years': years, 'summer_days': summer_days, 'tropical_days': tropical_days}
        
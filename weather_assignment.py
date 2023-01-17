import json

with open('precipitation.json') as f:
    measurements = json.load(f)

#from our csv file, i know the station code for seattle is GHCND:US1WAKG0038

#----------------------------------------------------------------------------------

#calculating total precipation per month for seattle:


#selecting all measurements for seattle from our original list of measurements:
measurements_seattle = []

for measurement in measurements:
    if measurement['station'] == 'GHCND:US1WAKG0038':
        measurements_seattle.append(measurement)

print(len(measurements_seattle))

#from looking at our data, i know all of our data was collected in the year 2010, so each date will start with 2010-month
total_monthly_precipitation = [0,0,0,0,0,0,0,0,0,0,0,0,] #creating a list in which we will collect our data, starting at 0 for each month

for i in range(1,10): #for our single-digit months, so january - september
    for measurement in measurements_seattle: #for each measurement
        if  measurement['date'].startswith(f'2010-0{i}'): #if that measurement is in that month
            total_monthly_precipitation[i-1] += measurement['value'] #add the value up to the corresponding item in our list

for i in range(10,13): #for october - december
    for measurement in measurements_seattle: #for each measurement
        if  measurement['date'].startswith(f'2010-{i}'): #if that measurement is in that month
            total_monthly_precipitation[i-1] += measurement['value'] #add the value up to the corresponding item in our list


with open('results.json', 'w') as f:
    json.dump(total_monthly_precipitation, f, indent=4)




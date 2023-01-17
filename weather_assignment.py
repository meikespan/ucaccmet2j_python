import json
from csv import DictReader

##-------------------------------------------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------------
#first, we need to set everything up:


#opening our measurements and loading it into a list of dictionaries with each item being measurement and its information
with open('precipitation.json') as f:
    measurements = json.load(f)

#loading our stations and storing it in a list of dictionaries with our locations and their information
with open('stations.csv') as csvfile:
    stationsfile = DictReader(csvfile)
    stations = list(stationsfile)

#creating an empty directory in which we can later store all our data
results = {}

#calculating the total precipitation across all stations, so the sum off all measurements
total_yearly_precipitation_across_all_stations = sum(measurement['value'] for measurement in measurements)

sum_relative_yearly_precipitation = 0

##-------------------------------------------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------------
#now, we can start calculating our informative datapoints:


# creating a loop that calculates everything for each station
for station in stations:

#getting the keys we need to get the measurements and information for each station
    station_name = station['Location']
    station_state = station['State']
    station_code = station['Station']


#--------------------------------------------------------------------------------------------------------
    #calculating the total monthly  precipation

    total_monthly_precipitation = [0]*12 #creating a list in which we will collect our data, starting at 0 for each month

    for measurement in measurements:  # for each measurment in our file, we are going to evaluate:
        if measurement['station'] == station_code: # wether it is a measurement at the station we are currently working on

            #in which month it was collected, after which we add it to its index in our total month list
            #from looking at our data, i know all of our data was collected in the year 2010, so each date will start with 2010-month
            for i in range(1,10): #for our single-digit months, so january - september
                if  measurement['date'].startswith(f'2010-0{i}'): #if that measurement is in that month
                    total_monthly_precipitation[i-1] += measurement['value'] #add the value up to the corresponding item in our list

            for i in range(10,13): #for october - december
                if  measurement['date'].startswith(f'2010-{i}'): #if that measurement is in that month
                    total_monthly_precipitation[i-1] += measurement['value'] #add the value up to the corresponding item in our list

#--------------------------------------------------------------------------------------------------------
    #calculating the total yearly precipation
    total_yearly_precipitation = sum(total_monthly_precipitation)

#----------------------------------------------------------------------------------------------------------
    # calculating the relative monthly precipation
    relative_monthly_precipitation = [0]*12

    for i in range(1,13):
        relative_monthly_precipitation[i-1] = total_monthly_precipitation[i-1]/total_yearly_precipitation

#----------------------------------------------------------------------------------------------------------
    # calculating the relative yearly precipation
    relative_yearly_precipitation = total_yearly_precipitation/total_yearly_precipitation_across_all_stations

#-----------------------------------------------------------------------------------------------------------
    #output our results for each station into our results dictionary
    results[station_name] = {
        'station': station_code,
        'state': station_state,
        'total_monthly_precipitation': total_monthly_precipitation,
        'total_yearly_precipitation' : total_yearly_precipitation,
        'relative_monthly_precipitation' :relative_monthly_precipitation,
        'relative_yearly_precipitation': relative_yearly_precipitation
    }

##-------------------------------------------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------------
# now, we can store all our new informatin into an output file:

# outputting our results dictionary with all our data into our json file
with open('results.json', 'w') as f:
    json.dump(results, f, indent=4)
import json
from csv import DictReader

##-------------------------------------------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------------
#first, we need to set everything up:


#opening our measurements and loading it into a list of dictionaries with each item being a measurement and its information
with open('precipitation.json') as f:
    measurements = json.load(f)

#loading our stations and storing it in a list of dictionaries with our locations and their information
with open('stations.csv') as csvfile:
    stationsfile = DictReader(csvfile)
    stations = list(stationsfile)

#creating an empty directory in which we can later store all our results
results = {}

#calculating the total precipitation across all stations, so the sum off all measurements, so we can use it later:
total_yearly_precipitation_across_all_stations = sum(measurement['value'] for measurement in measurements)


##-------------------------------------------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------------
#now, we can start calculating our informative datapoints:


# creating a loop that calculates everything for each station seperately
for station in stations:

#getting the keys we need to get the measurements and information for our current specific station
    station_name = station['Location']
    station_state = station['State']
    station_code = station['Station']


#--------------------------------------------------------------------------------------------------------
    #calculating the total monthly  precipation

    total_monthly_precipitation = [0]*12 #creating a list in which we will collect our data, starting at 0 for each month

    for measurement in measurements:  # for each measurement in our file, we are going to evaluate:
        if measurement['station'] == station_code: # wether it is a measurement at the station we are currently working on, and if it is:
            
            #in which month it was collected, after which we add it to the sum at the corresponding index in our total month list
            for i in range(1,13): #for each month seperately, we are telling it to
                if i < 10:  #for january-september, make sure the month is denoted by two numbers, 01, 02 etc. instead of 1, 2
                    i = f'0{i}'
                if  measurement['date'].startswith(f'{i}', 5): #if the date for each measurement has the month code we are looking for in this loop on position 6 (as each date starts with 2010-):
                    total_monthly_precipitation[int(i)-1] += measurement['value'] #add the value to our month total in the correct index of our list for this month
                    
#--------------------------------------------------------------------------------------------------------
    #calculating the total yearly precipation
    total_yearly_precipitation = sum(total_monthly_precipitation)

#----------------------------------------------------------------------------------------------------------
    # calculating the relative monthly precipation
    relative_monthly_precipitation = [0]*12

    for i in range(1,13): # for month 1-12
        relative_monthly_precipitation[i-1] = total_monthly_precipitation[i-1]/total_yearly_precipitation #calculate the relative precipation per that month

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
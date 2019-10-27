import requests 
from datetime import datetime

URL = "https://api.coinranking.com/v1/public/coin/1/history/30d"
response = requests.get(URL)
data = response.json() 

entries_number = 24 * 30 
print(entries_number) 

all_dates = {} 
for i in range(0,entries_number): 
    timestamp = data['data']['history'][i]['timestamp']
    string_timestamp = str(timestamp)
    full_timestamp = datetime.fromtimestamp(int(string_timestamp[0:10]))
    date = str(full_timestamp)[0:10]

    if date not in all_dates: 
        all_dates[date] = 1 
    else: 
        all_dates[date] = all_dates[date] + 1 

print(all_dates)

def getDailyReport(occurances, day, start): 
    daily_report = {} 
    day_range = [] 
    timestamp = "" 
    days_of_the_week = {0:'Monday', 1:'Tuesday', 2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    for i in range(start,occurances):   
        day_range.append(data['data']['history'][i]['price'])

    daily_report['date'] = day + "T00:00:00"
    #print(type(datetime.strptime(day, '%Y-%m-%d')))
    daily_report['dayOfWeek'] = days_of_the_week.get(datetime.strptime(day, '%Y-%m-%d').weekday())
    daily_report['price'] = max(day_range) 
    return daily_report 

full_report = []
previousPrice = 0.0 
highSinceStart = 0.0
lowSinceStart = 100000.0 
start = 0 
occurances = 0 
for day in all_dates: 
    higest = False 
    lowest = False 
    occurances = occurances + all_dates.get(day)
    daily_report = getDailyReport(occurances,day,start) 
    start = start + all_dates.get(day)
    if (float(highSinceStart) < float(daily_report['price'])): 
        highSinceStart = daily_report['price'] 
        highest = True 
    elif (float(lowSinceStart) > float(daily_report['price'])): 
        lowSinceStart = daily_report['price']
        lowest = True 

    if highest == True: 
        daily_report['highest'] = 'True' 
    elif lowest == True: 
        daily_report['lowest'] = 'True' 

    if previousPrice == 0.0: 
        daily_report['change'] = 'na'
    else:
        daily_report['change'] = float(daily_report['price']) - float(previousPrice)

    daily_report['highSinceStart'] = highSinceStart
    daily_report['lowSinceStart'] = lowSinceStart 
    if float(previousPrice) > float(daily_report['price']): 
        daily_report['direction'] = 'Up' 
    elif float(previousPrice) < float(daily_report['price']): 
        daily_report['direction'] = 'Down'
    else: 
        daily_report['direction'] = 'Same'
    previousPrice = daily_report['price'] 
    full_report.append(daily_report) 

print(full_report)




    

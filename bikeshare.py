#import relevant packages
import time #needed to calculate program run time
import pandas as pd
import numpy as np
import calendar #needed to convert month number to month name, found on Stackoverflow post: https://stackoverflow.com/questions/6557553/get-month-name-from-number


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#welcome message
print("Hello! Let\'s analyze some bikeshare data!")

#create analysis function
def load_data(city, month, day): #load chosen city, month and day into function

    print('\nCalculating bikeshare statistics...\n')
    start_time = time.time() #get start time to calculate total run time

    city = city.lower()
    month = month.lower()

    df = pd.read_csv(CITY_DATA[city]) #read appropriate data file

    #convert Start Time column to datetime
    #extract month, day of week, hour from datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    df['combo_station'] = df['Start Station'] + ' and ' + df['End Station'] #create combo station for start and end stations

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    else:
        pop_month = df['month'].mode()[0]
        pop_month = calendar.month_name[pop_month] #converting month number to month name
        print('Most Popular Month:', pop_month)

    #filter by day of week if applicable
    if day != 'All':
        df = df[df['day_of_week'] == day]
    else:
        pop_day = df['day_of_week'].mode()[0]
        print('Most Popular Day of Week:', pop_day)

    #calculate most popular start hour
    pop_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', pop_hour)

    #calculate most popular start and end stations, and combination of start and end stations
    pop_start = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', pop_start)

    pop_end = df['End Station'].mode()[0]
    print('Most Popular End Station:', pop_end)

    pop_combo = df['combo_station'].mode()[0]
    print('Most Popular Combination of Start and End Stations:', pop_combo)

    #calculate total trip time and average trip time
    total_time = round(df['Trip Duration'].sum()/8640)
    print('Total Travel Time:', total_time, 'days')

    average_time = round(df['Trip Duration'].mean()/60, 2)
    print('Average Travel Time:', average_time, ' minutes')

    #calculate user counts
    user_count = df['User Type'].value_counts()
    print('Count of Each User Type: \n', user_count)

    #calculate gender counts, only availabe in Chicago and New York City
    if city == 'chicago' or city == 'new york city':
        gender_count = df['Gender'].value_counts()
        print('Count of Each Gender: \n', gender_count)
    else:
        print('No Customer Gender Information for', city.title())

    #calculate birth year stats, only availabe in Chicago and New York City
    if city == 'chicago' or city == 'new york city':
        earliest_year = int(df['Birth Year'].min())
        latest_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('Earliest Customer Birth Year:', earliest_year)
        print('Most Recent Customer Birth Year:', latest_year)
        print('Most Common Customer Birth Year:', most_common_year)
    else:
        print('No Customer Birth Year Information for', city.title())

    #print total run time
    calc_time = time.time() - start_time
    print('Calculation time:', calc_time, 'seconds')


#create while loop to allow for additional runs
lets_analyze = 'Yes'
while lets_analyze.lower() == 'yes':

    #create while loops to account for user input errors for city, month and day
    while True:
        city = input('Enter a city to analyze, either Chicago, New York City, or Washington: ')
        if city.lower() in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Not a valid city, please try again.')

    while True:
        month = input('Enter a month from January through June, to analyze, or choose "All": ')
        if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june','all']:
            break
        else:
            print('Not a valid month, please try again.')

    while True:
        day = input('Enter a day of the week, Sunday through Saturday, to analyze, or choose "All": ')
        if day.lower() in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','all']:
            break
        else:
            print('Not a valid day, please try again.')

    load_data(city, month, day)

    #create while loop to allow user to see 5 rows of raw data, and to prompt to see additional 5 rows until user says 'No'
    raw_data = input('Would you like to see 5 rows of raw data? Enter "Yes" or "No": ')

    df = pd.read_csv(CITY_DATA[city.lower()])

    n = 0
    m = 5

    while raw_data.lower() == 'yes':
        print(df[n:m])
        n += 5
        m += 5
        raw_data = input('Would you like to see 5 more rows of raw data? Enter "Yes" or "No": ')

    lets_analyze = input('Would you like to see additional metrics? Enter "Yes" or "No": ')

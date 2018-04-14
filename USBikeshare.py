import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ["chicago", "new york city", "washington"]
    while True:
    	print("List of available cities : "+str(valid_cities))
    	city = input("Enter a city\n")
    	city = city.lower()
    	if city in valid_cities:
    		city = CITY_DATA[city]
    		break
    	else:
    		print("INVALID CITY")

    # get user input for month (all, january, february, ... , june)
    valid_month = ["all", "january", "february", "march", "april", "may", "june"]
    while True:
    	print("Enter a month between january to june (both inclusive) or Enter 'all' for no month filter")
    	month = input()
    	month = month.lower()
    	if month in valid_month:
    		break
    	else:
    		print("INVALID MONTH")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
    	print("Enter a valid weekday or Enter 'all' for no day filter")
    	day = input()
    	day = day.lower()
    	if day in valid_days:
    		break
    	else:
    		print("INVALID DAY")

    print('-'*40) #
    return city, month, day

def get_weekday(day):
	if day == "monday":
		return 0
	elif day == "tuesday":
		return 1
	elif day == "wednesday":
		return 2
	elif day == "thursday":
		return 3
	elif day == "friday":
		return 4
	elif day == "saturday":
		return 5
	else:
		return 6
	    
def get_weekday_word(day):
	if day == 0:
		return "monday"
	elif day == 1:
		return "tuesday"
	elif day == 2:
		return "wednesday"
	elif day == 3:
		return "thursday"
	elif day == 4:
		return "friday"
	elif day == 5:
		return "saturday"
	else:
		return "sunday"

def get_month_word(month):
	if month == 1:
		return "january"
	elif month == 2:
		return "february"
	elif month == 3:
		return "march"
	elif month == 4:
		return "april"
	elif month == 5:
		return "may"
	elif month == 6:
		return "june"

def get_month(month):
	if month == "january":
		return 1
	elif month == "february":
		return 2
	elif month == "march":
		return 3
	elif month == "april":
		return 4
	elif month == "may":
		return 5
	else:
		return 6

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city) 
    if month != "all" and day != "all":
      weekday = get_weekday(day)
      month_value = get_month(month)
      df['Start Time'] = pd.to_datetime(df['Start Time'])
      df = df[df['Start Time'].dt.month == month_value]
      df = df[df['Start Time'].dt.dayofweek == weekday]
    elif month != "all" and day == "all":
    	month_value = get_month(month)
    	df['Start Time'] = pd.to_datetime(df['Start Time'])
    	df = df[df['Start Time'].dt.month == month_value]
    elif month == "all" and day != "all":
    	weekday = get_weekday(day)
    	df['Start Time'] = pd.to_datetime(df['Start Time'])
    	df = df[df['Start Time'].dt.dayofweek == weekday]

    return df

def time_stats(df, filtered):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['Start Month'] = df['Start Time'].dt.month
    popular_month = df['Start Month'].mode()[0]
    count  = df['Start Month'].value_counts().max()
    print("Most Popular Month : "+str(get_month_word(popular_month))+", Count : "+str(count)+", Filter : "+filtered)

    # display the most common day of week
    df['Start Day'] = df['Start Time'].dt.dayofweek
    popular_day = df['Start Day'].mode()[0]
    count = df['Start Day'].value_counts().max()
    print("Most Popular Day : "+str(get_weekday_word(popular_day))+", Count : "+str(count)+", Filter : "+filtered)

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    count = df['Start Hour'].value_counts().max()
    print("Most Popular Hour : "+str(popular_hour)+", Count : "+str(count)+", Filter : "+filtered)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filtered):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count = df['Start Station'].value_counts().max()
    print("Popular Start Station : "+str(popular_start_station)+", Count : "+str(count)+", Filter : "+filtered)


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count = df['End Station'].value_counts().max()
    print("Popular End Station : "+str(popular_end_station)+", Count : "+str(count)+", Filter : "+filtered)

    # display most frequent combination of start station and end station trip
    df['x'] = df['Start Station'] +" -> "+df['End Station']
    popular_trip = df['x'].mode()[0]
    count = df['x'].value_counts().max()
    print("Popular Trip : "+str(popular_trip)+", Count : "+str(count)+", Filter : "+filtered)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filtered):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_time = df['Trip Duration'].sum()
    print("Total Trip Time : "+str(trip_time)+", Count : "+str(df.shape[0])+", Filter : "+filtered)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean Trip Time : "+str(mean_time)+", Count : "+str(df.shape[0])+", Filter : "+filtered)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, filtered):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Subscribers : "+str(df[df['User Type']=="Subscriber"].shape[0])+", Customers : "+str(df[df['User Type']=="Customer"].shape[0])+", Filter : "+filtered)
    try:
    	# Display counts of gender
    	print("Male count : "+str(df[df['Gender']=="Male"].shape[0])+", Female Count : "+str(df[df['Gender']=="Female"].shape[0])+", Filter : "+filtered)

    	# Display earliest, most recent, and most common year of birth
    	print("Earliest Y.o.B : "+str(df['Birth Year'].min())+", Recent Y.o.B : "+str(df['Birth Year'].max())+", Most Common Y.o.B : "+str(df['Birth Year'].mode()[0])+", Filter : "+filtered)
    except:
    	print("Washington City Does not maintain Gender and Birth of Year Records")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if month != "all" and day != "all":
        	filtered = month + " & "+day 
        elif month != "all" and day == "all":
        	filtered = month
        elif month == "all" and day != "all":
        	filtered = day
        else:
        	filtered = "no filter applied"
        time_stats(df, filtered)
        station_stats(df, filtered)
        trip_duration_stats(df, filtered)
        user_stats(df, filtered)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
	main()

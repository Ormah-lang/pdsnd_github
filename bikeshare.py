import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_valid_city_from_user():
    """
    Gets valid city from user and handles invalid user input

    Returns:
        (str) city - name of the valid city
    """
    city = input('Enter your city (city should be from chicago, new york city or washington): ').strip().lower()             
    while city not in CITY_DATA:         
        print('Please enter a valid city')
        city = input('Enter your city (city should be from chicago, new york city or washington): ').strip().lower()
    return city

def get_valid_month_from_user():
    """
    Gets valid month of the year from user and handles invalid user input.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    valid_months = {'all', 'january','febuary', 'march', 'april', 'may', 'june'}
    month = input('Enter a month from January to June or type \'all\' for all months: ').strip().lower()
    while month not in valid_months:
        month = input('Please enter a valid month from January to June or type \'all\' for all months: ').strip().lower()
    return month

def get_valid_day_from_user():
    """
    Gets valid day of the week from user and handles invalid user input.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_days = {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    day = input('Enter the day of the week or type \'all\' for all days of the week: ').strip().lower()
    while day not in valid_days:
        day = input('Please enter a valid day of the week or type \'all\' for all days of the week: ') 
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington)
    city = get_valid_city_from_user()
        
    # get user input for month (all, january, february, ... , june)
    month = get_valid_month_from_user()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_day_from_user()
        
    print('-'*40)
    return city, month, day


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
  
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of the week: ', common_day_of_week)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common starting hour is: ', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ',  most_used_start_station)

    # display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ',  most_used_end_station)

    # display most frequent combination of start station and end station trip
    df['Frequent Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination_trip = df['Frequent Trip'].mode()[0]
    print('The most frequent combination of start and end station trip: ', common_combination_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print ('The total travel time is: ', total)

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print ('The mean travel time is: ', mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('The user type count is:\n', str(user_type_count))
    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('The user type count is:\n', str(gender_count))
    else:    
        print('Sorry, gender stats cannot be calculated because it does not exist in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print('The earliest year of birth is: ', earliest_birth_year)   
          
        recent_birth_year = int(df['Birth Year'].max())
        print('The most recent year of birth is: ', recent_birth_year)       
          
        most_birth_year= int(df['Birth Year'].mode()[0])
        print('The most common year of birth is: ', most_birth_year)
    else:    
        print('Sorry, year of birth stats cannot be calculated because it does not exist in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

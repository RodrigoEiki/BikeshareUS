import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

day_selection = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

month_selection = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

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
    while True:
        city = input('Which city do you want to analyse? chicago, new york city, washington \n').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Now tell me what month? all or -> january, february, march, ..., december \n').lower()
        if month in month_selection:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Now tell me what day of week? all or -> monday, tuesday, ... sunday \n').lower()
        if day in day_selection:
            break

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
    #loads data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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
    most_common_month = df['month'].value_counts().idxmax()
    print('The most common month:', most_common_month)
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print('The most common day of week:', most_common_day_of_week)
    
    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print('The most common start hour:', most_common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print('Most common Start Station:', most_common_start_station)
    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print('Most common End Station:', most_common_end_station)
    # display most frequent combination of start station and end station trip
    most_combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'The most frequent combination of start station and end stations trip: {most_combination_station[0], {most_combination_station[1]}}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time
    total_travel_time = df["Trip Duration"].sum()
    print('Total travel time:', total_travel_time)

    # displays mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    key_counts_user_types = df['User Type'].value_counts().keys().tolist()
    counts_user_types = df['User Type'].value_counts().tolist()
    print(f'{key_counts_user_types[0]}:{counts_user_types[0]}')
    print(f'{key_counts_user_types[1]}:{counts_user_types[1]}')

    # Display counts of gender
    if 'Gender' in df.columns:
        key_counts_gender = df['Gender'].value_counts().keys().tolist()
        counts_gender = df['Gender'].value_counts().tolist()
        print(f'{key_counts_gender[0]}:{counts_gender[0]}')
        print(f'{key_counts_gender[1]}:{counts_gender[1]}')
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print('The earlist birth:', earliest_birth)
        
        most_recent_birth = df['Birth Year'].max()
        print('The most recent birth:', most_recent_birth)
        
        most_common_birth = df['Birth Year'].value_counts().idxmax()
        print('The most common birth year:', most_common_birth)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    run = 0
    while True:
        raw_datas = input('Do you want to see 5 lines of raw data? Enter yes or no.\n')
        if raw_datas.lower() == 'yes':
            run = run + 1
            print(df.iloc[(run-1)*5:run*5])
        elif raw_datas == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

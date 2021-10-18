import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input('Enter the name of a city listed to view transit data for that city: Chicago, New York City, or Washington: '))
        if city.lower() in CITY_DATA:
            break
        else:
            print('Invalid entry. Please enter one of the cities listed: Chicago, New York City, or Washington.')

    # get user input for month (all, january, february, ... , june)
    valid_months=('january', 'february', 'march', 'april', 'may', 'june', 'all')
    while True:
        month = str(input('\nEnter a month between January and June to view transit data for that month. Leave the space blank and press [Enter] to view all available months: ') or 'all')
        if month.lower() in valid_months:
            break
        else:
            print('Invalid entry. Please enter the name of a month between January and June, or leave the space blank for all available months.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day=('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')
    while True:
        day = str(input('\nEnter a day of the week, Monday through Sunday, to view transit data for that day. Leave the space blank and press [Enter] to view all available days of the week: ') or 'all')
        if day.lower() in valid_day:
            break
        else:
            print('Invalid entry. Please enter a day of the week, or leave the space blank for all available days.')

    print('-'*40)
    return city.lower(), month, day

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

    print('\nLoading data for selected city: ' + city.title() + ', selected month: ' + month.title() + ' and selected day of week: ' + day.title() + '...\n')

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name ## after v0.22 the function is dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months.index(month.lower()) + 1
       df = df[df['month'] == month]

    if day != 'all':
       df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month for the selection >>> ' + str(df['month'].mode()[0]))

    # display the most common day of week
    print('Most common day of the week for the selection >>> ' + str(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Most common start hour for the selection >>> ' + str(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station for the selection >>> ' + df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station for the selection >>> ' + df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Start_End'] = 'from: ' + df['Start Station'] + ' to: ' + df['End Station']
    print('Most frequent combination of start and end station trip for the selection >>> ' + df['Start_End'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time for the selection >>> ' + str(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time for the selection >>> ' + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type stats for the selection >>> \n')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nGender stats for the selection >>> \n')
    print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('\nEarliest year of birth for the selection >>> ' + str(df['Birth Year'].min()))
    print('Most recent year of birth for the selection >>> ' + str(df['Birth Year'].max()))
    print('Most common year of birth for the selection >>> ' + str(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """
    Displays filtered df raw data 5 rows at a time.
    Stops loop if user doesn't answer 'Y' or once end of list is reached.
    """
    start = 0
    end = 0

    print('\nThere are a total of ' + str(df['Start Time'].count()) + ' rows in the data selection.')
    userinput = input('Do you want to see the data? Enter \'y\' for yes or \'n\' for no: \n')

    if userinput.lower() == 'y':
        while True:
            #update start and end index of the data to be shown for each iteration
            start = end
            end = end + 5

            #exit if end of data is reached
            if start > df['Start Time'].count():
                print('\nEnd of data reached.')
                break

            #show 5 rows of data
            print(df[start:end])

            #check if user wants to see the next 5 rows of data
            userinput = input('\nShow more rows of data? Enter y/n: \n')
            if  userinput != 'y':
                print('\nOkay, terminating...\n')
                break
    else:
        print('\nOkay, terminating...\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

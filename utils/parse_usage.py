import sys 
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

        
def parse_xml_to_dataframe(filename):
    """
    This function parses the energy usage XML file from the Duke Energy website and returns a Pandas DataFrame.
    :param xml_file: an XML file containing energy usage data in espi format
    :return: a dataframe containing the energy usage data
    """

    # Parse the XML file
    tree = ET.parse(filename)
    root = tree.getroot()

    data = []
    # Iterate through IntervalReading elements
    for interval_reading in root.findall('.//espi:IntervalReading', namespaces={'espi': 'http://naesb.org/espi'}):
        time_period = interval_reading.find('espi:timePeriod', namespaces={'espi': 'http://naesb.org/espi'})
        start_time_seconds = int(time_period.find('espi:start', namespaces={'espi': 'http://naesb.org/espi'}).text)

        # Convert start time to datetime
        start_datetime = datetime.utcfromtimestamp(start_time_seconds)

        # Extract month, date, and day of the week
        month = start_datetime.month
        date = start_datetime.day
        day_of_week = start_datetime.weekday()  # Monday is 0, Sunday is 6
        hour_of_day = start_datetime.hour
        minute = start_datetime.minute

        value = float(interval_reading.find('espi:value', namespaces={'espi': 'http://naesb.org/espi'}).text)

        data.append({
            'Timestamp': start_datetime,
            'Month': month,
            'Date': date,
            'DayOfWeek': day_of_week,
            'HourOfDay': hour_of_day,
            'Minute': minute,
            'Value': value
        })

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)
    return df


def sum_over_hour(dataframe):
    """
    Sum the values over each hour and add the sum to the last entry for each hour. This will add one entry per hour
    that is the total energy usage for that hour.
    :param dataframe: a pandas dataframe
    :return: a dataframe with an additional column for the sum of the values for each hour (3 NaNs, 1 sum for each hour)
    """
    # Group by month, date, day of the week, and hour of the day
    grouped_df = dataframe.groupby(['Month', 'Date', 'DayOfWeek', 'HourOfDay']).agg({'Value': 'sum'}).reset_index()

    # Merge the grouped sum with the original DataFrame to add the sum to the last entry for each hour
    merged_df = pd.merge(dataframe, grouped_df, on=['Month', 'Date', 'DayOfWeek', 'HourOfDay'], how='left', suffixes=('', '_sum'))

    # Identify the latest entry for each hour
    latest_entry_mask = merged_df['Timestamp'] == merged_df.groupby(['Month', 'Date', 'DayOfWeek', 'HourOfDay'])['Timestamp'].transform('max')

    # Replace sum values for non-latest entries with None
    merged_df.loc[~latest_entry_mask, 'Value_sum'] = None

    return merged_df


def filter_results(self, dataframe, min_value, max_value, filter_column):
    """
    Filter the results of a dataframe by a column value given a min and max value.
    The results are inclusive of the min and max values.
    :param dataframe: a pandas dataframe
    :param min_value: minimum value to filter by in the column
    :param max_value: maximum value to filter by in the column
    :param filter_column: the name of the column to filter by
    :return: a dataframe only including filtered results
    """
    # Filter the dataframe by the min and max values inclusive
    filtered_df = dataframe[dataframe[filter_column] >= min_value]
    filtered_df = filtered_df[filtered_df[filter_column] <= max_value]

    return filtered_df


def add_time_period(dataframe):
    """Add a time period column to the dataframe for easier plotting.
    The time periods are:
    Early Morning: 12am - 4am
    Morning: 4am - 8am
    Late Morning: 8am - 12pm
    Afternoon: 12pm - 4pm
    Evening: 4pm - 8pm
    Night: 8pm - 12am
    :param dataframe: data frame with an HourOfDay column
    :return: dataframe with the additional "TimePeriod" column
    """
    # Create a time period column
    dataframe['TimePeriod'] = dataframe['HourOfDay']\
        .apply(lambda x: 'Early Morning' if 0 <= x < 4 else
                        'Morning' if 4 <= x < 8 else
                        'Late Morning' if 8 <= x < 12 else
                        'Afternoon' if 12 <= x < 16 else
                        'Evening' if 16 <= x < 20 else
                        'Night' if 20 <= x < 24 else None)

    return dataframe


if __name__ == "__main__":
    filename = "../energy_usage.xml"
    df = parse_xml_to_dataframe(filename)
    df.to_csv('test.csv')
    # summed_dataframe.to_csv('energy_usage.csv')


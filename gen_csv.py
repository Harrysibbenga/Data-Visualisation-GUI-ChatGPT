import csv
import random
from datetime import datetime, timedelta

# Set the start and end dates for the data
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)

# Create a list of dates between the start and end dates
date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days)]

# Generate random temperature data for each date
temperature_data = [random.randint(0, 100) for _ in range(len(date_range))]

# Write the data to a CSV file
with open('temperature_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Temperature'])
    for i in range(len(date_range)):
        writer.writerow([date_range[i].strftime('%Y-%m-%d'), temperature_data[i]])

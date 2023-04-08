import re
import pandas as pd


def preprocess(data):
    messages = data.split('\n')

    # Extract the relevant information for each message
    data = {'date': [], 'time': [], 'sender': [], 'message': []}
    for message in messages:
        # Parse the message to extract the date, time, sender, and message content
        # and append them to the corresponding lists in the data dictionary
        match = re.search('(\d{1,2}\/\d{1,2}\/\d{2}),\s(\d{1,2}:\d{2} (?:AM|PM))\s-\s([^:]+): (.+)', message)
        if match:
            date = match.group(1)
            time = match.group(2)
            sender = match.group(3)
            message_content = match.group(4)
            data['date'].append(date)
            data['time'].append(time)
            data['sender'].append(sender)
            data['message'].append(message_content)

    # Create the dataframe
    df = pd.DataFrame(data)

    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Create separate columns for day, month, and year
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    # df['date'] = df['date'].dt.date

    return df
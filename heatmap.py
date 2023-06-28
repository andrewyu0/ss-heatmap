import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

def generate_heatmap(start_date=None, end_date=None, directory="."):
    if start_date is None:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    files = os.listdir(directory)
    files = [f for f in files if f.startswith('Screenshot')]
    date_time_list = []
    for file in files:
        match = re.search(r"(\d{4}-\d{2}-\d{2} at \d{2}.\d{2}.\d{2} (AM|PM))", file)
        if match:
            date_time_str = match.group(1)
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d at %I.%M.%S %p')
            if start_date <= date_time <= end_date:
                date_time_list.append((date_time, file))
    
    if not date_time_list:
        print("No screenshots found within the given date range.")
        return

    df = pd.DataFrame(date_time_list, columns=["Datetime", "File"])
    df['Date'] = df['Datetime'].dt.date
    df['Time'] = df['Datetime'].dt.time

    pivot_table = df.pivot_table(index='Time', columns='Date', aggfunc='size', fill_value=0)
    pivot_table.sort_index(ascending=False, inplace=True)

    plt.figure(figsize=(10, 10))
    plt.title('Screenshot Heatmap', fontsize=20)
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Time', fontsize=15)
    plt.pcolor(pivot_table, cmap='hot', edgecolors='white', linewidths=2)
    plt.xticks(np.arange(0.5, len(pivot_table.columns), 1), pivot_table.columns, fontsize=10, rotation=45)
    plt.yticks(np.arange(0.5, len(pivot_table.index), 1), pivot_table.index, fontsize=10)
    plt.colorbar(label='Number of Screenshots')
    plt.tight_layout()
    plt.show()

    for _, row in df.iterrows():
        file = row["File"]
        path = Path(directory) / file
        path = quote(str(path))
        time = row["Time"]
        print(f"<a href={path}>{time}</a>")

generate_heatmap('2023-06-20', '2023-06-27', 'ss')

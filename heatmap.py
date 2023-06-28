from flask import Flask, render_template
import os
import plotly.express as px
import pandas as pd
import re
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def heatmap():
    directory = "./ss"

    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()

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

    df = pd.DataFrame(date_time_list, columns=["Datetime", "File"])
    df['Date'] = df['Datetime'].dt.date
    df['Hour'] = df['Datetime'].dt.hour
    df['File'] = "<a href=\"ss/" + df['File'] + "\">" + df['Hour'].astype(str) + "</a>"

    pivot_table = pd.pivot_table(df, values='File', index='Hour', columns='Date', aggfunc=lambda x: ' '.join(x), fill_value="")
    
    fig = px.imshow(pivot_table, labels=dict(x="Date", y="Hour", color="Frequency"))
    div = fig.to_html(full_html=False)

    return render_template('index.html', plot_div=div)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

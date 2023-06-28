from flask import Flask, render_template, request
import pandas as pd
import os
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__, template_folder=os.path.abspath('templates'))

@app.route('/heatmap')
def heatmap():
    start_date = request.args.get('start_date', default = (datetime.now() - relativedelta(weeks=1)).strftime('%Y-%m-%d'), type = str)
    end_date = request.args.get('end_date', default = datetime.now().strftime('%Y-%m-%d'), type = str)

    path = os.path.abspath('./ss')
    file_info = [(f, *f.split(' ')[1].split(' at '), os.path.join(path, f)) for f in os.listdir(path) if start_date <= f.split(' ')[1] <= end_date]
    ss_df = pd.DataFrame(file_info, columns=["file_path", "date", "time", "ss_link"])
    ss_df['time'] = pd.to_datetime(ss_df['time'], format="%I.%M.%S %p")
    ss_resampled = ss_df.set_index("time").groupby(pd.Grouper(freq='H')).ss_link.apply(list).reset_index()
    ss_resampled['hour'] = ss_resampled.time.dt.hour
    source = ColumnDataSource(ss_resampled)
    hover = HoverTool(tooltips=[("Time", "@time{%F %T}"), ("Screenshot", "@ss_link")], formatters={"@time": "datetime"})
    p = figure(x_axis_type="datetime", plot_width=800, plot_height=350, tools=[hover], title="Screenshots Heatmap")
    p.vbar(x='time', top='hour', source=source, width=0.5)
    script, div = components(p)
    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run(debug=False, port=5001)

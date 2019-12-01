from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import row, column
import pandas as pd

df = pd.read_csv('df.csv', sep=";")

def create_plot():
    p = figure(plot_height=400, plot_width=800)
    p.xaxis.axis_label = "Skoleår"
    p.yaxis.axis_label = "Andel"
    
    #df2 = df.loc[df['kjonn']==kjonnselect.value & df['fullforingsgrad'] == fullfselect.value & df['studieretning_utdanningsprogram']==studretnselect.value]
    source = ColumnDataSource(data=dict(x=[1, 2, 3], y=[3, 2, 3]))
    p.circle(x='x', y='y', source=source)
    return(p)

def update_plot(attr, old, new):
    layout.children[1] = create_plot()

kjonnselect = Select(title="Kjønn", value="kjonn", options=sorted(set(df['kjonn'])))
fullfselect = Select(title="Fullføringsgrad", value="fullf", options=sorted(set(df['fullforingsgrad'])))
studretnselect = Select(title="Studieretning", value="studretn", options=sorted(set(df['studieretning_utdanningsprogram'])))


kjonnselect.on_change('value', update_plot)
fullfselect.on_change('value', update_plot)
studretnselect.on_change('value', update_plot)

controls = column(kjonnselect, fullfselect, studretnselect, width=300)

layout = row(controls, create_plot())
curdoc().add_root(layout)
curdoc().title("first")
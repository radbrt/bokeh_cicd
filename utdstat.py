from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import row, column
import pandas as pd

df = pd.read_csv('df.csv', sep=";")
df['aar'] = df['intervall_ar'].str[0:4].astype(int)

def create_plot():
    p = figure(plot_height=400, plot_width=800)
    p.xaxis.axis_label = "Skoleår"
    p.yaxis.axis_label = "Andel"
    
    df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value)]
    
    print(len(df2))
    source = ColumnDataSource(data=df2)
    p.circle(x='aar', y='elever', source=source)
    return(p)

def update_plot(attr, old, new):
    #df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value)]
    layout.children[1] = create_plot()
    print("plot update triggered")
    print(kjonnselect.value, fullfselect.value, studretnselect.value)

kjonnselect = Select(title="Kjønn", value="Begge kjønn", options=sorted(set(df['kjonn'])))
fullfselect = Select(title="Fullføringsgrad", value="I alt", options=sorted(set(df['fullforingsgrad'])))
studretnselect = Select(title="Studieretning", value="Alle studieretninger/utdanningsprogram", options=sorted(set(df['studieretning_utdanningsprogram'])))


kjonnselect.on_change('value', update_plot)
fullfselect.on_change('value', update_plot)
studretnselect.on_change('value', update_plot)

controls = column(kjonnselect, fullfselect, studretnselect, width=300)

layout = row(controls, create_plot())
curdoc().add_root(layout)
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.plotting import figure
#from bokeh.transform import factor_cmap
from bokeh.layouts import row, column
from bokeh.palettes import colorblind
import pandas as pd

def create_col_column(colors, column):
    u_vals = sorted(set(column))
    d = {k: v for k, v in zip(u_vals, colors)}
    colcols = [d[val] for val in column]
    return(colcols)

TOOLTIPS=[
    ("Antall", "@elever"),
    ("År", "@aar"),
    ("Prosent", "@andel_elever_prosent"),
    ("Foreldrenes utdanning", "@foreldrenes_utdanningsniva")
]

df = pd.read_csv('df.csv', sep=";")
df['aar'] = df['intervall_ar'].str[0:4].astype(int)

def callback(attr, old, new):
    df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value)].groupby('foreldrenes_utdanningsniva')
    p = figure(plot_height=400, plot_width=950, tooltips=TOOLTIPS, toolbar_location=None, name="mainplot")
    p.xaxis.axis_label = "Skoleår"
    p.yaxis.axis_label = "Andel"

    for utdniv, color in zip(set(df['foreldrenes_utdanningsniva']), colorblind['Colorblind'][6] ):
        dfgroup = df2.get_group(utdniv)
        source = ColumnDataSource(data=dfgroup)
        p.line(x="aar", y="elever", color=color, source=source, line_width=3)
    
    layout.children[1] = p


kjonnselect = Select(title="Kjønn", value="Begge kjønn", options=sorted(set(df['kjonn'])))
fullfselect = Select(title="Fullføringsgrad", value="I alt", options=sorted(set(df['fullforingsgrad'])))
studretnselect = Select(title="Studieretning", value="Alle studieretninger/utdanningsprogram", options=sorted(set(df['studieretning_utdanningsprogram'])))

kjonnselect.on_change('value', callback)
fullfselect.on_change('value', callback)
studretnselect.on_change('value', callback)

p = figure(plot_height=400, plot_width=950, tooltips=TOOLTIPS, toolbar_location=None)
p.xaxis.axis_label = "Skoleår"
p.yaxis.axis_label = "Andel"

# Apply list on grouped dataframe returns list of lists - must be run on each variable.
df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value) ].groupby('foreldrenes_utdanningsniva')

controls = column(kjonnselect, fullfselect, studretnselect, width=300)

for utdniv, color in zip(set(df['foreldrenes_utdanningsniva']), colorblind['Colorblind'][6] ):
    dfgroup = df2.get_group(utdniv)
    source = ColumnDataSource(data=dfgroup)
    p.line(x="aar", y="elever", color=color, source=source, line_width=3)


layout = row(controls, p)
curdoc().add_root(layout)
curdoc().title = "Gjennomføring i VGO"


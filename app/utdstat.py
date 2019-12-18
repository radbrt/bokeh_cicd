from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, HoverTool, Select, CheckboxGroup
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

#df = pd.read_csv('/app/df.csv', sep=";")
df = pd.read_csv('app/df.csv', sep=";")
df['aar'] = df['intervall_ar'].str[0:4].astype(int)

def antallprosent(selectbox, active="andel_elever_prosent", inactive="elever"):
    """ Return variable for checkbox option """
    if selectbox.active:
        return(active)
    else:
        return(inactive)

def andelprosent_label(selectbox, active="Prosent av elever", inactive="Antall elever"):
    """ Return y-axis label for checkbox option """
    if selectbox.active:
        return(active)
    else:
        return(inactive)

def callback(attr, old, new):
    df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value)].groupby('foreldrenes_utdanningsniva')
    p = figure(plot_height=400, plot_width=950, tooltips=TOOLTIPS, name="mainplot", sizing_mode='scale_width')
    p.xaxis.axis_label = "Skoleår"
    p.yaxis.axis_label = andelprosent_label(prosent)

    for utdniv, color in zip(set(df['foreldrenes_utdanningsniva']), colorblind['Colorblind'][6] ):
        dfgroup = df2.get_group(utdniv)
        source = ColumnDataSource(data=dfgroup)
        p.line(x="aar", y=antallprosent(prosent), color=color, source=source, line_width=3)
    
    layout.children[0] = p


kjonnselect = Select(title="Kjønn", value="Begge kjønn", options=sorted(set(df['kjonn'])))
fullfselect = Select(title="Fullføringsgrad", value="I alt", options=sorted(set(df['fullforingsgrad'])))
studretnselect = Select(title="Studieretning", value="Alle studieretninger/utdanningsprogram", options=sorted(set(df['studieretning_utdanningsprogram'])))
prosent = CheckboxGroup(labels = ["Vis prosent"], active = [])

kjonnselect.on_change('value', callback)
fullfselect.on_change('value', callback)
studretnselect.on_change('value', callback)
prosent.on_change('active', callback)

p = figure(plot_height=400, plot_width=950, tooltips=TOOLTIPS, sizing_mode='scale_width')
p.xaxis.axis_label = "Skoleår"
p.yaxis.axis_label = andelprosent_label(prosent)

# Apply list on grouped dataframe returns list of lists - must be run on each variable.
df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value) ].groupby('foreldrenes_utdanningsniva')

pctrow = row(prosent, width=950)
controls = row(kjonnselect, fullfselect, studretnselect, width=950)

for utdniv, color in zip(set(df['foreldrenes_utdanningsniva']), colorblind['Colorblind'][6] ):
    dfgroup = df2.get_group(utdniv)
    source = ColumnDataSource(data=dfgroup)
    p.line(x="aar", y=antallprosent(prosent), color=color, source=source, line_width=3)


layout = column(p, pctrow, controls)
curdoc().add_root(layout)
curdoc().title = "Gjennomføring i VGO"


from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import row, column
from bokeh.palettes import colorblind
import pandas as pd


def create_col_column(colors, column):
    u_vals = sorted(set(column))
    d = {k: v for k, v in zip(u_vals, colors)}
    colcols = [d[val] for val in column]
    return(colcols)


df = pd.read_csv('df.csv', sep=";")
df['aar'] = df['intervall_ar'].str[0:4].astype(int)

TOOLTIPS=[
    ("Antall", "@elever"),
    ("År", "@aar"),
    ("Prosent", "@andel_elever_prosent"),
    ("Foreldrenes utdanning", "@foreldrenes_utdanningsniva")
]



def create_plot():
    p = figure(plot_height=400, plot_width=950, tooltips=TOOLTIPS, toolbar_location=None)
    p.xaxis.axis_label = "Skoleår"
    p.yaxis.axis_label = "Andel"
    
    # Apply list on grouped dataframe returns list of lists - must be run on each variable.
    df2 = df.loc[ (df['kjonn']==kjonnselect.value) & (df['fullforingsgrad'] == fullfselect.value) & (df['studieretning_utdanningsprogram']==studretnselect.value) ].groupby('foreldrenes_utdanningsniva')

    for utdniv, color in zip(set(df['foreldrenes_utdanningsniva']), colorblind['Colorblind'][6] ):
        dfgroup = df2.get_group(utdniv)
        source = ColumnDataSource(data=dfgroup)
        p.line(x="aar", y="elever", color=color, source=source, line_width=3)

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
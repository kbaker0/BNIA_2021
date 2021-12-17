from pandas.core.reshape.melt import melt
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import geopandas
import numpy as np
import chart_studio.plotly as py
import chart_studio
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

baseurl = "https://services1.arcgis.com/mVFRs7NF4iFitgbY/ArcGIS/rest/services/"
slug = "/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pgeojson"

vacant_shortname = 'vacant'
nomail_shortname = 'nomail'
rehab_shortname = 'resrehab'
owntax_shortname = 'owntax'
voucher_shortname = 'hcvhouse'
constr_shortname = 'constper'
salepr_shortname = 'salepr'
demper_shortname = 'demper'

# Plotly Chart Studio creds
api_key = 'lM8S3E40y3ZLZxHnRBAL'
username = 'kbaker0'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

# URL for each indicator
vacant_url = baseurl+vacant_shortname+slug
ch_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/ArcGIS/rest/services/Community_Change_Database/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pgeojson'
nomail_url = baseurl+nomail_shortname+slug
rehab_url = baseurl+rehab_shortname+slug
owntax_url = baseurl+owntax_shortname+slug
voucher_url = baseurl+voucher_shortname+slug
constr_url = baseurl+constr_shortname+slug
salepr_url = baseurl+salepr_shortname+slug
demper_url = baseurl+demper_shortname+slug

# Data Frames
df = geopandas.read_file(vacant_url).set_index('CSA2010').drop(axis=1,columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_nomail = geopandas.read_file(nomail_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_change = geopandas.read_file(ch_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_rehab = geopandas.read_file(rehab_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_constr = geopandas.read_file(constr_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_salepr = geopandas.read_file(salepr_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_demper = geopandas.read_file(demper_url).set_index(df.index).drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])

available_keys = df.keys()
nomail_keys = df_nomail.keys()
rehab_keys = df_rehab.keys()
constr_keys = df_constr.keys()
salepr_keys = df_salepr.keys()
demper_keys = df_demper.keys()
change_keys = df_change.keys()

def melt_function(df, available_keys):
    mdf = pd.melt(df, value_vars=[i for i in available_keys], var_name='indicator_year', ignore_index=False)
    return mdf
# print(df_change)
change_df = df_change[['chvacant']]
df_change_nomail = df_change[['chnomail']]
df_change_resrehab = df_change[['chresrehab']]
df_change_constr = df_change[['chconstper']]
df_change_salepr = df_change[['chsalepr']]
df_change_demper = df_change[['chdemper']]

thisone = change_df.sort_values('chvacant', ascending=False)

ch_group = pd.cut(change_df['chvacant'], bins=[-40, -1, 1, 10], labels=['decrease', 'little_change', 'increase'])
change_df['group'] = ch_group.values

chnomail_group = pd.cut(df_change_nomail['chnomail'], bins=[-100, -1, 1, 100], labels=['decrease', 'little_change', 'increase'])
df_change_nomail['group'] = chnomail_group.values

chresrehab_group = pd.cut(df_change_resrehab['chresrehab'], bins=[0, 1.5, 3, 6], labels=['decrease', 'no_change', 'increase'])
df_change_resrehab['group'] = chresrehab_group.values

chconstr_group = pd.cut(df_change_constr['chconstper'], bins=[-100, -1, 1, 100], labels=['decrease', 'little_change', 'increase'])
df_change_constr['group'] =chconstr_group.values

chsalepr_group = pd.cut(df_change_salepr['chsalepr'], bins=[-100, -1, 1, 100], labels=['decrease', 'little_change', 'increase'])
df_change_salepr['group'] = chsalepr_group.values

chdemper_group = pd.cut(df_change_demper['chdemper'], bins=[-100, -1, 1, 100], labels=['decrease', 'little_change', 'increase'])
df_change_demper['group'] = chdemper_group.values

my_df = melt_function(df, df.keys())
df_nomail = melt_function(df_nomail, df_nomail.keys())
df_resrehab = melt_function(df_rehab, df_rehab.keys())
df_const= melt_function(df_constr, df_constr.keys())
df_salepri = melt_function(df_salepr, df_salepr.keys())
df_demo = melt_function(df_demper, df_demper.keys())

def trend_column(df, mdf):
    mdf['trend'] = mdf.rename(index=df.set_index(df.index)['group']).index
    return mdf
    
trend_column(change_df, my_df)
trend_column(df_change_nomail, df_nomail)
# trend_column(df_change_resrehab, df_resrehab)
# trend_column(df_change_demper, df_demo)
# trend_column(df_change_salepr, df_salepri)
# trend_column(df_change_constr, df_const)

def sorted_change_column(df, mdf, column):
    mdf['change'] = mdf.rename(index=df.set_index(df.index)[column]).index
    sortem = mdf.sort_values('change', ascending=False)
    return sortem
nomail_sorted_column = sorted_change_column(df_change_nomail, df_nomail, 'chnomail')
vacant_sorted_column = sorted_change_column(change_df, my_df, 'chvacant')

# print(vacant_sorted_column)


def map_group(mdf):
    group = mdf.groupby('trend')
    print(group.get_group('decrease').sort_values('change', ascending=True),'---------------------------')
    maps = {'Decrease':[i for i in group.get_group('decrease').sort_values('change', ascending=True).index],
        'Very Little Change':[i for i in group.get_group('little_change').index],
        'Increase':[i for i in group.get_group('increase').index]}
    return maps

vacant_map = map_group(my_df)
nomail_map = map_group(df_nomail)
# print(vacant_map)
# resrehab_map = map_group(df_resrehab)
# const_map = map_group(df_const)
# salepri_map = map_group(df_salepri)
# demo_map = map_group(df_demo)

my_df['indicator_year'] = my_df['indicator_year'].map(
    {'vacant10':'2010', 'vacant11':'2011', 'vacant12':'2012', 
    'vacant13':'2013', 'vacant14':'2014', 'vacant15':'2015', 
    'vacant16':'2016', 'vacant17':'2017', 'vacant18':'2018', 
    'vacant19':'2019', 'vacant20':'2020'})

df_nomail['indicator_year'] = df_nomail['indicator_year'].map(
    {'nomail10':'2010', 'nomail11':'2011', 'nomail12':'2012', 
    'nomail13':'2013', 'nomail14':'2014', 'nomail15':'2015', 
    'nomail16':'2016', 'nomail17':'2017', 'nomail18':'2018', 
    'nomail19':'2019', 'nomail20':'2020'})



# print(vacant_sorted_column)
# print(nomail_sorted_column)

# def line_plot(mdf, title, map, order):
#     fig = px.line(mdf, title=title, x=mdf['indicator_year'], y = mdf['value'], labels={ 'indicator_year': 'Year'}, 
#     color = mdf.index, facet_col='trend', category_orders={'CSA2010': [i for i in order.index.unique()], 'trend': ['decrease', 'no_change', 'increase']}, 
#     template='plotly_white') 

def line_plot(mdf, title, map, order):
    fig = px.line(mdf, title=title, x=mdf['indicator_year'], y = mdf['value'], labels={ 'indicator_year': 'Year', 'value':'Percent'}, 
    color = mdf.index, facet_col='trend', category_orders={'CSA2010': [i for i in order.index], 'trend': ['decrease', 'little_change', 'increase']}, 
    template='plotly_white') 
    print([i for i in order.index])
    # groups and trace visibilities
    group = []
    vis = []
    visList = []
    for m in map.keys():
        for j in mdf.index:
            if j in map[m]:
                vis.append(True)
            else:
                vis.append(False)
        group.append(m)
        visList.append(vis)
        vis = []

    # buttons for each group
    buttons = []
    for i, g in enumerate(group):
        button =  dict(label=g,
                    method = 'restyle',
                    args = ['visible',visList[i]])
        buttons.append(button)

    buttons = [{'label': 'All',
                    'method': 'restyle',
                    'args': ['visible', [True]]}] + buttons                   

    # update layout with buttons                       
    fig.update_layout(
        updatemenus=[
            dict(
            type="dropdown",
            direction="down",
            buttons = buttons)
        ],
    )
   
    fig.show()
    return fig

line_plot(my_df, "Percent of Residential Properties that are Vacant and Abandoned, by CSA", vacant_map, vacant_sorted_column)
# line_plot(df_nomail, "Percent of Residential Properties that Do Not Receive Mail, by CSA", nomail_map, nomail_sorted_column)
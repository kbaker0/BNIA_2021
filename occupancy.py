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

# Shortnames for API call
vacant_shortname = 'vacant'
rehab_shortname = 'resrehab'
nomail_shortname = 'nomail'
owntax_shortname = 'owntax'
voucher_shortname = 'hcvhouse'
constr_shortname = 'constper'
salepr_shortname = 'salepr'
demper_shortname = 'demper'

# API URL
baseurl = "https://services1.arcgis.com/mVFRs7NF4iFitgbY/ArcGIS/rest/services/"
slug = "/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pgeojson"

# Plotly Chart Studio creds
api_key = 'lM8S3E40y3ZLZxHnRBAL'
username = 'kbaker0'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

# URL for each indicator
vacant_url = baseurl+vacant_shortname+slug
nomail_url = baseurl+nomail_shortname+slug
rehab_url = baseurl+rehab_shortname+slug
owntax_url = baseurl+owntax_shortname+slug
voucher_url = baseurl+voucher_shortname+slug
constr_url = baseurl+constr_shortname+slug
salepr_url = baseurl+salepr_shortname+slug
demper_url = baseurl+demper_shortname+slug
ch_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/ArcGIS/rest/services/Community_Change_Database/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pgeojson'

# Parsing the data into data frames
df = geopandas.read_file(vacant_url).set_index('CSA2010').drop(axis=1,columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_nomail = geopandas.read_file(nomail_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_rehab = geopandas.read_file(rehab_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_constr = geopandas.read_file(constr_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_salepr = geopandas.read_file(salepr_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_demper = geopandas.read_file(demper_url).set_index(df.index).drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_change = geopandas.read_file(ch_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])

# Available keys of each data frame
available_keys = df.keys()
nomail_keys = df_nomail.keys()
rehab_keys = df_rehab.keys()
constr_keys = df_constr.keys()
salepr_keys = df_salepr.keys()
demper_keys = df_demper.keys()
change_keys = df_change.keys()

# Top x in specified incidator
# def sort_data(data, indicator, ascending):
#     my_sorted = data.sort_values(indicator, ascending=ascending)
#     return my_sorted

# vacant_sorted = sort_data(df, 'vacant20', False)
# nomail_sorted = sort_data(df_nomail, 'nomail20', False)
# salepr_sorted = sort_data(df_salepr, 'salepr19', True)
# const_sorted = sort_data(df_constr, 'constper20', True)
# rehab_sorted = sort_data(df_rehab, 'resrehab20', True)
# demper_sorted = sort_data(df_demper, 'demper20', False)

# Creates x,y columns for line graph view
def melt_function(df, available_keys):
    mdf = pd.melt(df, value_vars=[i for i in available_keys], var_name='indicator_year', ignore_index=False)
    return mdf
change_df = df_change[['chvacant']]
df_change_nomail = df_change[['chnomail']]

# Find difference between each column in order
def diff_function(df):
    ndf= df.diff(axis=1)
    return ndf

vacant_diff = diff_function(df)
nomail_diff = diff_function(df_nomail)
constr_diff = diff_function(df_constr)
rehab_diff = diff_function(df_rehab)
salepr_diff = diff_function(df_salepr)
dempter_diff = diff_function(df_demper)

# Find the mean of percent diff across all years
def find_mean(df):
    df_mean = df.agg("mean", axis="columns")
    df['mean'] = df_mean.values
    return df

vacant_mean = find_mean(vacant_diff)
constr_mean = find_mean(constr_diff)
nomail_mean = find_mean(nomail_diff)
rehab_mean = find_mean(rehab_diff)
salepr_mean = find_mean(salepr_diff)
demper_mean = find_mean(dempter_diff)

# Take the keys and group by ascending/no change/descending
# grouped = pd.qcut(vacant_mean['mean'], 3, labels=['decrease', 'no_change', 'increase'])
# df['group'] = grouped.values
# print(df)

def group_function(df):
    grouped = pd.qcut(df['mean'], 3, labels=['decrease', 'no_change', 'increase'])
    df['group'] = grouped.values
    return df
dfgrouped_vacant = group_function(vacant_mean)
dfgrouped_nomail = group_function(nomail_mean)
dfgrouped_constr = group_function(constr_mean)
dfgrouped_rehab = group_function(rehab_mean)
dfgrouped_salepr = group_function(salepr_mean)
dfgrouped_demper = group_function(demper_mean)

# print(pd.cut(df_change['chvacant'], bins=[-40, -1, 1, 10], labels=['decrease', 'no_change', 'increase'], retbins=True))
ch_group = pd.cut(change_df['chvacant'], bins=[-40, -1, 1, 10], labels=['decrease', 'no_change', 'increase'])
change_df['group'] = ch_group.values

chnomail_group = pd.cut(df_change_nomail['chnomail'], bins=[-100, -1, 1, 100], labels=['decrease', 'no_change', 'increase'])
df_change_nomail['group'] = chnomail_group.values

# vacant_most = vacant_mean.nlargest(5, 'mean')
# nomail_most = nomail_mean.nlargest(5, 'mean')

my_df = melt_function(df, available_keys)
df_nomail = melt_function(df_nomail, nomail_keys)
df_resrehab = melt_function(df_rehab, rehab_keys)
df_const= melt_function(df_constr, constr_keys)
df_salepri = melt_function(df_salepr, salepr_keys)
df_demo = melt_function(df_demper, demper_keys)
# df_vacant_most = melt_function(vacant_most, vacant_most.keys())
# df_nomail_most = melt_function(nomail_most, nomail_most.keys())
# vacant_mean=melt_function(vacant_mean, vacant_mean.keys())

def trend_column(df, mdf):
    mdf['trend'] = mdf.rename(index=df.set_index(df.index)['group']).index
    return mdf
# trend_column(dfgrouped_vacant, my_df)
trend_column(dfgrouped_nomail, df_nomail)
trend_column(dfgrouped_rehab, df_resrehab)
trend_column(dfgrouped_constr, df_const)
trend_column(dfgrouped_demper, df_demo)
trend_column(dfgrouped_salepr, df_salepri)
trend_column(change_df, my_df)
trend_column(df_change_nomail, df_nomail)


# def mean_column(df, mdf):
#     mdf['mean'] = mdf.rename(index=df.set_index(df.index)['mean']).index
#     sortem = mdf.sort_values('mean', ascending=False)
#     return sortem
def sorted_change_column(df, mdf, column):
    mdf['change'] = mdf.rename(index=df.set_index(df.index)[column]).index
    sortem = mdf.sort_values('change', ascending=False)
    return sortem
nomail_sorted_column = sorted_change_column(df_change_nomail, df_nomail, 'chnomail')
vacant_sorted_column = sorted_change_column(change_df, my_df, 'chvacant')
# print(nomail_sorted_column)
# vacant_mean_column = mean_column(vacant_mean, my_df)
# nomail_mean_column = mean_column(nomail_mean, df_nomail)
# rehab_mean_column = mean_column(rehab_mean, df_resrehab)
# constr_mean_column = mean_column(constr_mean, df_const)
# salepr_mean_column = mean_column(salepr_mean, df_salepr)
# demper_mean_column = mean_column(demper_mean, df_demo)

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

def line_plot(df, title, order):
    fig = px.line(df, title=title, x=df['indicator_year'], y='value', labels={ 'indicator_year': 'Year'}, color=df.index, facet_col='trend', category_orders={'CSA2010': [i for i in order.index], 'trend': ['decrease', 'no_change', 'increase']}, template='plotly_white')
    fig.show()
    return fig

def bar_plot(df, title, color_scale_order):
    ndf = df.sort_values('mean', ascending=False)
    fig = px.bar(ndf, title=title, x=ndf.index, y='mean', color='mean', color_continuous_scale=color_scale_order, width= 1250, height=800)
    fig.show()
    return fig

# fig = px.line(my_df, title='Percent of Residential Properties that are Vacant and Abandoned by CSA, 2010-2020', x=my_df['indicator_year'], y='value', labels={ 'indicator_year': 'Year'}, color=my_df.index, facet_col='trend', category_orders={'trend': ['decrease', 'no_change', 'increase']}, )
# fig.show()

# fig2 = px.line(df_nomail, title='Percent of Residential Properties that Do Not Receive Mail by CSA, 2010-2020', x=df_nomail['indicator_year'], y='value', labels={ 'indicator_year': 'Year'}, color=df_nomail.index, facet_col='trend', category_orders={'trend': ['decrease', 'no_change', 'increase']}, )
# fig2.show()

# line_plot(df_nomail, 'Percent of Residential Properties that Do Not Receive Mail by CSA, 2010-2020', nomail_sorted_column)
# line_plot(my_df, 'Percent of Residential Properties that are Vacant and Abandoned by CSA, 2010-2020', vacant_sorted_column)

# Make a table
# df.reset_index(inplace=True)
# df.rename(columns={'index':''}, inplace = True)
# new_df = df.drop(columns=['group'])
# fig = go.Figure(data=[go.Table(
#     header=dict(values=list(new_df.columns),
#                 fill_color='paleturquoise',
#                 align='left'),
#     cells=dict(values=[new_df[col] for col in new_df.columns],
#                fill_color='lavender',
#                align='left')),
               
# ])
# fig.show()

# vacant_most.reset_index(inplace=True)
# vacant_most.rename(columns={'index':''}, inplace = True)
# # new_df = df.drop(columns=['group'])
# fig = go.Figure(data=[go.Table(
#     header=dict(values=list(vacant_most.columns),
#                 fill_color='paleturquoise',
#                 align='left'),
#     cells=dict(values=[vacant_most[col] for col in vacant_most.columns],
#                fill_color='lavender',
#                align='left')),
               
# ])
# fig.show()
# nomail_most.reset_index(inplace=True)
# nomail_most.rename(columns={'index':''}, inplace = True)
# # new_df = df.drop(columns=['group'])
# fig = go.Figure(data=[go.Table(
#     header=dict(values=list(nomail_most.columns),
#                 fill_color='paleturquoise',
#                 align='left'),
#     cells=dict(values=[nomail_most[col] for col in nomail_most.columns],
#                fill_color='lavender',
#                align='left')),
               
# ])
# fig.show()
# fig = go.Figure()

# Add to Chart Studio
fig = line_plot(my_df, 'Percent of Residential Properties that are Vacant and Abandoned by CSA, 2010-2020', vacant_sorted_column)
py.plot(fig, filename ='Vacant_and_Abandoned', auto_open=True)

# fig = bar_plot(vacant_mean, 'vacant mean', 'balance')
# py.plot(fig, validate=True, filename='vacant_mean_test', auto_open=True)
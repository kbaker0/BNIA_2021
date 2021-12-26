from ssl import DER_cert_to_PEM_cert
from _plotly_utils.colors import colorscale_to_colors, colorscale_to_scale, convert_colorscale_to_rgb, get_colorscale, n_colors, named_colorscales, sample_colorscale
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
import itertools

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
lifexp_shortname = 'lifexp'

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
lifexp_url = baseurl+lifexp_shortname+slug
nointernet_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/ArcGIS/rest/services/Nohhint' + slug
libcard_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Libcard' + slug
lead_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Ebll' + slug
infmort_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Mort1_' + slug
teenbir_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Teenbir' + slug
pcrime_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Prop' + slug
vcrime_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Viol' + slug
dirt_url = 'https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Dirtyst' + slug

# Data Frames
df = geopandas.read_file(vacant_url).set_index('CSA2010').drop(axis=1,columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_nomail = geopandas.read_file(nomail_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_change = geopandas.read_file(ch_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_rehab = geopandas.read_file(rehab_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_constr = geopandas.read_file(constr_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_salepr = geopandas.read_file(salepr_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_demper = geopandas.read_file(demper_url).set_index(df.index).drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_lifexp = geopandas.read_file(lifexp_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_internet = geopandas.read_file(nointernet_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_libcard = geopandas.read_file(libcard_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_lead = geopandas.read_file(lead_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_infmort = geopandas.read_file(infmort_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_teenbir = geopandas.read_file(teenbir_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_pcrime = geopandas.read_file(pcrime_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_vcrime = geopandas.read_file(vcrime_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])
df_dirt = geopandas.read_file(dirt_url).set_index('CSA2010').drop(columns=['OBJECTID', 'Shape__Area', 'Shape__Length', 'geometry'])


# fig = px.scatter(df.melt(id_vars="beep"), x='beep', y='value', color='variable')
# fig.show()
# #
available_keys = df.keys()
nomail_keys = df_nomail.keys()
rehab_keys = df_rehab.keys()
constr_keys = df_constr.keys()
salepr_keys = df_salepr.keys()
demper_keys = df_demper.keys()
change_keys = df_change.keys()
lifexp_keys = df_lifexp.keys()

def melt_function(df, availablekeys):
    mdf = pd.melt(df, value_vars=[i for i in availablekeys], var_name='indicator_year', ignore_index=False)
    return mdf
# print(df_change.keys())
change_df = df_change[['chvacant']]
df_change_nomail = df_change[['chnomail']]
df_change_resrehab = df_change[['chresrehab']]
df_change_constr = df_change[['chconstper']]
df_change_salepr = df_change[['chsalepr']]
df_change_demper = df_change[['chdemper']]
df_change_libcard = df_change[['chlibcard']]
# df_change_lifexp = df_change[['chlifexp']]

# Creating columns in the change dataframes that are assigned the indicator change values respectively
ch_group = pd.cut(change_df['chvacant'], bins=[-40, -1, 1, 40], labels=['Decrease', 'Little Change', 'Increase'])
change_df['group'] = ch_group.values

chnomail_group = pd.cut(df_change_nomail['chnomail'], bins=[-100, -1, 1, 100], labels=['Decrease', 'Little Change', 'Increase'])
df_change_nomail['group'] = chnomail_group.values

chresrehab_group = pd.cut(df_change_resrehab['chresrehab'], bins=[0, 1.5, 3, 100], labels=['Decrease', 'Little Change', 'Increase'])
df_change_resrehab['group'] = chresrehab_group.values

chconstr_group = pd.cut(df_change_constr['chconstper'], bins=[0, 1, 50, 100], labels=['Decrease', 'Little Change', 'Increase'])
df_change_constr['group'] =chconstr_group.values

chsalepr_group = pd.cut(df_change_salepr['chsalepr'], bins=[-20000, -1000, 1000, 20000], labels=['Decrease', 'Little Change', 'Increase'])
df_change_salepr['group'] = chsalepr_group.values

chdemper_group = pd.cut(df_change_demper['chdemper'], bins=[0, 1, 50, 100], labels=['Decrease', 'Little Change', 'Increase'])
df_change_demper['group'] = chdemper_group.values

chlibcard_group = pd.cut(df_change_libcard['chlibcard'], bins=[-100, 1, 20, 100], labels=['Decrease', 'Little Change', 'Increase'])
df_change_libcard['group'] = chlibcard_group.values


my_df = melt_function(df, df.keys())
df_nomail = melt_function(df_nomail, df_nomail.keys())
df_resrehab = melt_function(df_rehab, df_rehab.keys())
df_const= melt_function(df_constr, df_constr.keys())
df_salepri = melt_function(df_salepr, df_salepr.keys())
df_demo = melt_function(df_demper, df_demper.keys())
df_lifexp = melt_function(df_lifexp, df_lifexp.keys())
df_libcard = melt_function(df_libcard, df_libcard.keys())

# def trend_column(df, mdf):
#     mdf['trend'] = mdf.rename(index=df.set_index(df.index)['group']).index
#     return mdf
    
# trend_column(change_df, my_df)
# trend_column(df_change_nomail, df_nomail)
# # trend_column(df_change_lifexp, df_lifexp)
# trend_column(df_change_resrehab, df_resrehab)
# trend_column(df_change_demper, df_demo)
# trend_column(df_change_salepr, df_salepri)
# trend_column(df_change_constr, df_const)

def sorted_change_column(df, mdf, column):
    mdf['trend'] = mdf.rename(index=df.set_index(df.index)['group']).index
    mdf['change'] = mdf.rename(index=df.set_index(df.index)[column]).index
    mdf = mdf.sort_values('change', ascending=True)
    # return sortem
    return mdf
sorted_change_column(df_change_nomail, df_nomail, 'chnomail')
sorted_change_column(change_df, my_df, 'chvacant')
sorted_change_column(df_change_resrehab, df_resrehab, 'chresrehab')
sorted_change_column(df_change_demper, df_demo,'chdemper')
sorted_change_column(df_change_salepr, df_salepri,'chsalepr')
sorted_change_column(df_change_constr, df_const, 'chconstper')
sorted_change_column(df_change_libcard, df_libcard, 'chlibcard')

my_df = my_df.sort_values('change', ascending=True)
df_nomail = df_nomail.sort_values('change', ascending=True)
df_resrehab = df_resrehab.sort_values('change', ascending=True)
df_demo = df_demo.sort_values('change', ascending=True)
df_const = df_const.sort_values('change', ascending=True)
df_salepri = df_salepri.sort_values('change', ascending=True)
df_libcard = df_libcard.sort_values('change', ascending=False)

# Mapping out better labeling for each year associated with each indicator name
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

df_resrehab['indicator_year'] = df_resrehab['indicator_year'].map(
    {'resrehab10':'2010', 'resrehab11':'2011', 'resrehab12':'2012', 
    'resrehab13':'2013', 'resrehab14':'2014', 'resrehab15':'2015', 
    'resrehab16':'2016', 'resrehab17':'2017', 'resrehab18':'2018', 
    'resrehab19':'2019', 'resrehab20':'2020'})

df_salepri['indicator_year'] = df_salepri['indicator_year'].map(
    {'salepr10':'2010', 'salepr11':'2011', 'salepr12':'2012', 
    'salepr13':'2013', 'salepr14':'2014', 'salepr15':'2015', 
    'salepr16':'2016', 'salepr17':'2017', 'salepr18':'2018', 
    'salepr19':'2019', 'salepr20':'2020'})

df_libcard['indicator_year'] = df_libcard['indicator_year'].map(
    {'libcard11':'2011', 'libcard12':'2012', 
    'libcard13':'2013', 'libcard14':'2014', 'libcard15':'2015', 
    'libcard16':'2016', 'libcard17':'2017', 'libcard18':'2018', 
    'libcard19':'2019'})

# def line_plot(mdf, title, map, order):
#     fig = px.line(mdf, title=title, x=mdf['indicator_year'], y = mdf['value'], labels={ 'indicator_year': 'Year'}, 
#     color = mdf.index, facet_col='trend', category_orders={'CSA2010': [i for i in order.index.unique()], 'trend': ['decrease', 'no_change', 'Increase']}, 
#     template='plotly_white') 

# def line_plot(mdf, title, map, order):
#     fig = px.line(mdf, title=title, x=mdf['indicator_year'], y = mdf['value'], labels={ 'indicator_year': 'Year', 'value':'Percent'}, 
#     color = mdf.index, facet_col='trend', category_orders={'CSA2010': [i for i in order.index.unique()], 'trend': ['decrease', 'Little Change', 'Increase']}, 
#     template='plotly_white') 

# print(n_colors(lowcolor='rgb(23, 28, 66)', highcolor='rgb(172, 43, 36)', n_colors=4, colortype="rgb"))
# for i in colorscale

# Function to create a graph
# def line_plot(mdf, title, map):

def line_plot(mdf, title):
    def map_group(mdf):
        group = mdf.groupby('trend')
        # print(group.get_group('decrease').sort_values('change', ascending=True),'---------------------------')
        maps = {'Decrease':[i for i in group.get_group('Decrease').index.unique()],
                'Very Little Change':[i for i in group.get_group('Little Change').index.unique()],
                'Increase':[i for i in group.get_group('Increase').index.unique()]}
        # maps = {'Decrease':[i for i in group.get_group('Decrease').sort_values('change', ascending=True, ).index],
        #     'Very Little Change':[i for i in group.get_group('Little Change').index],
        #     'Increase':[i for i in group.get_group('Increase').index]}
        return maps

    map = map_group(mdf)

    # decrease = [i for i in map["Decrease"]]
    # stay_same = [i for i in map["Very Little Change"]]
    # increase = [i for i in map["Increase"]]
    
    # group_color = {i: get_colorscale('Blues') for i in map["Decrease"]}
    # group_color = {i: 'mediumblue' for i in map["Decrease"]}
    # group_color_yellow= {i: 'dimgrey' for i in map["Very Little Change"]}
    # group_color_red = {i: 'red' for i in map["Increase"]}
    # group_color.update(group_color_yellow)
    # group_color.update(group_color_red)

    color_ = sample_colorscale(get_colorscale('blues_r'), samplepoints=len(map["Decrease"]), low=0.0, high=.75)
    color_medium = sample_colorscale(get_colorscale('greys'), samplepoints=len(map["Very Little Change"]), low=.25, high=.85)
    color_high = sample_colorscale(get_colorscale('reds'), samplepoints=len(map["Increase"]), low=.5)
    count=0
    color_list = {}
    for j in map['Decrease']:
        d_color =  {j : color_[count]}
        color_list.update(d_color)
        count+=1
    count=0
    for j in map['Very Little Change']:
        d_color =  {j : color_medium[count]}
        color_list.update(d_color)
        count+=1
    count=0
    for j in map['Increase']:
        d_color =  {j : color_high[count]}
        color_list.update(d_color)
        count+=1
    print(color_list)
    
    # print(group_color)
    print(sample_colorscale(get_colorscale('Blues'), samplepoints=len(map["Decrease"])))
    # for i in decrease:
        # colors_= n_colors(lowcolor='rgb(23, 28, 66)', highcolor='rgb(172, 43, 36)', n_colors=, colortype="rgb")
        # colors_ = get_colorscale('Blues')
        # print(colors_)
        # group_color = {i: color}


    # colors_= n_colors(lowcolor='rgb(23, 28, 66)', highcolor='rgb(172, 43, 36)', n_colors=group_color, colortype="rgb")
    # Setting up the graph
    # fig = px.line(mdf, title=title, x=mdf['indicator_year'], y = mdf['value'], labels={ 'indicator_year': 'Year', 'value':'Total per Year'}, 
    #     color = mdf.index, color_discrete_sequence=px.colors.sequential.Plotly3, facet_col='trend', category_orders={'trend': ['Decrease', 'Little Change', 'Increase']}, height=600, width=1250, 
    #     template='plotly_white') 
    fig = px.line(mdf, title=title, x=mdf['indicator_year'], y = mdf['value'], labels={ 'indicator_year': 'Year', 'value':'Percent'}, 
        color = mdf.index, color_discrete_map=color_list, facet_col='trend', category_orders={'trend': ['Decrease', 'Little Change', 'Increase']}, height=600, width=1250, 
        template='plotly_white') 
    group = []
    vis = []
    visList = []
    for m in map.keys():
        for j in mdf.index.unique():
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
        button =  dict( label=g,
                        method = 'restyle',
                        args = ['visible',visList[i]])
        buttons.append(button)
    buttons = [{'label': 'All',
                'method': 'restyle',
                'args': ['visible', [True]]}] + buttons                   

    # buttons = []
    # button = dict(label="No mail",
    #                   method = 'restyle',
    #                   args = [['x',df_nomail['indicator_year'], ['y', df_nomail['value']]]])
    # buttons.append(button)
    # buttons = [{'label': 'Vacant',
    #             'method': 'restyle',
    #             'args': ['data_frame', my_df]}] + buttons
    # update layout with buttons                       
    fig.update_layout(
        updatemenus=[
            dict(
            type="dropdown",
            direction="down",
            buttons = buttons)
        ]
    )
    def stackcount():
        counter = itertools.count(start=1)
        # print("counter: ", counter)
        def update_trace_stack(t):
            t.update(stackgroup=next(counter))
            # print("counter: ", counter)
        return update_trace_stack
    # print(stackcount())
    
    fig.for_each_trace(stackcount())
    fig.update_traces(fill='none')
    fig.update_xaxes(type='linear')

    # fig.show()
    return fig
# line_plot(my_df, "Percent of Residential Properties that are Vacant and Abandoned, by CSA")
# line_plot(my_df, "Percent of Residential Properties that are Vacant and Abandoned, by CSA", vacant_map)
# line_plot(my_df, "Percent of Residential Properties that are Vacant and Abandoned, by CSA", vacant_map, vacant_sorted_column)

# line_plot(df_nomail, "Percent of Residential Properties that Do Not Receive Mail, by CSA")
# line_plot(df_demo, "Percent of Residential Properties that Do Not Receive Mail, by CSA")
# line_plot(df_salepri, "sale price")
# line_plot(df_const, "construction")
# line_plot(df_resrehab, "residential rehab")
# line_plot(df_libcard, "libcard")
line_plot(my_df, "Vacant, by CSA")
# line_plot(df_lifexp, "Life expectancy", lifexp_map, lifexp_sorted_column)

# fig = line_plot(my_df, "Percent of Residential Properties that are Vacant and Abandoned, by CSA", vacant_map)
# py.plot(fig, filename ='beep', auto_open=True)
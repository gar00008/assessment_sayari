from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import math
import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network

def horiz_bar_chart(data,index):
    
    fig = go.Figure()

    data.set_index(index,inplace=True)
    data.sort_values(by=['total rating'],ascending=True,inplace=True)
    data.drop(columns=['total rating'],inplace=True)
    
    #print(data)
    
    for index,item in data.T.iterrows():      
        
        fig.add_trace(go.Bar(
            y=list(item.keys()),
            x=list(item),
            name=str(index),
            orientation='h',
            marker=dict(
                #color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(255,255,255,1)', width=1)
            )
        ))
    

        fig.update_layout(barmode='stack',showlegend=True)

    return fig

def supply_chain(nodes,links):
    
  nx_graph = nx.Graph()

  for index,item in nodes.iterrows:
        nx_graph.add_node(item.node, size=120, label=item.name,title='<url>', level=1, shape='box', group=1, physics=False)
        


  nx_graph.add_node(1, size=120, label='Product 1',title='<url>', level=1, shape='box', group=1, physics=False)
  nx_graph.add_node(2, size=120, label='Company B',title='<url>', level=2, shape='box', group=2, physics=False)
  nx_graph.add_node(3, size=120, label='Company C',title='<url>', level=2, shape='box', group=2, physics=False)
  nx_graph.add_node(4, size=120, label='Company D',title='<url>', level=3, shape='box', group=2, physics=False)
  nx_graph.add_node(5, size=120, label='Company E',title='<url>', level=4, shape='box', group=2, physics=False)
  nx_graph.add_node(6, size=120, label='Company F',title='<url>', level=3, shape='box', group=2, physics=False)
  nx_graph.add_node(7, size=120, label='Company G',title='<url>', level=4, shape='box', group=2, physics=False)
  nx_graph.add_node(8, size=120, label='Company H',title='<url>', level=4, shape='box', group=2, physics=False)
        
  nx_graph.add_edge(1, 2, length = 200, weight=5,label='Part 1', physics=True,arrows='to')
  nx_graph.add_edge(1, 3, length = 200, weight=5,label='Part 2', physics=True,arrows='to')
  nx_graph.add_edge(2, 4, length = 200, weight=5,label='Part 3', physics=True,arrows='to')
  nx_graph.add_edge(2, 6, length = 200, weight=5,label='Part 4', physics=True,arrows='to')
  nx_graph.add_edge(4, 5, length = 200, weight=5,label='Part 5', physics=True,arrows='to')
  nx_graph.add_edge(6, 7, length = 200, weight=5,label='Part 6', physics=True,arrows='to')
  nx_graph.add_edge(6, 8, length = 200, weight=5,label='Part 8', physics=True,arrows='to')

  nt = Network("600px", "100%",notebook=False, bgcolor="black")

  nt.set_options("""
    var options = {
      "layout": {
        "hierarchical": {
            "levelSeparation": 200,
            "nodeSpacing": 200,
            "treeSpacing": 300,
            "direction": "LR",
            "sortMethod": "directed",
            "parentCentralization":true,
            "shakeTowards": "roots"
            }
        }
    }
    """)

  nt.from_nx(nx_graph)
  nt.save_graph('vc.html')


def risk_reg_sum_fig():
    
    fig =go.Figure(go.Sunburst(
        labels=["Substance", "REACH", "RoHS", "Prop65", "SCIP","Party", "US CBP Watchlist", "Product", "FDA Recalls", "Jurisdiction","DRC"],
        parents=["", "Substance", "Substance", "Substance", "Substance","", "Party", "", "Product", "","Jurisdiction" ],
        values=[10, 7, 5, 10, 2, 2, 6, 6, 4, 4,4],
    ))
    
    # Update layout for tight margin
    # See https://plotly.com/python/creating-and-updating-figures/
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    
    return fig


def risk_rep_sum_fig():
    
    fig =go.Figure(go.Sunburst(
        labels=["Corp Responsibility", "Brand","Org","Product","Environmental", "Social", "Governance", "LCA", "SLA", "Liability"],
        parents=["", "", "Corp Responsibility", "Corp Responsibility","Org","Org", "Org", "Product", "Brand", "Brand"],
        values=[10, 14, 12, 10, 2, 6, 6, 4,2,4]
    ))
    
    # Update layout for tight margin
    # See https://plotly.com/python/creating-and-updating-figures/
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    
    return fig

def risk_cat_region_fig():
    
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
    df.head()

    colors = ['rgb(239,243,255)','rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)']
    months = {6:'June',7:'July',8:'Aug',9:'Sept'}

    fig = go.Figure()

    for i in range(6,10)[::-1]:
        df_month = df.query('Month == %d' %i)
        fig.add_trace(go.Scattergeo(
            lon = df_month['Lon'],
            lat = df_month['Lat'],
            text = df_month['Value'],
            name = months[i],
            marker = dict(
                size = df_month['Value']/50,
                color = colors[i-6],
                line_width = 0
            )))

    df_sept = df.query('Month == 9')
    fig['data'][0].update(mode='markers+text', textposition='bottom center',
                      text=df_sept['Value'].map('{:.0f}'.format).astype(str)+' '+\
                      df_sept['Country'])

    # Inset
    #fig.add_trace(go.Choropleth(
    #    locationmode = 'country names',
    #    locations = df_sept['Country'],
    #    z = df_sept['Value'],
    #    text = df_sept['Country'],
    #    colorscale = [[0,'rgb(0, 0, 0)'],[1,'rgb(0, 0, 0)']],
    #    autocolorscale = False,
    #    showscale = False,
    #    geo = 'geo2'
    #))

    #fig.add_trace(go.Scattergeo(
    #    lon = [21.0936],
    #    lat = [7.1881],
    #    text = ['Africa'],
    #    mode = 'text',
    #    showlegend = False,
    #    geo = 'geo2'
    #))

    fig.update_layout(
        geo = go.layout.Geo(
            resolution = 50,
            scope = 'africa',
            showframe = False,
            showcoastlines = True,
            landcolor = "white",
            countrycolor = "white" ,
            bgcolor="black",
            #coastlinecolor = "black",
            projection_type = 'mercator',
            lonaxis_range= [ -15.0, -1.0 ],
            lataxis_range= [ 2.0, 12.0 ],
            domain = dict(x = [ 0, 1 ], y = [ 0, 1 ])
        ),
        #geo2 = go.layout.Geo(
        #    scope = 'africa',
        #    showframe = False,
        #    landcolor = "#F0DC82",
        #    showcountries = False,
        #    domain = dict(x = [ 0, 0.6 ], y = [ 0, 0.6 ]),
        #    #bgcolor = 'rgba(255, 255, 255, 0.0)',
        #),
        legend_traceorder = 'reversed'
    )

    return fig





def risk_sup_sum_fig():
    
    # Load data, define hover text and bubble size
    data = px.data.gapminder()
    df_2007 = data[data['year']==2007]
    df_2007 = df_2007.sort_values(['continent', 'country'])

    hover_text = []
    bubble_size = []

    for index, row in df_2007.iterrows():
        hover_text.append(('Country: {country}<br>'+
                      'Life Expectancy: {lifeExp}<br>'+
                      'GDP per capita: {gdp}<br>'+
                      'Population: {pop}<br>'+
                      'Year: {year}').format(country=row['country'],
                                            lifeExp=row['lifeExp'],
                                            gdp=row['gdpPercap'],
                                            pop=row['pop'],
                                            year=row['year']))
        bubble_size.append(math.sqrt(row['pop']))

    df_2007['text'] = hover_text
    df_2007['size'] = bubble_size
    sizeref = 2.*max(df_2007['size'])/(100**2)

    # Dictionary with dataframes for each continent
    continent_names = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
    continent_data = {continent:df_2007.query("continent == '%s'" %continent)
                              for continent in continent_names}

    # Create figure
    fig = go.Figure()

    for continent_name, continent in continent_data.items():
        fig.add_trace(go.Scatter(
            x=continent['gdpPercap'], y=continent['lifeExp'],
            name=continent_name, text=continent['text'],
            marker_size=continent['size'],
            ))

    # Tune marker appearance and layout
    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                              sizeref=sizeref, line_width=2))

    fig.update_layout(
        title='Region Impact to Supply Chain',
        xaxis=dict(
            title='Total Annual Puchases (dollars)',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Risk Likelihood (%)',
            gridcolor='white',
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )
    
    return fig

def risk_prod_sum_fig():
    
    top_labels = ['Prod Comp', 'Trade', 'ESG-Envi', 'ESG-Social','Brand-Defect']
    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
          'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
          'rgba(190, 192, 213, 1)']
    x_data = [[21, 30, 21, 16, 12],
          [24, 31, 19, 15, 11],
          [27, 26, 23, 11, 13],
          [29, 24, 15, 18, 14]]
    y_data = ['Prod Group 4','Prod Group 3', 'Prod Group 2','Prod Group 1']
    
    #top_labels = data['top_labels']
    #colors = data['colors']
    #x_data = data['x_data']
    #y_data = data['y_data']
   

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        #paper_bgcolor='rgb(248, 248, 255)',
        #plot_bgcolor='rgb(248, 248, 255)',
        #margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                            x=0.14, y=yd,
                            xanchor='right',
                            text=str(yd),
                            font=dict(family='Arial', size=14,
                            #          color='rgb(67, 67, 67)'
                                     ),
                            showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                            x=xd[0] / 2, y=yd,
                            text=str(xd[0]) + '%',
                            font=dict(family='Arial', size=10,color='rgb(255, 255,255)'),
                            showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                x=xd[0] / 2, y=1.1,
                                text=top_labels[0],
                                font=dict(family='Arial', size=10),
                                showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                    x=space + (xd[i]/2), y=yd,
                                    text=str(xd[i]) + '%',
                                    font=dict(family='Arial', size=10,color='rgb(255, 255,255)'),
                                    showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                        x=space + (xd[i]/2), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=10),
                                        showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)
    
    
    return fig



def risk_ESG_donut_fig():

    fig = make_subplots(rows=1, cols=4)

    labels = ['Overall','']
    values = [71,29]
    fig.add_trace(go.Pie(labels=labels, values=values, hole=.8,
                             marker={'colors': ['green','white']},
                             textposition='none',
                             domain = {'row': 1, 'column': 0}))
    
    labels = ['Environment','']
    values = [50,50]
    fig.add_trace(go.Pie(labels=labels, values=values, hole=.8,
                             marker={'colors': ['green','white']},
                             domain = {'row': 1, 'column': 1}))
    
    labels = ['Social','']
    values = [62,48]
    fig.add_trace(go.Pie(labels=labels, values=values, hole=.8,
                             marker={'colors': ['green','white']},
                             domain = {'row': 1, 'column': 2}))
    
    labels = ['Governance','']
    values = [86,14]
    fig.add_trace(go.Pie(labels=labels, values=values, hole=.8,
                             marker={'colors': ['green','white']},
                             domain = {'row': 1, 'column': 3}))
  
    
    fig.update_layout(showlegend=False, grid = {'rows': 1, 'columns': 3, 'pattern': "independent"}, height=500, width=600, title_text="Risk Metrics")

    return fig

def risk_dash_fig(data):

    i=j=0
    max = 3

    fig = make_subplots(rows=2, cols=max+1)
    
    for index,item in data.iterrows():
        
        print("coords:  ",j,i)
        
        fig.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = item[2022],
            delta = {'reference': item[2021]},
            title = index,
            domain = {'row': j, 'column': i},
            #gauge_axis_range=[0,1],
            #gauge_bar_color='green'
            ))
    
        if (i<max):
            i=i+1
        else:
            i=0
            if (j<max):
                j=j+1
    
    fig.update_layout(grid = {'rows': 2, 'columns': max+1, 'pattern': "independent"}, height=600, width=800, title_text="Risk Metrics")

    return fig

def prod_vc_fig(labels,data):

    fig = go.Figure(data=[go.Sankey(
        #valueformat = ".0f",
        valuesuffix = "$K",
        # Define nodes
        node = dict(
            pad = 15,
            thickness = 15,
            line = dict(color = "white", width = 0.5),
            label =  list(labels)
            ),
        # Add links
        link = dict(
            source =  data['product_code'].values,
            target =  data['part_code'].values,
            value =   data['qty'].values, 
            color =  data['color'].values
        ))])
    
    return fig
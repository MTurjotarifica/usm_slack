import plotly.graph_objects as go
import plotly
import plotly.io as pio
import plotly.offline as pyo
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as delta
from datetime import timedelta
from vis_functions import *
import requests 
import json

def backgroundworker(text,response_url, df_raw, client):

    
    #NEW ADDITION posts message when keyword isn't available
    if text.lower() not in df_raw.keyword.unique().tolist():
        client.chat_postMessage(channel='#project', 
                                            text=" ",
                                            )
    else:
        pass
    
    #we are creating manuals parameter dictionary for function values at the moment
    params = {'key': f'{text.lower()}',
              'geo': 'DE',
              'cat': 13,
              'startdate': '2022-01-01',
              'index': False,
              'indexdate': '2022-08-01',
              'font_use': 'Roboto Mono Light for Powerline',
              'out_type': 'png'
             }
    
    #function that produces and saves the vis
    def single(key,geo,cat,startdate,index,indexdate,font_use,out_type):

        
        df_key = df_raw[(df_raw.keyword == f'{params.get("key")}')\
                        &(df_raw.country == f'{params.get("geo")}')\
                        &(df_raw.gt_category == int(f'{params.get("cat")}'))]
        if params.get("index")==True: 
            df_key = add_indexing(df_key,'vl_value',f'{params.get("indexdate")}')
            var_new = 'vl_value_index'
        else:
            var_new = 'vl_value'
            #running the functions we created to create moving average, smoother
        df_key = add_ma(df_key,var_new,14)
        df_key = add_smoother(df_key,var_new,0.02) 
        df = df_key[df_key.date>=f'{params["startdate"]}']
        fig = go.Figure()
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new],
                name='original', 
                mode='lines',
                opacity = 0.3,
                line=dict(color='#024D83',
                          width=4),
                showlegend=True
        ))
        #creating the trendline values
        df_trend = df[['date',var_new]]         #i.e we need date and vl_value 
        df_trend0 = df_trend.dropna()           #dropping 0 because trendlines can't cope without numeric values
        x_sub = df_trend0.date    
        y_sub = df_trend0[var_new]
        x_sub_num = mdates.date2num(x_sub)      #transforming dates to numeric values, necessary for polynomial fitting
        z_sub = np.polyfit(x_sub_num, y_sub, 1) #polynomial fitting
        p_sub = np.poly1d(z_sub)
        #adding the trendline trace
        fig.add_trace(
            go.Scatter( 
                x=x_sub, 
                y=p_sub(x_sub_num), 
                name='trend', 
                mode='lines',
                opacity = 1,
                line=dict(color='green',
                          width=4,
                          dash='dash')
        ))
        #adding the 2 week's moving avg trace
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new+'_ma'+str(14)],
                name=var_new+'_ma'+str(14), 
                mode='lines',
                opacity = 1,
                line=dict(color='red',
                          width=4),
                showlegend=True
        ))
        #adding the smoothed trace
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new+'_smooth'],
                name='smoothed', 
                mode='lines',
                opacity = 1,
                line=dict(color='purple',
                          width=6),
                showlegend=True
        ))
        fig.update_layout(
            xaxis={'title': None,
                   'titlefont':{'color':'#BFBFBF', 
                                'family': font_use},
                   'tickfont':{'color':'#002A34',
                               'size':30, 
                               'family': font_use},
                   'gridcolor': '#4A4A4A',
                   'linecolor': '#000000',
                   'showgrid':False},
            yaxis={'title': 'Digital Demand'  ,
                   'titlefont':{'color':'#002A34',
                                'size':50, 
                                'family': font_use},
                   'tickfont':{'color':'#002A34',
                               'size':30, 
                               'family': font_use},
                   'showgrid':False,
                   'zeroline':False},
            margin={'l': 170, 
                    'b': 150, 
                    't': 150,
                    'r': 40},
            title={'text': f'{text}'.capitalize(), 
                   'font':{'color':'#000000', 
                           'size':40,
                           'family': font_use},
                   'yanchor':"top",
                   'xanchor':"center"},
            legend={'font':{'size':20, 
                            'color':'#333',
                            'family': font_use},
                    'yanchor':"top",
                    'xanchor':"center",
                    'y':0.9,
                    'x':.95,
                    'orientation':'v',
                    },
            template = 'none',
            hovermode='x unified',
            width = 1920,
            height = 1080     
        )
        
        
        pio.write_image(fig, 'fig.png')
        client.files_upload(channels='#project', file='fig.png', initial_comment="Visualization: ")

        # fig.write_image(os.path.expanduser(f"{text}.png"))


        payload = {"text":"your task is complete",
                "username": "bot"}

        requests.post(response_url,data=json.dumps(payload))  
        # response_url = payload['response_url']
        # response_data = {
        #     "text": "Processing complete!"
        # }
        # requests.post(response_url, json=response_data)
            
            
        return 'vis completed'
    
    #this is running from vis_functions.py
    single(
        key = f'{text.lower()}', 
        geo = 'DE',
        cat = 13,
        startdate = '2020-01-01',
        index = False,
        indexdate = '2022-08-01',
        font_use = 'Roboto Mono Light for Powerline',
        out_type = 'png'
    )

#test background worker 2
def backgroundworker2(text, init_date, response_url, df_raw, client):   
    #NEW ADDITION
    if text.lower() not in df_raw.keyword.unique().tolist():
        client.chat_postMessage(channel='#project', 
                                            text="Keyword not in Digital Demand Database. Please try the command again with a differenrent keyword. "
                                            )
    else:
        pass
    
    #we are creating manuals parameter dictionary for function values at the moment
    params = {'key': f'{text.lower()}',
              'geo': 'DE',
              'cat': 13,
              'startdate': f'{init_date}',
              'index': False,
              'indexdate': '2022-08-01',
              'font_use': 'Roboto Mono Light for Powerline',
              'out_type': 'png'
             }
    
    #function that produces and saves the vis
    def single(key,geo,cat,startdate,index,indexdate,font_use,out_type):
 
        df_key = df_raw[(df_raw.keyword == f'{params.get("key")}')\
                        &(df_raw.country == f'{params.get("geo")}')\
                        &(df_raw.gt_category == int(f'{params.get("cat")}'))]
        if params.get("index")==True: 
            df_key = add_indexing(df_key,'vl_value',f'{params.get("indexdate")}')
            var_new = 'vl_value_index'
        else:
            var_new = 'vl_value'
            #running the functions we created to create moving average, smoother
        df_key = add_ma(df_key,var_new,14)
        df_key = add_smoother(df_key,var_new,0.02) 
        df = df_key[df_key.date>=f'{params["startdate"]}']
        fig = go.Figure()
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new],
                name='original', 
                mode='lines',
                opacity = 0.3,
                line=dict(color='#024D83',
                          width=4),
                showlegend=True
        ))
        #creating the trendline values
        df_trend = df[['date',var_new]]         #i.e we need date and vl_value 
        df_trend0 = df_trend.dropna()           #dropping 0 because trendlines can't cope without numeric values
        x_sub = df_trend0.date    
        y_sub = df_trend0[var_new]
        x_sub_num = mdates.date2num(x_sub)      #transforming dates to numeric values, necessary for polynomial fitting
        z_sub = np.polyfit(x_sub_num, y_sub, 1) #polynomial fitting
        p_sub = np.poly1d(z_sub)
        #adding the trendline trace
        fig.add_trace(
            go.Scatter( 
                x=x_sub, 
                y=p_sub(x_sub_num), 
                name='trend', 
                mode='lines',
                opacity = 1,
                line=dict(color='green',
                          width=4,
                          dash='dash')
        ))
        #adding the 2 week's moving avg trace
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new+'_ma'+str(14)],
                name=var_new+'_ma'+str(14), 
                mode='lines',
                opacity = 1,
                line=dict(color='red',
                          width=4),
                showlegend=True
        ))
        #adding the smoothed trace
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new+'_smooth'],
                name='smoothed', 
                mode='lines',
                opacity = 1,
                line=dict(color='purple',
                          width=6),
                showlegend=True
        ))
        fig.update_layout(
            xaxis={'title': None,
                   'titlefont':{'color':'#BFBFBF', 
                                'family': font_use},
                   'tickfont':{'color':'#002A34',
                               'size':30, 
                               'family': font_use},
                   'gridcolor': '#4A4A4A',
                   'linecolor': '#000000',
                   'showgrid':False},
            yaxis={'title': 'Digital Demand'  ,
                   'titlefont':{'color':'#002A34',
                                'size':50, 
                                'family': font_use},
                   'tickfont':{'color':'#002A34',
                               'size':30, 
                               'family': font_use},
                   'showgrid':False,
                   'zeroline':False},
            margin={'l': 170, 
                    'b': 150, 
                    't': 150,
                    'r': 40},
            title={'text': f'{text}'.capitalize(), 
                   'font':{'color':'#000000', 
                           'size':40,
                           'family': font_use},
                   'yanchor':"top",
                   'xanchor':"center"},
            legend={'font':{'size':20, 
                            'color':'#333',
                            'family': font_use},
                    'yanchor':"top",
                    'xanchor':"center",
                    'y':0.9,
                    'x':.95,
                    'orientation':'v',
                    },
            template = 'none',
            hovermode='x unified',
            width = 1920,
            height = 1080     
        )
        
        pio.write_image(fig2, 'fig2.png')
        client.files_upload(channels='#project', file='fig2.png', initial_comment="Visualization: ")

        return 'vis completed'
    
    #this is running from vis_functions.py
    single(
        key = f'{text.lower()}', 
        geo = 'DE',
        cat = 13,
        startdate = f'{init_date}',
        index = False,
        indexdate = '2022-08-01',
        font_use = 'Roboto Mono Light for Powerline',
        out_type = 'png'
    )
    
    #payload is required to to send second message after task is completed
    payload = {"text":"your task is complete",
                "username": "bot"}
    
    #uploading the file to slack using bolt syntax for py
    try:
        filename=f"{text}.png"
        response = client.files_upload(channels='#project',
                                        file=filename,
                                        initial_comment="Visualization: ")
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

    requests.post(response_url,data=json.dumps(payload))

#test background worker 2
def backgroundworker3(text, init_date, index_date, response_url, df_raw, client):    
    #NEW ADDITION
    if text.lower() not in df_raw.keyword.unique().tolist():
        client.chat_postMessage(channel='#project', 
                                            text="Keyword not in Digital Demand Database. Please try the command again with a differenrent keyword. "
                                            )
    else:
        pass
    
    #we are creating manuals parameter dictionary for function values at the moment
    params = {'key': f'{text.lower()}',
              'geo': 'DE',
              'cat': 13,
              'startdate': f'{init_date}',
              'index': True,
              'indexdate': f'{index_date}',
              'font_use': 'Roboto Mono Light for Powerline',
              'out_type': 'png'
             }
    
    #function that produces and saves the vis
    def single(key,geo,cat,startdate,index,indexdate,font_use,out_type):
      
        
        df_key = df_raw[(df_raw.keyword == f'{params.get("key")}')\
                        &(df_raw.country == f'{params.get("geo")}')\
                        &(df_raw.gt_category == int(f'{params.get("cat")}'))]
        if params.get("index")==True: 
            df_key = add_indexing(df_key,'vl_value',f'{params.get("indexdate")}')
            var_new = 'vl_value_index'
        else:
            var_new = 'vl_value'
            #running the functions we created to create moving average, smoother
        df_key = add_ma(df_key,var_new,14)
        df_key = add_smoother(df_key,var_new,0.02) 
        df = df_key[df_key.date>=f'{params["startdate"]}']
        fig = go.Figure()
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new],
                name='original', 
                mode='lines',
                opacity = 0.3,
                line=dict(color='#024D83',
                          width=4),
                showlegend=True
        ))
        #creating the trendline values
        df_trend = df[['date',var_new]]         #i.e we need date and vl_value 
        df_trend0 = df_trend.dropna()           #dropping 0 because trendlines can't cope without numeric values
        x_sub = df_trend0.date    
        y_sub = df_trend0[var_new]
        x_sub_num = mdates.date2num(x_sub)      #transforming dates to numeric values, necessary for polynomial fitting
        z_sub = np.polyfit(x_sub_num, y_sub, 1) #polynomial fitting
        p_sub = np.poly1d(z_sub)
        #adding the trendline trace
        fig.add_trace(
            go.Scatter( 
                x=x_sub, 
                y=p_sub(x_sub_num), 
                name='trend', 
                mode='lines',
                opacity = 1,
                line=dict(color='green',
                          width=4,
                          dash='dash')
        ))
        #adding the 2 week's moving avg trace
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new+'_ma'+str(14)],
                name=var_new+'_ma'+str(14), 
                mode='lines',
                opacity = 1,
                line=dict(color='red',
                          width=4),
                showlegend=True
        ))
        #adding the smoothed trace
        fig.add_trace(
            go.Scatter( 
                x=df.date, 
                y=df[var_new+'_smooth'],
                name='smoothed', 
                mode='lines',
                opacity = 1,
                line=dict(color='purple',
                          width=6),
                showlegend=True
        ))
        fig.update_layout(
            xaxis={'title': None,
                   'titlefont':{'color':'#BFBFBF', 
                                'family': font_use},
                   'tickfont':{'color':'#002A34',
                               'size':30, 
                               'family': font_use},
                   'gridcolor': '#4A4A4A',
                   'linecolor': '#000000',
                   'showgrid':False},
            yaxis={'title': 'Digital Demand'  ,
                   'titlefont':{'color':'#002A34',
                                'size':50, 
                                'family': font_use},
                   'tickfont':{'color':'#002A34',
                               'size':30, 
                               'family': font_use},
                   'showgrid':False,
                   'zeroline':False},
            margin={'l': 170, 
                    'b': 150, 
                    't': 150,
                    'r': 40},
            title={'text': f'{text}'.capitalize(), 
                   'font':{'color':'#000000', 
                           'size':40,
                           'family': font_use},
                   'yanchor':"top",
                   'xanchor':"center"},
            legend={'font':{'size':20, 
                            'color':'#333',
                            'family': font_use},
                    'yanchor':"top",
                    'xanchor':"center",
                    'y':0.9,
                    'x':.95,
                    'orientation':'v',
                    },
            template = 'none',
            hovermode='x unified',
            width = 1920,
            height = 1080     
        )
        
        pio.write_image(fig3, 'fig3.png')
        client.files_upload(channels='#project', file='fig3.png', initial_comment="Visualization: ")
            
        return 'vis completed'
    
    #this is running from vis_functions.py
    single(
        key = f'{text.lower()}', 
        geo = 'DE',
        cat = 13,
        startdate = f'{init_date}',
        index = True,
        indexdate = f'{index_date}',
        font_use = 'Roboto Mono Light for Powerline',
        out_type = 'png'
    )
    
    #payload is required to to send second message after task is completed
    payload = {"text":"your task is complete",
                "username": "bot"}
    
    #uploading the file to slack using bolt syntax for py
    try:
        filename=f"{text}.png"
        response = client.files_upload(channels='#project',
                                        file=filename,
                                        initial_comment="Visualization: ")
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

    requests.post(response_url,data=json.dumps(payload))     
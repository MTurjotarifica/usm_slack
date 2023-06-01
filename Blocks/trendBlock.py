import pandas as pd
import mysql.connector as mysql
import numpy as np
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import text as sqlalctext #edit st 2023-03-07

def generate_trend_block(df):
    engine = create_engine('mysql+pymysql://sandbox_read_only:zhsqehk23Xs8tVmVn3sSkyq5TvZumR5q@mysqldatabase.cmi5f1vp8ktf.us-east-1.rds.amazonaws.com:3306/sandbox')

    #creating a connection object
    connection = engine.connect()

    #creating the metadata object
    # metadata = MetaData()

    # Loading the digital_demand table #edit pik 2023-03-07
    # df_dd_raw_table = Table('digital_demand',
    #                        metadata)

    # This is the query to be performed #edit st 2023-03-07
    stmt = "SELECT * FROM digital_demand WHERE (gt_category = 13) AND (country = 'DE') and (date >= '2023-01-01');" #date updated to 2022 jan 1

    df_dd_raw = pd.read_sql(sqlalctext(stmt), connection) #edit st 2023-03-07
    unique_keywords = df_dd_raw['keyword'].unique().tolist()
        
    connection.close()  

    trend_block = [
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Test block with multi static select"
            },
            "accessory": {
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select options",
                    "emoji": True
                },
                "options": [],
                "action_id": "trend-select"
            }
        }
    ]

    options = []
    for keyword in unique_keywords:
        option = {
            "text": {
                "type": "plain_text",
                "text": keyword,
                "emoji": True
            },
            "value": keyword
        }
        options.append(option)

    trend_block[1]['accessory']['options'] = options

    return trend_block

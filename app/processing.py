from app import db, app
from app.models import User, WeighIn

import io, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

def get_weight_bf_graph(user_id):
    if user_id is None:
        print('Error: need df or user_id',flush=True)
    df = pd.read_sql(WeighIn.query.filter_by(user_id=user_id).order_by(WeighIn.timestamp).statement,db.engine)
    
    x1 = df['timestamp']
    y1 = df['weight']
    y2 = df['bf']
    
    fig = plt.figure(figsize=(9,5))
    ax1 = fig.add_subplot(111)
    color = 'tab:red'
    ax1.set_xlabel('date')
    
    ax1.set_ylabel('weight (kg)', color=color)
    ax1.plot(
        x1, 
        y1, 
        color=color, 
        marker='s',
        markerfacecolor=color,
        markeredgecolor=color,
        linestyle = 'None',
    )
    ax1.tick_params(axis='x', labelrotation=40)
    ax1.tick_params(axis='y', labelcolor=color)
    
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)

    ax1.set_ylim([40,85])

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('BF%', color=color)  # we already handled the x-label with ax1
    ax2.plot(
        x1,
        y2, 
        color=color, 
        marker='v',
        markerfacecolor=color,
        markeredgecolor=color,
        linestyle='None'
    )
    ax2.tick_params(axis='y', labelcolor=color)
    
    ax2.set_ylim([0,30])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
        
    # save as bytesIO
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    
    return bytes_image
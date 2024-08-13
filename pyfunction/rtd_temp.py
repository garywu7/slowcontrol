import os
import matplotlib.pyplot as plt
import numpy as np
import time 
import datetime
import matplotlib.dates as mdates
from math import sqrt
import rpyc
from quickle import dumps, loads
def cooling_rtd(x):
    # from Keita
    u, d, w, G, A, B = 3.3, 1, 1.25, 21.58, 3.9083e-3, -5.775e-7  # constants
    I = x  # if isinstance(x, int) else int.from_bytes(x, byteorder='little', signed=False)
    # I = I if I <= 2047 else I - 4096
    I = np.where(I <= 2047, I, I - 4096)
    V = I * 10 / 4096
    R = u * (w * d + V * (u + d) / G) / (w * u - V * (u + d) / G)
    T = (-A + (A**2 - 4 * B * (1 - R)) ** 0.5) / (2 * B)
    return T  # degree C

def plot_rtd_temp(fignum,timeperiod):
    
    try:
        time_end_string=request.form['timeend']
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
    except:
        timeend = int(time.time())
        #timeend=1687219200
    try:
        time_begin_string=request.form['timebegin']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60

    # Convert timestamps to datetime objects
    utc_time_begin = datetime.datetime.utcfromtimestamp(timebegin)
    utc_time_end = datetime.datetime.utcfromtimestamp(timeend)
    cl=['b','g','r','c','m','y','orange','purple']
    fig, ax = plt.subplots(figsize=(1800/100, 500/100), dpi=100)
   
    #conn = sqlite3.connect('gsedb_nts.sqlite')
    conn= rpyc.connect('127.0.0.1', 44555)
    sql=f'SELECT gcutime FROM cooling WHERE gcutime >= {timebegin} AND gcutime <= {timeend} ;'
    data=conn.root.query(sql)
    ti=loads(data)
    maxtemp=0
    for i in range(8):
        rtdid=fignum*8+i
        temp_adc = {}
        temp={}
        query=f'SELECT rtd_{rtdid} FROM cooling WHERE gcutime >= {timebegin} AND gcutime <= {timeend};'
        data=conn.root.query(query)
        temp_adc[f"rtdtemp_adc_{rtdid}"]=loads(data)
        
        
        temp[f"rtd_{rtdid}"]=[cooling_rtd(ts[0])for ts in temp_adc[f"rtdtemp_adc_{rtdid}"]]
        ti_int = [int(ts[0]) for ts in ti]
        utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
        plt.plot(utc_times, temp[f"rtd_{rtdid}"],color=cl[i])
        maxtemp=max([maxtemp]+temp[f"rtd_{rtdid}"])
    plt.xlim(utc_time_begin,utc_time_end)
    fig.patch.set_alpha(0.) 
    if maxtemp>20:
        plt.ylim(top=20) 
    plt.xticks(rotation=45)
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Temperature (C)')
    ax.set_title(f'RTDTEMP_Group{fignum} ')

    plt.tight_layout()
    plt.savefig(f'./static/images/rtd{fignum}.png')
  
import os
import matplotlib.pyplot as plt
from flask import Flask, render_template,request,jsonify
import numpy as np
import time 
import datetime
import matplotlib.dates as mdates
import rpyc
from quickle import dumps, loads
def plot_event_display_getrowid(timeperiod,layer):
    
    try:
        time_end_string=request.form['timeend']
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
    except:
        timeend = int(time.time())
    try:
        time_begin_string=request.form['timebegin']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60

    # Convert timestamps to datetime objects
    sys=layer+128
    conn= rpyc.connect('127.0.0.1', 44555)
    sql=f'SELECT rowid FROM gfptrackerpacket WHERE gcutime >= {timebegin} AND gcutime <= {timeend} AND sysid=={sys} order by gcutime desc;'
    data=conn.root.query(sql)
    packet_rowid=loads(data)
    #conn = sqlite3.connect('gsedb_nts.sqlite')
    #cursor = conn.cursor()
    #cursor.execute(f'SELECT rowid,sysid FROM gfptrackerpacket WHERE gcutime >= {timebegin} AND gcutime <= {timeend} order by gcutime desc;')
    #packet_rowid = cursor.fetchall()
    #cursor.close()
    conn.close()
    return packet_rowid

def plot_event_display(packet_rowid,layer,row,module,channel):    
    
    packet_rowid_list = "(" + ", ".join(str(t[0]) for t in packet_rowid) + ")"
    
    #packet_rowid_min=packet_rowid[-1][0]
    #packet_rowid_max=packet_rowid[0][0]
    #print(packet_rowid_max,packet_rowid_min)
    #conn = sqlite3.connect('gsedb_nts.sqlite')
    #cursor = conn.cursor()
    conn= rpyc.connect('127.0.0.1', 44555)
    #sql=f'SELECT rowid FROM gfptrackerevent WHERE parent >= {packet_rowid_min} AND parent <= {packet_rowid_max} order by parent desc;'
    sql=f'SELECT rowid FROM gfptrackerevent WHERE parent in ' + packet_rowid_list +' order by parent desc;'
    
    #cursor.execute('SELECT rowid FROM gfptrackerevent WHERE parent >= ? AND parent <= ? ;',(packet_rowid_min,packet_rowid_max))
    #event_rowid = cursor.fetchall()
    data=conn.root.query(sql)
    event_rowid =loads(data)
    #event_rowid_max=event_rowid[0][0]
    #event_rowid_min=event_rowid[-1][0]
    #print(event_rowid_max,event_rowid_min)
    event_rowid_list = "(" + ", ".join(str(t[0]) for t in event_rowid) + ")"
    energy_range = (100, 1500)
    #cursor = conn.cursor()
    cl=['b','g','r','c','m','y']
    if module =='all':
        plt.figure(figsize=(16, 8))
        for i in range(6):
            #query=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= ? AND parent <= ? AND row = ? AND module = ?AND (asiceventcode = 0 OR asiceventcode=2);'
            sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent in ' +event_rowid_list+f' AND row = {row} AND module = {i} AND (asiceventcode = 0 OR asiceventcode=2);'
            #sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= {event_rowid_min} AND parent <= {event_rowid_max} AND row = {row} AND module = {i} AND (asiceventcode = 0 OR asiceventcode=2);'
            data=conn.root.query(sql)
            #cursor.execute(query,(event_rowid_min,event_rowid_max,row,i))
            #adc = cursor.fetchall()
            adc=loads(data)
            energy_data = [entry[0] for entry in adc]
            hist_counts, hist_bins = np.histogram(energy_data, bins=100,range=energy_range)  # 这里将能量数据分成 10 个 bin  
            # 获取每个 bin 的中心点（可选）
            hist_left = hist_bins[:-1]
            hist_right = hist_bins[1:]

            # 绘制直方图的线图
            

            # 绘制每个 bin 对应的横线
            plt.hlines(hist_counts, hist_left, hist_right, color=cl[i], lw=2)

            # 绘制相邻 bin 之间的垂直线
            for j in range(len(hist_counts) - 1):
                plt.vlines(hist_right[j], hist_counts[j], hist_counts[j+1], colors=cl[i], lw=2)
            # 添加标题和标签
        plt.title(f'Spectrum_L{layer}R{row}')

    elif channel =='all':
        #sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= {event_rowid_min} AND parent <= {event_rowid_max} AND row = {row} AND module = {module} AND (asiceventcode = 0 OR asiceventcode=2);'
        sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent in ' +event_rowid_list+f' AND row = {row} AND module = {module} AND (asiceventcode = 0 OR asiceventcode=2);'
        #cursor.execute('SELECT adcdata FROM gfptrackerhit WHERE parent >= ? AND parent <= ? AND row = ? AND module = ? AND (asiceventcode = 0 OR asiceventcode=2);',(event_rowid_min,event_rowid_max,row,module))
        #adc = cursor.fetchall()
        data=conn.root.query(sql)
        adc=loads(data)
        energy_data = [entry[0] for entry in adc]
        hist_counts, hist_bins = np.histogram(energy_data, bins=100,range=energy_range)  # 这里将能量数据分成 10 个 bin  
        # 获取每个 bin 的中心点（可选）
        hist_left = hist_bins[:-1]
        hist_right = hist_bins[1:]

        # 绘制直方图的线图
        plt.figure(figsize=(16, 8))

        # 绘制每个 bin 对应的横线
        plt.hlines(hist_counts, hist_left, hist_right, color='b', lw=2)

        # 绘制相邻 bin 之间的垂直线
        for i in range(len(hist_counts) - 1):
            plt.vlines(hist_right[i], hist_counts[i], hist_counts[i+1], colors='b', lw=2)
        # 添加标题和标签
        plt.title(f'Spectrum_L{layer}R{row}M{module}')
    else:
        #cursor.execute('SELECT adcdata FROM gfptrackerhit WHERE parent >= ? AND parent <= ? AND row = ? AND module = ? AND channel=? AND (asiceventcode = 0 OR asiceventcode=2);',(event_rowid_min,event_rowid_max,row,module,channel))
        #sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= {event_rowid_min} AND parent <= {event_rowid_max} AND row = {row} AND channel={channel} AND module = {module} AND (asiceventcode = 0 OR asiceventcode=2);'
        sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent in ' +event_rowid_list+f' AND row = {row} AND module = {module} AND channel={channel} AND (asiceventcode = 0 OR asiceventcode=2);'

        data=conn.root.query(sql)
        adc=loads(data)
        #adc = cursor.fetchall()
        energy_data = [entry[0] for entry in adc]
        hist_counts, hist_bins = np.histogram(energy_data, bins=100,range=energy_range)  # 这里将能量数据分成 10 个 bin  
        # 获取每个 bin 的中心点（可选）
        hist_left = hist_bins[:-1]
        hist_right = hist_bins[1:]

        # 绘制直方图的线图
        plt.figure(figsize=(16, 8))

        # 绘制每个 bin 对应的横线
        plt.hlines(hist_counts, hist_left, hist_right, color='b', lw=2)

        # 绘制相邻 bin 之间的垂直线
        for i in range(len(hist_counts) - 1):
            plt.vlines(hist_right[i], hist_counts[i], hist_counts[i+1], colors='b', lw=2)
        # 添加标题和标签
        plt.title(f'Spectrum_L{layer}R{row}M{module}CH{channel}')
    plt.xlabel('ADC')
    plt.ylabel('Counts')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'./static/images/event_display_layer{layer}.png')
    #cursor.close()
    conn.close()
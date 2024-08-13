import os
import matplotlib.pyplot as plt
import numpy as np
import time 
import datetime
import matplotlib.dates as mdates
import rpyc
from quickle import dumps, loads
def plot_event_display_getrowid(tibegin,timeperiod,layer):
    
    timebegin = int(tibegin)
    timeend = timebegin+timeperiod

    # Convert timestamps to datetime objects
    sys=layer+128
    conn= rpyc.connect('127.0.0.1', 44555)
    sql=f'SELECT rowid,gcutime FROM gfptrackerpacket WHERE gcutime >= {timebegin} AND gcutime <= {timeend} AND sysid=={sys} order by gcutime desc;'
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
    
    conn= rpyc.connect('127.0.0.1', 44555)
    
    sql=f'SELECT rowid FROM gfptrackerevent WHERE parent in ' + packet_rowid_list +' order by parent desc;'
    
    data=conn.root.query(sql)
    event_rowid =loads(data)
    
    
    event_rowid_list = "(" + ", ".join(str(t[0]) for t in event_rowid) + ")"
    
    if module =='all':
        plt.figure(figsize=(16, 8))
        for i in range(6):
            #query=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= ? AND parent <= ? AND row = ? AND module = ?AND (asiceventcode = 0 OR asiceventcode=2);'
            sql=f'SELECT adcdata ,asiceventcode FROM gfptrackerhit WHERE parent in ' +event_rowid_list+f' AND row = {row} AND module = {i} AND (asiceventcode = 0 OR asiceventcode=2);'
            #sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= {event_rowid_min} AND parent <= {event_rowid_max} AND row = {row} AND module = {i} AND (asiceventcode = 0 OR asiceventcode=2);'
            data=conn.root.query(sql)
            #cursor.execute(query,(event_rowid_min,event_rowid_max,row,i))
            #adc = cursor.fetchall()
            adc=loads(data)
            energy_data = [entry[0] for entry in adc]
            hist_counts, hist_bins = np.histogram(energy_data, bins=100,range=energy_range)  # 这里将能量数据分成 10 个 bin  
            
    elif channel =='all':
        #sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent >= {event_rowid_min} AND parent <= {event_rowid_max} AND row = {row} AND module = {module} AND (asiceventcode = 0 OR asiceventcode=2);'
        sql=f'SELECT adcdata FROM gfptrackerhit WHERE parent in ' +event_rowid_list+f' AND row = {row} AND module = {module} AND (asiceventcode = 0 OR asiceventcode=2);'
        #cursor.execute('SELECT adcdata FROM gfptrackerhit WHERE parent >= ? AND parent <= ? AND row = ? AND module = ? AND (asiceventcode = 0 OR asiceventcode=2);',(event_rowid_min,event_rowid_max,row,module))
        #adc = cursor.fetchall()
        #data=conn.root.query(sql)
        #adc=loads(data)
        #energy_data = [entry[0] for entry in adc]
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
        sql=f'SELECT adcdata,asiceventcode,parent,module,channel FROM gfptrackerhit WHERE parent in ' +event_rowid_list+f' AND row = {row}  AND (asiceventcode = 0 OR asiceventcode=2);'
        #sql=f'SELECT adcdata,asiceventcode,parent,module,channel FROM gfptrackerhit WHERE parent= 19286404548 AND row = {row} ;'

        data=conn.root.query(sql)
        adc=loads(data)

        f=open(resultlist,mode='a',encoding='utf-8')
        for i in range(len(adc)):
            f.write(str(layer)+' '+str(row)+' '+str(adc[i][3])+' '+str(adc[i][4])+' '+str(adc[i][1])+' '+str(adc[i][0])+' '+str(adc[i][2])+'\n')
    conn.close()
for p in range(48):
    begintime=1723001127+p*30
    resultlist=f'./{begintime}_{begintime+30}.txt'
    for i in range(7):
        packet_rowid=plot_event_display_getrowid(begintime,30,i)
        
        print('end')
        for j in range(6):
            
            try:
                plot_event_display(packet_rowid,i,j,0,0)
                print('finish'+str(i)+str(j))
            except:
                print('error:'+str(i)+str(j)+str(p))
            
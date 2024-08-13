import os
from flask import Flask, render_template,request,jsonify
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time 
import datetime
import matplotlib.dates as mdates
import rpyc
from quickle import dumps, loads
def plot_HLVPS(timeperiod):
    try:
        layer_string=request.form['layer']
        layer=int(layer_string)
    except:
        layer = 0
    try:
        row_string=request.form['row']
        row=int(row_string)
    except:
        row = 0
    try:
        module_string=request.form['module']
        module=int(module_string)
    except:
        module = 0    
    try:
        time_end_string=request.form['timeend1']
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
    except:
        #timeend = int(time.time())
        timeend =int(time.time())
    try:
        time_begin_string=request.form['timebegin1']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60

    # Convert timestamps to datetime objects
    utc_time_begin = datetime.datetime.utcfromtimestamp(timebegin)
    utc_time_end = datetime.datetime.utcfromtimestamp(timeend)

    conn = sqlite3.connect('test2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT gcutime FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer == ? AND row ==? AND module ==?;',(timebegin,timeend,layer,row,module))
    ti = cursor.fetchall()
    cursor.execute('SELECT HV FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,layer,row,module))
    HV= cursor.fetchall()
    cursor.execute('SELECT digital_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,layer,row,module))
    LV1= cursor.fetchall()
    cursor.execute('SELECT analog_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,layer,row,module))
    LV2= cursor.fetchall()
    cursor.execute('SELECT calib_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,layer,row,module))
    LV3= cursor.fetchall()
    cursor.execute('SELECT IF_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,layer,row,module))
    LV4= cursor.fetchall()
    cursor.close()
    conn.close()
    ti_int = [int(ts[0]) for ts in ti]
    utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
    # Plotting
    
    fig, ax = plt.subplots()
    plt.figure(figsize=(1500/100, 600/100), dpi=100)
    #plt.plot(utc_times, temp,marker='o')
    plt.plot(utc_times, HV)
    plt.xlim(utc_time_begin,utc_time_end)
    # Set x-axis major locator and formatter dynamically
    
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.ylabel('HV')
    plt.title(f'HVPS_L{layer}R{row}M{module} ')

    plt.tight_layout()
    plt.savefig('./static/images/power_load_HV.png')

    fig, ax = plt.subplots()
    plt.figure(figsize=(1500/100, 600/100), dpi=100)
    #plt.plot(utc_times, temp,marker='o')
    plt.plot(utc_times, LV1)
    plt.xlim(utc_time_begin,utc_time_end)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.ylabel('Digital_LV')
    plt.title(f'Digital_LV_L{layer}R{row}M{module} ')
    plt.tight_layout()
    plt.savefig('./static/images/power_load_digital_LV.png')

    fig, ax = plt.subplots()
    plt.figure(figsize=(1500/100, 600/100), dpi=100)
    #plt.plot(utc_times, temp,marker='o')
    plt.plot(utc_times, LV2)
    plt.xlim(utc_time_begin,utc_time_end)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.ylabel('Analog_LV')
    plt.title(f'Analog_LV_L{layer}R{row}M{module} ')
    plt.tight_layout()
    plt.savefig('./static/images/power_load_analog_LV.png')

    fig, ax = plt.subplots()
    plt.figure(figsize=(2000/100, 600/100), dpi=100)
    #plt.plot(utc_times, temp,marker='o')
    plt.plot(utc_times, LV3)
    plt.xlim(utc_time_begin,utc_time_end)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.ylabel('Calib_LV')
    plt.title(f'Calib_LV_L{layer}R{row}M{module} ')
    plt.tight_layout()
    plt.savefig('./static/images/power_load_calib_LV.png')

    fig, ax = plt.subplots()
    plt.figure(figsize=(1500/100, 600/100), dpi=100)
    #plt.plot(utc_times, temp,marker='o')
    plt.plot(utc_times, LV4)
    plt.xlim(utc_time_begin,utc_time_end)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.ylabel('IF_LV')
    plt.title(f'IF_LV_L{layer}R{row}M{module} ')
    plt.tight_layout()
    plt.savefig('./static/images/power_load_if_LV.png')



  
   



def lvps(timeperiod,layer,row):
    i=int(layer)
    
    try:
        time_end_string=request.form['timeend0']
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
    except:
        #timeend = int(time.time())
        timeend =int(time.time())
    try:
        time_begin_string=request.form['timebegin0']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60
    
    utc_time_begin = datetime.datetime.utcfromtimestamp(timebegin)
    utc_time_end = datetime.datetime.utcfromtimestamp(timeend)
    conn= rpyc.connect('127.0.0.1', 44555)
    if row != 'all':
        j=int(row)
        crate = i % 2
        card = i + (i + 1) % 2 + j // 3 
        if j%3==0:
            connector='a'
            
        elif j%3==1:
            connector='b'
            
        else:
            connector='c'
            
        if i==1 and j==2:
            crate==1
            card=9
            connector='b'
            
        if i==5 and j==2:
            crate==1
            card=9
            connector='c'
        sql=f"SELECT gcutime, lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_a2i8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
        data=conn.root.query(sql)

        #cursor.execute('SELECT digital_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,i,j,k))
        # 获取当前通道的开关状态
        LV = loads(data)
        ti_int = [int(ts[0]) for ts in LV]
        lv_IF=[ts[1] for ts in LV]
        lv_digital=[ts[2] for ts in LV]
        lv_analog=[ts[3] for ts in LV]
        lv_calib=[ts[4] for ts in LV]
        print(lv_calib)
        utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
        
        plt.xticks(rotation=45)
        plt.xlabel('Time (UTC)')
        plt.xlim(utc_time_begin,utc_time_end)

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        plt.plot(utc_times, lv_IF)
        plt.ylabel('LV_IF')
        plt.title(f'LV_IF_L{i}R{j}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_IF.png')
        
        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        plt.plot(utc_times, lv_digital)
        plt.ylabel('LV_Digital')
        plt.title(f'LV_Digital_L{i}R{j}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_digital.png')

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        plt.plot(utc_times, lv_analog)
        plt.ylabel('LV_Analog')
        plt.title(f'LV_Analog_L{i}R{j}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_analog.png')

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        plt.plot(utc_times, lv_calib)
        plt.ylabel('LV_Calib')
        plt.title(f'LV_Calib_L{i}R{j}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_calib.png')
    else:
        
        plt.xticks(rotation=45)
        plt.xlabel('Time (UTC)')
        plt.xlim(utc_time_begin,utc_time_end)
        cl=['b','g','r','c','m','y']
        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        for j in range(6):
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'
                
            elif j%3==1:
                connector='b'
                
            else:
                connector='c'
                
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            sql=f"SELECT gcutime, lv_d3v8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            #sql=f"SELECT gcutime, lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_a2i8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            data=conn.root.query(sql)

            #cursor.execute('SELECT digital_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,i,j,k))
            # 获取当前通道的开关状态
            LV = loads(data)
            ti_int = [int(ts[0]) for ts in LV]
            lv_IF=[ts[1] for ts in LV]
            #lv_digital=[ts[2] for ts in LV]
            #lv_analog=[ts[3] for ts in LV]
            #lv_calib=[ts[4] for ts in LV]           
            utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
            plt.plot(utc_times, lv_IF,color=cl[j])
        plt.ylabel('LV_IF')
        plt.title(f'LV_IF_L{i}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_IF.png')

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        for j in range(6):
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'
                
            elif j%3==1:
                connector='b'
                
            else:
                connector='c'
                
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            sql=f"SELECT gcutime, lv_d2v8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            #sql=f"SELECT gcutime, lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_a2i8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            data=conn.root.query(sql)

            #cursor.execute('SELECT digital_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,i,j,k))
            # 获取当前通道的开关状态
            LV = loads(data)
            ti_int = [int(ts[0]) for ts in LV]
            #lv_IF=[ts[1] for ts in LV]
            lv_digital=[ts[1] for ts in LV]
            #lv_analog=[ts[3] for ts in LV]
            #lv_calib=[ts[4] for ts in LV]           
            utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
            plt.plot(utc_times, lv_digital,color=cl[j])
        plt.ylabel('LV_Digital')
        plt.title(f'LV_Digital_L{i}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_digital.png')

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100,400/100), dpi=100)
        for j in range(6):
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'
                
            elif j%3==1:
                connector='b'
                
            else:
                connector='c'
                
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            sql=f"SELECT gcutime, lv_a2v8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            #sql=f"SELECT gcutime, lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_a2i8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            data=conn.root.query(sql)

            #cursor.execute('SELECT digital_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,i,j,k))
            # 获取当前通道的开关状态
            LV = loads(data)
            ti_int = [int(ts[0]) for ts in LV]
            #lv_IF=[ts[1] for ts in LV]
            #lv_digital=[ts[2] for ts in LV]
            lv_analog=[ts[1] for ts in LV]
            #lv_calib=[ts[4] for ts in LV]           
            utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
            plt.plot(utc_times, lv_analog,color=cl[j])
        plt.ylabel('LV_Analog')
        plt.title(f'LV_Analog_L{i}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_analog.png')

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        for j in range(6):
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'
                
            elif j%3==1:
                connector='b'
                
            else:
                connector='c'
                
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            sql=f"SELECT gcutime, lv_a3v3_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            #sql=f"SELECT gcutime, lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_a2i8_{connector} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
            data=conn.root.query(sql)

            #cursor.execute('SELECT digital_lv FROM tracker_power2 WHERE gcutime >= ? AND gcutime <= ? AND layer== ? AND row ==? AND module ==?;',(timebegin,timeend,i,j,k))
            # 获取当前通道的开关状态
            LV = loads(data)
            ti_int = [int(ts[0]) for ts in LV]
            #lv_IF=[ts[1] for ts in LV]
            #lv_digital=[ts[2] for ts in LV]
            #lv_analog=[ts[3] for ts in LV]
            lv_calib=[ts[1] for ts in LV]           
            utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
            plt.plot(utc_times, lv_calib,color=cl[j])
        plt.ylabel('LV_Calib')
        plt.title(f'LV_Calib_L{i}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_lv_calib.png')


def hvps(timeperiod,layer,row,module):
    
    try:
        time_end_string=request.form['timeend1']
        print(time_end_string)
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
        
    except:
        
        timeend =int(time.time())
    try:
        time_begin_string=request.form['timebegin1']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60
    
    i=int(layer)
    
    j=int(row)
    
    utc_time_begin = datetime.datetime.utcfromtimestamp(timebegin)
    utc_time_end = datetime.datetime.utcfromtimestamp(timeend)
    conn= rpyc.connect('127.0.0.1', 44555)
    crate = i % 2
    card = i + (i + 1) % 2 + j // 3 
    cl=['b','g','r','c','m','y']
    if module=='all':
        if j%3==0:
            connector='a'
            channel=1
        elif j%3==1:
            connector='b'
            channel=7
        else:
            connector='c'
            channel=13
        if i==1 and j==2:
            crate==1
            card=9
            connector='b'
            channel=7
        if i==5 and j==2:
            crate==1
            card=9
            connector='c'
            channel=13
        sql=f"SELECT gcutime, hv_voltage_{channel}, hv_voltage_{channel+1}, hv_voltage_{channel+2}, hv_voltage_{channel+3},hv_voltage_{channel+4}, hv_voltage_{channel+5} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
        data=conn.root.query(sql)

        HV = loads(data)
        ti_int = [int(ts[0]) for ts in HV]
        HV_m0=[ts[1] for ts in HV]
        HV_m1=[ts[2] for ts in HV]
        HV_m2=[ts[3] for ts in HV]
        HV_m3=[ts[4] for ts in HV]
        HV_m4=[ts[5] for ts in HV]
        HV_m5=[ts[6] for ts in HV]
        
       
        utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
        
        plt.xticks(rotation=45)
        plt.xlabel('Time (UTC)')
        plt.xlim(utc_time_begin,utc_time_end)

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100,400/100), dpi=100)
        plt.plot(utc_times, HV_m0,color=cl[0])
        plt.plot(utc_times, HV_m1,color=cl[1])
        plt.plot(utc_times, HV_m2,color=cl[2])
        plt.plot(utc_times, HV_m3,color=cl[3])
        plt.plot(utc_times, HV_m4,color=cl[4])
        plt.plot(utc_times, HV_m5,color=cl[5])

        plt.ylabel('HV')
        plt.title(f'HV_L{i}R{j}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_HV.png')    
    else:
        m=int(module)
        if j%3==0:
            connector='a'
            channel=m+1
        elif j%3==1:
            connector='b'
            channel=m+7
        else:
            connector='c'
            channel=m+13
        if i==1 and j==2:
            crate==1
            card=9
            connector='b'
            channel=m+7
        if i==5 and j==2:
            crate==1
            card=9
            connector='c'
            channel=m+13
        sql=f"SELECT gcutime, hv_voltage_{channel} from tracker_power WHERE gcutime > {timebegin} AND gcutime < {timeend} AND crate = {crate} AND card = {card}  order by gcutime desc ;"
        data=conn.root.query(sql)

        HV = loads(data)
        ti_int = [int(ts[0]) for ts in HV]
        HV_m=[ts[1] for ts in HV]
        
        
        
        utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
        
        plt.xticks(rotation=45)
        plt.xlabel('Time (UTC)')
        plt.xlim(utc_time_begin,utc_time_end)

        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 400/100), dpi=100)
        plt.plot(utc_times, HV_m,color=cl[0])
        

        plt.ylabel('HV')
        plt.title(f'HV_L{i}R{j}M{m}')
        plt.tight_layout()
        plt.savefig('./static/images/power_load_HV.png')    
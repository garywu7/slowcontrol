import os
from flask import Flask, render_template,request,jsonify
from json import load as jsonload
import numpy as np

from pyfunction.tracker.event_display import plot_event_display_getrowid,plot_event_display
from pyfunction.tracker.power_load import lvps,hvps
from pyfunction.tracker.power_status import plot_power_lv_status,plot_power_hv_status,plot_power_hvlv_status
from pyfunction.tracker.asic_temp import temp_trans,temp_heat,plot_asic_temp
from pyfunction.pdu_plot import plot_pdu_status,pdu_temp,pdu_voltage,pdu_current,pdu_load
from pyfunction.rtd_temp import cooling_rtd,plot_rtd_temp
#from wtforms import Form, BooleanField, TextField, PasswordField, validators
#from flask_login import LoginManager
#from flask_login import UserMixin, current_user
#from flask_login import login_user, logout_user, login_required


APPDIR = os.path.abspath(os.path.dirname(__file__))
CFG_FILE = os.path.join(APPDIR, 'config.json')
fp = open(CFG_FILE, 'r')
cfg = jsonload(fp)

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'  # default login view for login_manager
#login_manager.login_message = 'Please log in'






app = Flask(__name__)

   
@app.route('/')
def index():
    for i in [0,2,3]:
        plot_pdu_status(i)
    for i in range(4):
        plot_rtd_temp(i,60)
    plot_power_hvlv_status()
    
    for i in range(7):
        temp_heat(i)
    return render_template('index.html')



@app.route('/TOF', methods=['GET', 'POST'])
def TOF():
    
   
    
    return render_template('TOF.html')


   

@app.route('/Tracker', methods=['GET', 'POST'])
def Tracker():
    return render_template('Tracker.html')
@app.route('/Tracker/Power_Status', methods=['GET', 'POST'])
def power_status():
    
    plot_power_hvlv_status()
    return render_template('power_status.html')

@app.route('/Tracker/Power_Load', methods=['GET', 'POST'])
def power_load():
    try:
        timeperiod = request.form['timeperiod0']
    except:
        timeperiod=15
    if timeperiod=="":
        try:
            timeperiod= request.form.get('selecttime0')
        except:
            timeperiod=15
    if timeperiod==None:timeperiod=15
    try:
        layer= request.form.get('layer0')
    except:
        layer=3
    if layer==None:layer=3
    try:
        row= request.form.get('row0')
    except:
        row='all'
    if row==None:row='all'
    
    lvps(timeperiod,layer,row)
    try:
        module= request.form.get('module1')
    except:
        module='all'
    if module==None:module='all'
    try:
        timeperiod = request.form['timeperiod1']
    except:
        timeperiod=15
    if timeperiod=="":
        try:
            timeperiod= request.form.get('selecttime1')
        except:
            timeperiod=15
    if timeperiod==None:timeperiod=15
    try:
        layer= request.form.get('layer1')
    except:
        layer=3
    if layer==None:layer=3
    try:
        row= request.form.get('row1')
    except:
        row=3
    if row==None:row=3
    
    hvps(timeperiod,layer,row,module)
    return render_template('power_load.html')

@app.route('/Tracker/Asic_Temp', methods=['GET', 'POST'])
def asic_temp():
    try:
        row= request.form.get('row')
    except:
        row=3
    if row==None:row=3
    try:
        module= request.form.get('module')
    except:
        module='all'
    if module==None:module='all'
    try:
        timeperiod = request.form['timeperiod']
    except:
        timeperiod=15
    if timeperiod=="":
        try:
            timeperiod= request.form.get('selecttime')
        except:
            timeperiod=15
    if timeperiod==None:timeperiod=15
    for i in range(7):
        plot_asic_temp(i,timeperiod,row,module)
        temp_heat(i)
    return render_template('asic_temp.html')

@app.route('/Tracker/Trigger_Rate', methods=['GET', 'POST'])
def trigger_rate():
    return render_template('trigger_rate.html')

@app.route('/Tracker/Band_Width', methods=['GET', 'POST'])
def band_width():
    return render_template('band_width.html')

@app.route('/Tracker/Event_Display', methods=['GET', 'POST'])
def event_display():
    try:
        timeperiod = request.form['timeperiod']
    except:
        timeperiod=5
    if timeperiod=="":
        try:
            timeperiod= request.form.get('selecttime')
        except:
            timeperiod=5
    if timeperiod==None:timeperiod=5
    try:
        row= request.form.get('row')
    except:
        row=3
    if row==None:row=3
    try:
        module= request.form.get('module')
    except:
        module='all'
    if module==None:module='all'
    try:
        channel= request.form.get('channel')
    except:
        channel=0
    if channel==None:channel=0
    packet_rowid=plot_event_display_getrowid(timeperiod,0)
    plot_event_display(packet_rowid,0,row,module,channel)
    
    packet_rowid=plot_event_display_getrowid(timeperiod,1)
    plot_event_display(packet_rowid,1,row,module,channel)
    
    packet_rowid=plot_event_display_getrowid(timeperiod,2)
    plot_event_display(packet_rowid,2,row,module,channel)
    
    packet_rowid=plot_event_display_getrowid(timeperiod,3)
    plot_event_display(packet_rowid,3,row,module,channel)
    
    packet_rowid=plot_event_display_getrowid(timeperiod,4)
    plot_event_display(packet_rowid,4,row,module,channel)
    
    packet_rowid=plot_event_display_getrowid(timeperiod,5)
    plot_event_display(packet_rowid,5,row,module,channel)
    
    packet_rowid=plot_event_display_getrowid(timeperiod,6)
    plot_event_display(packet_rowid,6,row,module,channel)
    return render_template('event_display.html')




@app.route('/Thermal')
def Thermal():
    for i in range(8):
        plot_rtd_temp(i,60)
    for i in range(7):
        temp_heat(i)
    return render_template('Thermal.html')




@app.route('/Payload')
def Payload():
    try:
        timeperiod = request.form['timeperiod']
    except:
        timeperiod=15
    if timeperiod=="":
        try:
            timeperiod= request.form.get('selecttime')
        except:
            timeperiod=15
    if timeperiod==None:timeperiod=15
    for i in [0,2,3]:
        plot_pdu_status(i)
        pdu_load(timeperiod,i)
    return render_template('Payload.html')  
          
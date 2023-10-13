# -*- coding: utf-8 -*-
"""
gui_interface.py
Created on Mon Sep 18 20:45:50 2023

@author:Carlos Alberto Duran Villalobos-The University of Manchester
"""
import ipywidgets as widgets
from IPython.display import display, clear_output
from cells_sim_2 import tcellmodel, control_tcell
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn import preprocessing

def sim(tcellmodel, hours, us, variability):
    #plt.style.available
    plt.style.use('seaborn-v0_8') #use plot styles
    [sx,sy,su] = control_tcell(tcellmodel, hours, us, variability)

    
    #plot figures
    font = 30
    fig, axs = plt.subplots(1,2, figsize=(16, 6))
    
    axs[0].plot(su,color='tab:brown', linewidth=3)
    axs[0].set_xlabel('Time [h]', fontsize = font)
    axs[0].set_ylabel('Feed rate [mL/h]', fontsize = font,color='tab:brown')
    axs[0].yaxis.set_tick_params(labelsize=font)
    axs[0].xaxis.set_tick_params(labelsize=font);
    axs[0].tick_params(axis='y', labelcolor='tab:brown')
    axs[0].set_ylim([0, 2])
    axs[1].plot(sy*sx[:,3],color='blue', linewidth=3)
    #axs[1].plot(sy,color='blue', linewidth=3)
    axs[1].set_xlabel('Time [h]', fontsize = font)
    axs[1].set_ylabel('Viable T-cells', fontsize = font,color='blue')
    axs[1].axhline(y=100e6, color="red", linestyle="--", label='Desired harvest')
    axs[1].axvline(x=96, color="red", linestyle="--", label='Desired harvest')
    axs[1].yaxis.set_tick_params(labelsize=font)
    axs[1].xaxis.set_tick_params(labelsize=font)
    #
    axs[1].tick_params(axis='y', labelcolor='blue')
    #axs[1].set_ylim([0, 1.5e8])
    handles, labels = axs[1].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axs[1].legend(by_label.values(), by_label.keys(), fontsize = font-10)

  
    #fig.delaxes(axs[2,2])
    fig.tight_layout(pad=0.8)
    clear_output(wait = True)
    #plt.pause(0.1)
    plt.show()
    return 

def display_selected_plot(a,b,c,d,e,f,g,h,i,j,via,inh,rg,bi):
        #Simulation with a feed
    hours=119
    #var = [95, -0.5, 0.5, -0.5] #variability: [viability, inhibitor, rg, bi]
    var = [via/100, inh/100, rg/100, bi/100]
    x=np.array([a,b,c,d,e,f,g,h,i,j])
    us=np.array([])
    for j in range(10):
        us = np.append(us, x[j]*np.ones(12)) if us.size else x[j]*np.ones(12)
   
    sim(tcellmodel, hours, us, var)
    
    
    
def gluc_slider():
    grid = widgets.GridspecLayout(1, 10)

    time =['0-12 h','12-24 h','24-36 h','36-48 h','48-60 h','60-72 h','72-84 h','84-96 h','96-108 h','108-120 h']
    
    for i in range(1):
        for j in range(10):
            grid[i, j] = widgets.FloatSlider(value=1,min=0,max=2,step=0.1,orientation='vertical',description=time[j],handle_style = {'size':20}) 
    h=widgets.HTML(value='<{size}>Glucose Feed:</{size}>'.format(size='h4'))
    
    box_layout2 = widgets.Layout(display='flex',
                        flex_flow='column',
                        align_items='stretch',
                        border='solid',
                        width='100%')
    items = [h, grid]
    box2 = widgets.Box(children=items, layout=box_layout2)
    box2
    #hide_code()
    return box2, grid

def sim_ideal(var):
    [box, grid] = gluc_slider()
    hidden = hidden_widget(var)
    out = widgets.interactive_output(display_selected_plot, {'a':grid[0,0],'b':grid[0,1],'c':grid[0,2],'d':grid[0,3],'e':grid[0,4],'f':grid[0,5],'g':grid[0,6],'h':grid[0,7],'i':grid[0,8],'j':grid[0,9],
                                                             'via':hidden[0], 'inh':hidden[1],  'rg':hidden[2], 'bi':hidden[3]})
    display(box, out)

def gluc_slider_sim():
    grid = widgets.GridspecLayout(1, 10)

    time =['36-48 h','48-60 h','60-72 h','72-84 h','84-96 h','96-108 h','108-120 h']
    
    for i in range(1):
        for j in range(7):
            grid[i, j] = widgets.FloatSlider(value=1,min=0,max=2,step=0.1,orientation='vertical',description=time[j],handle_style = {'size':20}) 
    h=widgets.HTML(value='<{size}>Glucose Feed:</{size}>'.format(size='h4'))
    
    box_layout2 = widgets.Layout(display='flex',
                        flex_flow='column',
                        align_items='stretch',
                        border='solid',
                        width='100%')
    items = [h, grid]
    box2 = widgets.Box(children=items, layout=box_layout2)
    box2
    #hide_code()
    return box2, grid


def run_sim(N):
    #Simulation with a feed
    hours=119
    #var = [95, -0.5, 0.5, -0.5] #variability: [viability, inhibitor, rg, bi]
    X = np.array([[]])
    Y = np.array([])
    for i in range(N):
    
        var = [np.random.uniform(70,99)/100, np.random.uniform(-50,50)/100, 
               np.random.uniform(-50,50)/100, np.random.uniform(-50,50)/100]
        
        x=np.array([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
        us=np.array([])
        for j in range(10):
            us = np.append(us, x[j]*np.ones(12)) if us.size else x[j]*np.ones(12)
    
        
        [sx,sy,su] = control_tcell(tcellmodel, hours, us, var)
        sx = sx[0:36,:]
        newx=np.array([[]])
        for i in range(len(sx)):
            newx = np.hstack([newx[:],np.array([sx[i,2],sx[i,3],sx[i,5],sx[i,6]])]) if newx.size else np.array([sx[i,2],sx[i,3],sx[i,5],sx[i,6]])  
        X = np.vstack([X[:], newx]) if X.size else newx
        Y = np.vstack([Y,sy[-1]*sx[-1,3]]) if Y.size else sy[-1]*sx[-1,3]
    scalerX = preprocessing.StandardScaler().fit(X) #obtain data for scale X
    scalerY = preprocessing.StandardScaler().fit(Y) #obtain data for scale Y
    X2 = scalerX.transform(X)
    Y2 = scalerY.transform(Y)
    kernel = 1.0 * RBF(length_scale=1e-1, length_scale_bounds=(1e-2, 1e3)) + WhiteKernel(
        noise_level=1e-2, noise_level_bounds=(1e-10, 1e1))
    gpr = GaussianProcessRegressor(kernel=kernel, alpha=0.0)
    gpr.fit(X2, Y2)
    return gpr, scalerX, scalerY
    

def display_selected_plot_real(a,b,c,d,e,f,g,h,i,j,via,inh,rg,bi):
        #Simulation with a feed
    hours=119
    #var = [95, -0.5, 0.5, -0.5] #variability: [viability, inhibitor, rg, bi]
    var = [via/100, inh/100, rg/100, bi/100]
    x=np.array([a,b,c,d,e,f,g,h,i,j])
    us=np.array([])
    for j in range(10):
        us = np.append(us, x[j]*np.ones(12)) if us.size else x[j]*np.ones(12)
   
    sim(tcellmodel, hours, us, var)    

def display_real(d,e,f,g,h,i,j,via,inh,rg,bi):
        #Simulation with a feed
    hours=119
    #var = [95, -0.5, 0.5, -0.5] #variability: [viability, inhibitor, rg, bi]
    var = [via/100, inh/100, rg/100, bi/100]
    x=np.array([0.1,0.1,0.1,d,e,f,g,h,i,j])
    us=np.array([])
    for j in range(10):
        us = np.append(us, x[j]*np.ones(12)) if us.size else x[j]*np.ones(12) 
    sim_endpoint(tcellmodel, hours, us, var)
    
def sim_endpoint(tcellmodel, hours, us, variability):
    #plt.style.available
    plt.style.use('seaborn-v0_8') #use plot styles
    [sx,sy,su] = control_tcell(tcellmodel, hours, us, variability)

    
    #plot figures
    font = 30
    fig, axs = plt.subplots(1,2, figsize=(16, 6))
    
    axs[0].plot(su,color='tab:brown', linewidth=3)
    axs[0].set_xlabel('Time [h]', fontsize = font)
    axs[0].set_ylabel('Feed rate [mL/h]', fontsize = font,color='tab:brown')
    axs[0].yaxis.set_tick_params(labelsize=font)
    axs[0].xaxis.set_tick_params(labelsize=font);
    axs[0].tick_params(axis='y', labelcolor='tab:brown')
    axs[0].set_ylim([0, 2])
    y_std = abs(np.random.uniform(-0.3, 0.3))*sx[96,3]
    y_mean = y_std*sy[96] + sy[96]*sx[96,3]
    axs[1].errorbar(96, y_mean, y_std*1.5*sy[96], color='tab:blue' , markersize=8 )
    axs[1].plot(96,sy[96]*sx[96,3], marker='o', markersize=8 ,color='blue', linewidth=3)
    #axs[1].plot(sy,color='blue', linewidth=3)
    axs[1].set_xlabel('Time [h]', fontsize = font)
    axs[1].set_ylabel('Viable T-cells', fontsize = font,color='blue')
    axs[1].axhline(y=100e6, color="red", linestyle="--", label='Desired harvest')
    axs[1].axvline(x=96, color="red", linestyle="--", label='Desired harvest')
    axs[1].yaxis.set_tick_params(labelsize=font)
    axs[1].xaxis.set_tick_params(labelsize=font)
    axs[1].set_ylim([0, 1.5e8])
    axs[1].set_xlim([0, 120])
    #
    axs[1].tick_params(axis='y', labelcolor='blue')
    #axs[1].set_ylim([0, 1.5e8])
    handles, labels = axs[1].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axs[1].legend(by_label.values(), by_label.keys(), fontsize = font-10)

  
    #fig.delaxes(axs[2,2])
    fig.tight_layout(pad=0.8)
    clear_output(wait = True)
    #plt.pause(0.1)
    plt.show()
    return 

    
def sim_real(var):
    [box, grid] = gluc_slider_sim()
    hidden = hidden_widget(var)
    out = widgets.interactive_output(display_real, {'d':grid[0,0],'e':grid[0,1],'f':grid[0,2],'g':grid[0,3],'h':grid[0,4],'i':grid[0,5],'j':grid[0,6],  
                                                    'via':hidden[0], 'inh':hidden[1],  'rg':hidden[2], 'bi':hidden[3]})
    
    display(box, out)
    
    
    
    # [model, scalerX, scalerY] = run_sim(N)  
    # var = [98/100, -50/100, 0/100, 0/100]
    # x=np.array([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
    # us=np.array([])
    # for j in range(10):
    #     us = np.append(us, x[j]*np.ones(12)) if us.size else x[j]*np.ones(12)
    # [sx,sy,su] = control_tcell(tcellmodel, 119, us, var)
    # sx = sx[0:36,:]
    # newx=np.array([[]])
    # for i in range(len(sx)):
    #     newx = np.hstack([newx[:],np.array([sx[i,2],sx[i,3],sx[i,5],sx[i,6]])]) if newx.size else np.array([sx[i,2],sx[i,3],sx[i,5],sx[i,6]])  
    # X_t = scalerX.transform(newx.reshape(1, -1))
    # y_mean, y_std = model.predict(X_t, return_std=True)
    # y_mean = scalerY.inverse_transform(y_mean.reshape(1, -1)) 
    # y_std = scalerY.inverse_transform(y_std.reshape(1, -1))
    
    # display(box)
    # return y_mean, y_std 
    


    
    

def select_patients():
    patient = widgets.RadioButtons(
    options=['A', 'B', 'C'],
#     value='pineapple',
    description='Patients:',
    disabled=False
    )
    return patient

def hidden_widget(var):
    hidden=[]
    hidden.append(widgets.IntText(value=var[0], description='Hidden Value:', style={'description_width': '0px'}))
    hidden[0].layout.display = 'none'  # Hide the widget
    hidden.append(widgets.IntText(value=var[1], description='Hidden Value:', style={'description_width': '0px'}))
    hidden[1].layout.display = 'none'  # Hide the widget
    hidden.append(widgets.IntText(value=var[2], description='Hidden Value:', style={'description_width': '0px'}))
    hidden[2].layout.display = 'none'  # Hide the widget
    hidden.append(widgets.IntText(value=var[3], description='Hidden Value:', style={'description_width': '0px'}))
    hidden[3].layout.display = 'none'  # Hide the widget
    return hidden
    
#var = [95, -70, 0, 0] # variability: [viability %, inhibitor conc., growth rate%, start of the exhaustion%] 
#sim_ideal(var)
#var = [98, -50, 0, 0] # variability: [viability , inhibitor conc., growth rate, start of the exhaustion] [%]
#sim_real(var)
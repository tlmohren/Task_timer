import numpy as np
import pandas as pd
import datetime

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.dates 
from matplotlib.ticker import MultipleLocator, FuncFormatter, NullFormatter
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def tick(x,pos): 
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return days[int(x)]  
    
def hours_to_hhmm( arr ): 
    out_list = []
    for val in arr:
        if val< 10:
            test = '0' + str(val) +':00'
        else:
            test = str(val) + ':00'
        out_list.append(test)
    return( out_list ) 
 
def plot_week_tasks( ax_pl, df_week, label_dict, bool_legend=False ):
    days_in_week = df_week['date'].unique()
    for day in days_in_week : 
        bool_day = df_week['date'] == day 
        df_week_temp = df_week[bool_day] 


        for j,row in df_week_temp.iterrows():
            y = get_sec( row['start time'] )
            dy =  row['Duration (s)'] 
            label = row['Label']  
            ax_pl.bar( row['date'],dy, bottom = y, 
                      color = label_dict[label] , label = label ) 
 
    # set xlim 
    first_day = pd.to_datetime( days_in_week[0] )
    mon_day = first_day - datetime.timedelta( first_day.isocalendar()[2] -0.5 )
    sun_day = mon_day + datetime.timedelta( 7)     
    
    ax_pl.set_xlim( matplotlib.dates.date2num(mon_day)-0.2, matplotlib.dates.date2num(sun_day)+0.2 )

    # set ylim 
    ax_pl.set_ylim([6*3600,21*3600]) 

    # set xaxis ticks and ticklabels
    ax_pl.xaxis.set_major_locator(MultipleLocator(1))
    daysFmt = DateFormatter("%a")
    ax_pl.xaxis.set_major_formatter(daysFmt) 
    for tick in ax_pl.get_xticklabels():
        tick.set_rotation( 45 )
        
    # set yaxis ticks 
    ax_pl.invert_yaxis()
    hours = np.array([9,12,13,17,20])
    ax_pl.yaxis.set_ticks( hours*3600)
    ax_pl.yaxis.set_ticklabels( hours_to_hhmm(hours ) )
    ax_pl.yaxis.grid('on')
 
    # remove spines 
    ax_pl.spines['top'].set_visible(False)
    ax_pl.spines['right'].set_visible(False) 
    
    # set background transparent for when graphs overlap slightly 
    ax_pl.patch.set_visible(False)
    
    # set legend 
    if bool_legend:
        handles, labels = ax_pl.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax_pl.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5) )
    
    bbox_props = dict(boxstyle="round,pad=0.1", fc="w", ec="w", lw=2, alpha = 0.5) 
#     ax_pl.annotate( mon_day.date(), (mon_day,7*3600), 
    ax_pl.annotate( mon_day.date(), (mon_day+ datetime.timedelta(5),7*3600), 
                   va='top',ha='left' ,
                   bbox={'boxstyle':"round,pad=0.1", 'fc':"w",'ec':'w', 'alpha':0.9})
    
    
def plot_time_spent_weekly(ax_pl,df_pl, label_dict, bool_legend=False): 
    df_pl = df_pl.groupby('Label').sum()  
      
    # obtain labels sorted by duration 
    df_pl = df_pl.sort_values( by=[ 'Duration (s)'], ascending=False)
    labels = df_pl.index
         
    col_list = []
    for key in df_pl.index.tolist():
        col_list.append( label_dict[key] ) 

    ax_pl.barh( df_pl.index, df_pl['Duration (s)'],color=col_list )

    hours = np.array([0,2,4,6,8,10])
    ax_pl.xaxis.set_ticks( hours*3600)
    ax_pl.xaxis.set_ticklabels( hours_to_hhmm(hours ) )
    ax_pl.set_xlabel('Total time spent (hh:mm)') 

    # remove spines 
    ax_pl.spines['top'].set_visible(False)
    ax_pl.spines['right'].set_visible(False) 
    
    # put grid on major x-ticks
    ax_pl.xaxis.grid('on')
    
    # set background transparent for when graphs overlap slightly 
    ax_pl.patch.set_visible(False)
    
    # set legend 
    if bool_legend:
        handles, labels = ax_pl.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax_pl.legend(by_label.values(), 
                     by_label.keys(), 
                     loc='center left', 
                     bbox_to_anchor=(1, 0.5) )
        
    
def plot_time_spent_daily( ax_pl, df_week, label_dict, bool_legend=False): 
    
    # sum per date and labels
    df_pl = df_week.groupby(['date','Label']).sum().reset_index() 

    # obtain labels sorted by duration 
    df_pl = df_pl.sort_values( by=['date','Duration (s)'], ascending=False)
    labels = df_pl['Label'].unique()
    
    # set bar with  
    bar_w = 1/len(labels)  
 
    days_in_week = df_pl['date'].unique()
    
    for day in days_in_week:
        bool_day = df_pl['date'] == day 

        # find labels per day
        day_labels =  df_pl.loc[bool_day,'Label'].unique()  
        n_day = len(day_labels) 
        
        for i,label in enumerate(day_labels): 
            bool_label = df_pl['Label'] == label

            # center bars around date
            x =  matplotlib.dates.date2num(day)+ i*bar_w - n_day*bar_w/2   
            y = df_pl.loc[bool_day & bool_label,'Duration (s)'].iloc[0]  
            
            # plot individual bars 
            ax_pl.bar(x,y, width = bar_w,
                   align='edge',
                   color=label_dict[label],
                     label = label )


    # # set xaxis ticks and ticklabels
    ax_pl.xaxis.set_major_locator(MultipleLocator(1))
    daysFmt = DateFormatter("%a")
    ax_pl.xaxis.set_major_formatter(daysFmt) 
    for tick in ax_pl.get_xticklabels():
        tick.set_rotation( 45 )

    # # set yaxis ticks  
    hours = np.array([0,1,2,3,4,5,6,7,8 ])
    ax_pl.yaxis.set_ticks( hours*3600)
    ax_pl.yaxis.set_ticklabels( hours_to_hhmm(hours ) )
    ax_pl.yaxis.grid('on')
    
    # # set xlim 
    first_day = pd.to_datetime( days_in_week[0] )
    mon_day = first_day - datetime.timedelta( first_day.isocalendar()[2] -0.5 )
    sun_day = mon_day + datetime.timedelta( 7)    
#     ax_pl.set_xlim([mon_day,sun_day])  
    ax_pl.set_xlim( matplotlib.dates.date2num(mon_day)-0.2, matplotlib.dates.date2num(sun_day)+0.2 )
 
    ax_pl.set_ylim([0,df_pl['Duration (s)'].max()*1.2 ])
      
    ax_pl.spines['top'].set_visible(False)
    ax_pl.spines['right'].set_visible(False) 

    # set background transparent for when graphs overlap slightly 
    ax_pl.patch.set_visible(False)
     
    ax_pl.set_ylabel('Time spent per day (hh:mm)')
 
    if bool_legend:
        handles, labels = ax_pl.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax_pl.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5) )
  
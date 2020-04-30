import numpy as np
import pandas as pd
import datetime
import glob
import os
import sys
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.dates 
from matplotlib.ticker import MultipleLocator, FuncFormatter, NullFormatter
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

package_path = 'D:\code_projects\\task_timer'
sys.path.append(package_path)
import analyze_log_functions as alf
 
log_path = r'D:\\Mijn_documenten\\Dropbox\\D_notebook\\log_files\\'
log_files = glob.glob( log_path+ '*.csv')  

df = pd.DataFrame()
for file in log_files :
    df_temp = pd.read_csv( file, index_col=None, header=0)  
    df = df.append(df_temp ,sort=False)   
df.tail()

# remove items shorter than 60 seconds, probably resulting from testing with weird label names
bool_short_duration = df['Duration (s)'] < 60
df = df[~bool_short_duration]

# standardize labels, needed because of earlier inconsistent labeling 
change_labels = ['Timing feedforward','Timing feedforward project','FFtiming pend','Timing feedforw']
goal_label = 'FF timing pend'
for change_label in change_labels:
    bool_label = df['Label'] != change_label 
    df['Label'] = df['Label'].where(bool_label, goal_label ) 
    
change_labels = ['Code','Study']
goal_label = 'Coding study'
for change_label in change_labels:
    bool_label = df['Label'] != change_label 
    df['Label'] = df['Label'].where(bool_label, goal_label ) 
    
change_labels = ['Jobsearch']
goal_label = 'Job search'
for change_label in change_labels:
    bool_label = df['Label'] != change_label 
    df['Label'] = df['Label'].where(bool_label, goal_label ) 
 
# create week column, useful for later sorting 
df['date'] = pd.to_datetime(df['date'] )  
df['Duration (hh:mm:ss)'] = pd.to_timedelta(df['Duration (s)'],'s')
df.tail()
df['Week'] = df['date'].dt.strftime("%V")

# make colorscheme 
cols = np.array([[166,206,227], 
[31,120,180], 
[178,223,138], 
[51,160,44], 
[251,154,153], 
[227,26,28], 
[253,191,111], 
[255,127,0], 
[202,178,214], 
[106,61,154], 
[255,255,153]]) /255  

# find unique labels for color mapping
labels = df['Label'].unique()     
label_dict = {}
for label,col in zip(labels,cols): 
    label_dict[label] = col 

# find dataframe belonging to this week 
weeks = df['Week'].unique() 
bool_week = df['Week'] == weeks[-1]
df_week = df[bool_week].copy() 

# plot figure 
fig, ax = plt.subplots(2, 2, squeeze=False, figsize =(10,5))
 
# plot 3 subplots
alf.plot_week_tasks( ax[0,0], df_week, label_dict ) 
alf.plot_time_spent_weekly(ax[0,1], df_week, label_dict  )
alf.plot_time_spent_daily( ax[1,0], df_week, label_dict  ) 
  
# adjust layout 
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.4, hspace=None) 

# remove unused lower right subplot
ax[1,1].axes.remove()

plt.show() 
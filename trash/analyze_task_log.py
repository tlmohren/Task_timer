import numpy as np
import pandas as pd
import datetime
import glob
import os
import sys 
import matplotlib.pyplot as plt 

# load project functions
package_path = 'D:\code_projects\\task_timer'
sys.path.append(package_path)
import analyze_log_functions as alf

# make colorscheme 
cols = np.array([
    # [166,206,227], 
[31,120,180], 
[178,223,138], 
# [51,160,44], 
# [251,154,153], 
[227,26,28], 
# [253,191,111], 
[255,127,0], 
# [202,178,214], 
[106,61,154], 
[255,255,153]]) /255  



# load most recent log file 
log_path = r'D:\\Mijn_documenten\\Dropbox\\D_notebook\\log_files\\'
log_files = sorted(glob.glob( log_path+ '*.csv')) 
df= pd.read_csv( log_files[-1], index_col=None, header=0)  
  
# remove any task shorter than 1 minute, it's probably originated from a test
bool_short_duration = df['Duration (s)'] < 60
df = df[~bool_short_duration]

# modify data to useful format 
df['date'] = pd.to_datetime(df['date'] )  
df['Duration (hh:mm:ss)'] = pd.to_timedelta(df['Duration (s)'],'s') 

# find unique labels for color mapping
labels = df['Label'].unique()     
label_dict = {}
for label,col in zip(labels,cols): 
    label_dict[label] = col  

# plot figure 
fig, ax = plt.subplots(2, 2, squeeze=False, figsize =(10,5))
 
# create 3 subplots
alf.plot_week_tasks( ax[0,0], df, label_dict ) 
alf.plot_time_spent_weekly(ax[0,1], df, label_dict  )
alf.plot_time_spent_daily( ax[1,0], df, label_dict  ) 
alf.plot_week_text(ax[1,1], df, ['Flex pendulum','FEA wing','Lab business', 'FF timing pend'], 'Time worked')
  
# adjust layout 
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.4, hspace=None)  

plt.show() 
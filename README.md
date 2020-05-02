# task_timer
A minimal timer that logs tasks per label to csv files (one per week). The Jupyter notebook can be used to analyze log files, an example is shown below.
Currently data are logged not in this repository, see the Timer_Class, log_elsewhere = True.

Timer behavior:
- The timer counts down from 25 minutes (25:00).
- From 01:00 to 00:00, the background turns red incrementally.
- At time 00:00, the timer resets to 25:00, continuing counting down.
- The stop button resets the timer to 25:00
- The task, label, start-time, date, and time spent are logged when either time equals 00:00 or stop is pressed


Screenshot of the task timer| The jupyter notebook visualization of weekly data
:-------------------------:|:-------------------------:
<img src="./figs/task_timer_example.png" alt="drawing" style="width:300px;"/>|      <mimg src="./figs/week_analysis.png" alt="drawing" style="width:500px;"/>

## Background
The timer GUI is based on PyQt5. The executable version is built using pyinstaller, though it currently takes up over 30 Mb (and needs to be in the same folder as the Task_timer.py file?).

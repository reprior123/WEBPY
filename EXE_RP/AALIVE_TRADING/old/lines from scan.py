import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
from datetime import datetime
current_time = datetime.now().time()
print current_time.isoformat()

##    Mbox('Trade Alert', trademsg, 1)
'''

Note the styles are as follows:

##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | No 
##  6 : Cancel | Try Again | Continue

    14:03:02       EUR.USD      1 hour 1122.4000  -0.1637 negcrossmcd negnegmcd 
   18:48:54       EUR.USD      5 mins 1111.8750  0.0441 poscrossmcd posposmcd 
 20150604 23:59:58       EUR.USD       1 day 1127.8500  0.9753 poscrossmcd posposmcd 
 2015-06-05 07:45:00       USD.JPY     15 mins 124.4750  0.0022 poscrossmcd posposmcd 
   19:18:35       USD.JPY     30 secs 125.5275  0.0024 poscrossmcd posposmcd 
   19:20:35       USD.JPY       1 min 125.5425  0.0035 poscrossmcd posposmcd 
 2015-06-04 17:00:00       USD.JPY      1 hour 124.6000  0.0323 poscrossmcd posposmcd 
   18:19:17       USD.JPY      5 mins 125.5275  -0.0008 negcrossmcd negnegmcd 
 20150519 23:59:58       USD.JPY       1 day 120.2150  0.0328 poscrossmcd posposmcd 
   14:32:44       AUD.USD     15 mins 765.4000  -0.0057 negcrossmcd negnegmcd 
   19:19:07       AUD.USD     30 secs 762.3250  -0.0369 negcrossmcd negnegmcd 
   19:25:09       AUD.USD       1 min 762.4500  -0.0095 negcrossmcd negnegmcd 
 2015-06-04 03:00:00       AUD.USD      1 hour 774.9000  -0.1814 negcrossmcd negnegmcd 
   19:09:04       AUD.USD      5 mins 762.8500  0.0261 poscrossmcd posposmcd 
 20150526 23:59:58       AUD.USD       1 day 778.9000  -0.3965 negcrossmcd negnegmcd 
   12:17:15            NQ     15 mins 4482.3750  -1.2673 negcrossmcd negnegmcd 
   19:21:46            NQ     30 secs 4480.8750  0.0683 poscrossmcd posposmcd 
   19:20:15            NQ       1 min 4480.3750  0.1040 poscrossmcd posposmcd 
 2015-06-04 08:00:00            NQ      1 hour 4517.0000  -0.1637 negcrossmcd negnegmcd 
   19:09:12            NQ      5 mins 4482.1250  0.0846 poscrossmcd posposmcd 
 20150413 23:59:58            NQ       1 day 4415.7500  0.5294 poscrossmcd posposmcd 
   12:02:14            ES     15 mins 2096.3750  -0.1185 negcrossmcd negnegmcd 
   19:27:50            ES     30 secs 2093.6250  0.0482 poscrossmcd posposmcd 
   19:20:17            ES       1 min 2093.3750  0.0003 poscrossmcd posposmcd 
 2015-06-04 09:00:00            ES      1 hour 2109.2500  -0.3755 negcrossmcd negnegmcd 
   19:09:14            ES      5 mins 2094.1250  0.1471 poscrossmcd posposmcd 
 20150409 23:59:58            ES       1 day 2075.2500  0.1870 poscrossmcd posposmcd 

grep for most recent....
time now = x
if bar time is within 2 minutes, sound alarm and show bar
'''

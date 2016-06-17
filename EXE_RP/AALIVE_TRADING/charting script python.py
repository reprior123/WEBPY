'''Historical Intraday Stock Price Data with Python
By popular request, this post will present how to acquire intraday stock data from google finance using python. The general structure of the code is pretty simple to understand. First a request url is created and sent. The response is then read by python to create an array or matrix of the financial data and a vector of time data. This array is created with the help of the popular Numpy package that can be downloaded from here. Then in one if-statement, the time data is then restructured into a proper unix time format and translated to a more familiar date string for each financial data point. The translated time vector is then joined with the financial array to produce a single easy to work with financial time series array. Since Numpy has been ported to Python 3, the code I wrote should be compatibile with both Python 2.X and 3.X. Here it is:

'''
import urllib2
import urllib
import numpy as np
from datetime import datetime
urldata = {}
 
urldata['q'] = ticker = 'JPM'       # stock symbol
urldata['x'] = 'NYSE'               # exchange symbol
urldata['i'] = '60'                 # interval
urldata['p'] = '1d'                 # number of past trading days (max has been 15d)
urldata['f'] = 'd,o,h,l,c,v'        # requested data d is time, o is open, c is closing, h is high, l is low, v is volume
 
url_values = urllib.urlencode(urldata)
url = 'http://www.google.com/finance/getprices'
full_url = url + '?' + url_values
req = urllib2.Request(full_url)
response = urllib2.urlopen(req).readlines()
getdata = response
del getdata[0:7]
numberoflines = len(getdata)
returnMat = np.zeros((numberoflines, 5))
timeVector = []
 
index = 0
for line in getdata:
    line = line.strip('a')
    listFromLine = line.split(',')
    returnMat[index,:] = listFromLine[1:6]
    timeVector.append(int(listFromLine[0]))
    index += 1
 
# convert Unix or epoch time to something more familiar
for x in timeVector:
    if x > 500:
        z = x
        timeVector[timeVector.index(x)] = datetime.fromtimestamp(x)
    else:
        y = z+x*60 # multiply by interval
        timeVector[timeVector.index(x)] = datetime.fromtimestamp(y)
 
tdata = np.array(timeVector)
time = tdata.reshape((len(tdata),1))
intradata = np.concatenate((time, returnMat), axis=1) # array of all data with the properly formated times
'''Here is a quick example of what can be done with this data in Python 2.7
using the Numpy and matplotlib libraries.
It is nothing fancy, just the usual moving average computations
and some styling preferences.

The python code that was used to create the plot above can is posted below:
'''
### Example on how to use and plot this data
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
 
def relative_strength(prices, n=14):
 
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
 
    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter
 
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
 
        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
 
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
 
    return rsi
 
def moving_average(p, n, type='simple'):
    """
    compute an n period moving average.
 
    type is 'simple' | 'exponential'
 
    """
    p = np.asarray(p)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))
 
    weights /= weights.sum()
 
 
    a =  np.convolve(p, weights, mode='full')[:len(p)]
    a[:n] = a[n]
    return a
 
def moving_average_convergence(p, nslow=26, nfast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(p) arrays
    """
    emaslow = moving_average(p, nslow, type='exponential')
    emafast = moving_average(p, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow
 
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
 
textsize = 9
left, width = 0.1, 0.8
rect1 = [left, 0.7, width, 0.2]
rect2 = [left, 0.3, width, 0.4]
rect3 = [left, 0.1, width, 0.2]
 
 
fig = plt.figure(facecolor='white')
axescolor  = '#f6f6f6'  # the axies background color
 
ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax2t = ax2.twinx()
ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
 
### plot the relative strength indicator
prices = intradata[:,4]
rsi = relative_strength(prices)
t = intradata[:,0]
fillcolor = 'darkgoldenrod'
 
ax1.plot(t, rsi, color=fillcolor)
ax1.axhline(70, color=fillcolor)
ax1.axhline(30, color=fillcolor)
ax1.fill_between(t, rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
ax1.fill_between(t, rsi, 30, where=(rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
ax1.set_ylim(0, 100)
ax1.set_yticks([30,70])
ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
ax1.set_title('%s daily'%ticker)
 
### plot the price and volume data
low = intradata[:,3]
high = intradata[:,2]
 
deltas = np.zeros_like(prices)
deltas[1:] = np.diff(prices)
up = deltas>0
ax2.vlines(t[up], low[up], high[up], color='black', label='_nolegend_')
ax2.vlines(t[~up], low[~up], high[~up], color='black', label='_nolegend_')
ma5 = moving_average(prices, 5, type='simple')
ma50 = moving_average(prices, 50, type='simple')
 
linema5, = ax2.plot(t, ma5, color='blue', lw=2, label='MA (5)')
linema50, = ax2.plot(t, ma50, color='red', lw=2, label='MA (50)')
 
props = font_manager.FontProperties(size=10)
leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
leg.get_frame().set_alpha(0.5)
 
volume = (intradata[:,4]*intradata[:,5])/1e6  # dollar volume in millions
vmax = volume.max()
poly = ax2t.fill_between(t, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
ax2t.set_ylim(0, 5*vmax)
ax2t.set_yticks([])
 
### compute the MACD indicator
fillcolor = 'darkslategrey'
nslow = 26
nfast = 12
nema = 9
emaslow, emafast, macd = moving_average_convergence(prices, nslow=nslow, nfast=nfast)
ema9 = moving_average(macd, nema, type='exponential')
ax3.plot(t, macd, color='black', lw=2)
ax3.plot(t, ema9, color='blue', lw=1)
ax3.fill_between(t, macd-ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
 
 
ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)'%(nfast, nslow, nema), va='top',
         transform=ax3.transAxes, fontsize=textsize)
 
# turn off upper axis tick labels, rotate the lower ones, etc
for ax in ax1, ax2, ax2t, ax3:
    if ax!=ax3:
        for label in ax.get_xticklabels():
            label.set_visible(False)
    else:
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('right')
 
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
 
class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)
 
    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)
 
# at most 5 ticks, pruning the upper and lower so they don't overlap
# with other ticks
ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))
 
plt.show()
##########################
'''
The line down = -seed[seed<0 -="-" ... the="the">0:
is not correct. 
You are right. It should be:

down = -seed[seed<0].sum()/n

I'll modify it as soon as I can! Thanks for the heads up.

Desert MonkSeptember 10, 2012 at 10:59 PM
Sorry to bring bad news... There are more errors... ax1.text(0.6, 0.1, '<30 ... label='_nolegend_')
ax2.vlines(t[~up], low[~up], high[~up], color='black', label='_nolegend_') 

It appears a few lines have been mangled during posting.

Miguel WongSeptember 11, 2012 at 1:28 PM
After playing around a bit Blogger, I think the code is finally fixed. It gets annoying sometimes when Blogger tries to be too helpful.

Desert MonkSeptember 11, 2012 at 11:39 PM
This is a useful bit of code. Thank you for sharing.

Hi, getting error with fill_between()

Traceback (most recent call last):
File "first.py", line 148, in 
ax1.fill_between(t, rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
File "/usr/lib/python2.7/site-packages/matplotlib/axes.py", line 6777, in fill_between
y1 = ma.masked_invalid(self.convert_yunits(y1))
File "/usr/lib/python2.7/site-packages/numpy/ma/core.py", line 2241, in masked_invalid
condition = ~(np.isfinite(a))
TypeError: ufunc 'isfinite' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''
could you check?

Bhoomi DesaiJuly 7, 2015 at 7:35 AM
Thanks for sharing such a wonderful piece of information, really appreciate. Keep informing... Forex Trading tips
'''

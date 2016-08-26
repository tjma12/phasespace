from gwpy.timeseries import TimeSeriesDict
from gwsumm.html.markup import page
import phasespace as ps
import numpy as np

startgps = 1128411017
duration = 300 
startgps2 = 1128453317 
outdir = '/path/to/save/images/'
chans = np.loadtxt('ASC_channels.txt',dtype=str)

time1 = TimeSeriesDict.fetch(np.ravel(chans),startgps,startgps+duration,verbose=True)
time2 = TimeSeriesDict.fetch(np.ravel(chans),startgps2,startgps2+duration,verbose=True)

page = page()
page.init(css='style.css')
page.div(class_='banner')
page.div(class_='title')
page.strong('Phase space plots: %s - %s'% (startgps,startgps2))
page.div.close()
page.div.close()

page.ul(style='list-style-type:none')
for chan1, chan2 in chans:
    outfile = '%s-%s-%d-%d.png' % (chan1.replace(':','-'),chan2.replace(':','-'),startgps,startgps2)
    pit_yaw = ps.phase_space(y_ts=time1[chan1],x_ts=time1[chan2],
                         y_ts_comp=time2[chan1],x_ts_comp=time2[chan2])
    scatterhist = pit_yaw.plot_2d_scatter_hist_comparison(timer=32,median=True,flip=True)
    scatterhist.savefig(outdir+outfile)
    page.li()
    page.img(src='%s' % outfile)
    page.li.close()

page.ul.close()

with open(outdir+'index.html','w') as f:
    f.write(str(page))



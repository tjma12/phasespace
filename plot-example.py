from gwpy.timeseries import TimeSeriesDict
import phasespace as ps

chan1 = 'H1:ASC-DSOFT_P_OUT_DQ'
chan2 = 'H1:ASC-DSOFT_Y_OUT_DQ'
startgps = 1128411017
duration = 300 
startgps2 = 1128453317 

time1 = TimeSeriesDict.fetch([chan1,chan2],startgps,startgps+duration,verbose=True)
time2 = TimeSeriesDict.fetch([chan1,chan2],startgps2,startgps2+duration,verbose=True)

pit_yaw = ps.phase_space(y_ts=time1[chan1],x_ts=time1[chan2],
                         y_ts_comp=time2[chan1],x_ts_comp=time2[chan2])
scatterhist = pit_yaw.plot_2d_scatter_hist_comparison(timer=32,median=False,flip=True)
scatterhist.savefig('test.png')

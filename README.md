# phasespace
A set of tools to analyze two GWpy time series in phase space.

A simple example to plot a 2D scatterplot can be found in `plot-example.py`. Replace the 
output file appropriately, source a GWpy user environment, and run `python plot-example.py` 
to generate a plot.

Parsing the lines of this example that use the phasespace.py module:

Initialize a phase space object using the TimeSeriesDict defined above:

`pit_yaw = ps.phase_space(y_ts=time1[chan1],x_ts=time1[chan2],y_ts_comp=time2[chan1],x_ts_comp=time2[chan2])`

This object now has a number of methods that can be called. To generate a 2D plot from these 
time series and save it to disk:

```scatterhist = pit_yaw.plot_2d_scatter_hist_comparison(timer=32,median=False,flip=True)
scatterhist.savefig('/path/to/file.png')```

The timer argument, `timer=32`, determines how often to plot a data point. Since the example channels are 
sampled at 2048 Hz, I decided I only wanted every 32nd point. 

If the median argument is set to `median=True`, the code with calculate the median along each 
axis for the first set of data points (`time1` in this case) and display them on the plot.

Enabling `flip=True` will change the order in which the time series are plotted, the default is to 
plot the second set of data points on top of the first set of data points.

---

A second example is provided in `several-alignment-chans.py`, which loops over a text file 
containing pairs of alignment channels and writes them to a directory along with some basic 
HTML to display them. The plotting code is all the same, this script is simply a wrapper around 
the plotting code that uses GWpy's html module for a simple display.

If this is going to be used with a different set of channels, replace the `ASC_channels.txt` 
file with a new file in the same format. 


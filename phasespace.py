from gwpy.timeseries import TimeSeries
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse
import logging
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plt.rc('axes', labelsize=12.0)
plt.rc('legend', fontsize=10.0)
plt.rc('xtick', labelsize=10.0)
plt.rc('ytick', labelsize=10.0)
plt.rc('figure', dpi=300)

class phase_space:
    """
    Takes 2 gwpy TimeSeries objects as inputs and provides functionality
    to plot them in a 2D phase space.

    Parameters
    ----------


    Returns
    -------



    Examples
    --------

    
    """
    def __init__(self,y_ts,x_ts,y_ts_comp=None,x_ts_comp=None):
        self.ydata = y_ts
        self.xdata = x_ts
        self.ydata_comp = y_ts_comp
        self.xdata_comp = x_ts_comp

    def quadrants(self):
        y_median = self.ydata.median().value
        x_median = self.xdata.median().value
        total = float(self.ydata.size)
        Q1 = np.array((self.ydata.value >= y_median) & 
                      (self.xdata.value >= x_median)).sum()/total
        Q2 = np.array((self.ydata.value >= y_median) & 
                      (self.xdata.value < x_median)).sum()/total
        Q3 = np.array((self.ydata.value < y_median) & 
                      (self.xdata.value < x_median)).sum()/total
        Q4 = np.array((self.ydata.value < y_median) & 
                      (self.xdata.value >= x_median)).sum()/total
        return Q1, Q2, Q3, Q4

    def quadrants_comp(self):
        y_median = self.ydata.median().value
        x_median = self.xdata.median().value
        total = float(self.ydata_comp.size)
        Q1 = np.array((self.ydata_comp.value >= y_median) &
                      (self.xdata_comp.value >= x_median)).sum()/total
        Q2 = np.array((self.ydata_comp.value >= y_median) &
                      (self.xdata_comp.value < x_median)).sum()/total
        Q3 = np.array((self.ydata_comp.value < y_median) &
                      (self.xdata_comp.value < x_median)).sum()/total
        Q4 = np.array((self.ydata_comp.value < y_median) &
                      (self.xdata_comp.value >= x_median)).sum()/total
        return Q1, Q2, Q3, Q4

    def plot_2d_scatter(self,timer=16):
        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(self.xdata.value[::timer],self.ydata.value[::timer],
                   s=5,c='c',alpha=0.8,edgecolors='none')
        ax.axhline(self.ydata.median().value,ls='dashed',c='k')
        ax.axvline(self.xdata.median().value,ls='dashed',c='k')
        ax.grid(which='major',axis='both')
        ax.set_xlabel(self.xdata.channel.name.replace(':','-').replace('_','-'))
        ax.set_ylabel(self.ydata.channel.name.replace(':','-').replace('_','-'))

        Q1, Q2, Q3, Q4 = self.quadrants()
        ax.annotate('%.2f' % Q1, xy=(0.95,0.95), xycoords='axes fraction',ha='center',va='center')
        ax.annotate('%.2f' % Q2, xy=(0.05,0.95), xycoords='axes fraction',ha='center',va='center')
        ax.annotate('%.2f' % Q3, xy=(0.05,0.05), xycoords='axes fraction',ha='center',va='center')
        ax.annotate('%.2f' % Q4, xy=(0.95,0.05), xycoords='axes fraction',ha='center',va='center')
        return fig

    def plot_2d_scatter_comparison(self,timer=32):
        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(self.xdata.value[::timer],self.ydata.value[::timer],
                   s=5,c='c',alpha=0.8,edgecolors='none')
        ax.axhline(self.ydata.median().value,ls='dashed',c='k',alpha=0.6)
        ax.axvline(self.xdata.median().value,ls='dashed',c='k',alpha=0.6)
        ax.grid(which='major',axis='both')
        ax.set_xlabel(self.xdata.channel.name.replace(':','-').replace('_','-'))
        ax.set_ylabel(self.ydata.channel.name.replace(':','-').replace('_','-'))
        ax.scatter(self.xdata_comp.value[::timer],self.ydata_comp.value[::timer],
                   s=5,c='g',alpha=0.8,edgecolors='none')

        Q1, Q2, Q3, Q4 = self.quadrants()
        Q1_comp, Q2_comp, Q3_comp, Q4_comp = self.quadrants_comp()
        ax.annotate('%.2f - %.2f' % (Q1,Q1_comp), xy=(0.90,0.95), xycoords='axes fraction',
                    ha='center',va='center')
        ax.annotate('%.2f - %.2f' % (Q2,Q2_comp), xy=(0.08,0.95), xycoords='axes fraction',
                    ha='center',va='center')
        ax.annotate('%.2f - %.2f' % (Q3,Q3_comp), xy=(0.08,0.05), xycoords='axes fraction',
                    ha='center',va='center')
        ax.annotate('%.2f - %.2f' % (Q4,Q4_comp), xy=(0.90,0.05), xycoords='axes fraction',
                    ha='center',va='center')
        return fig


    def plot_2d_scatter_hist_comparison(self,timer=32,median=False):
        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(self.xdata.value[::timer],self.ydata.value[::timer],
                   s=5,c='c',alpha=0.8,edgecolors='none')
        ax.grid(which='major',axis='both')
        ax.set_xlabel(self.xdata.channel.name.replace(':','-').replace('_','-'))
        ax.set_ylabel(self.ydata.channel.name.replace(':','-').replace('_','-'))
        ax.scatter(self.xdata_comp.value[::timer],self.ydata_comp.value[::timer],
                   s=5,c='g',alpha=0.8,edgecolors='none')

        ax.annotate(str(self.xdata.times.value[0]),xy=(1.2,1.5),xycoords='axes fraction',
                    ha='center',va='center',color='blue')
        ax.annotate(str(self.xdata_comp.times.value[0]),xy=(1.2,1.4),xycoords='axes fraction',
                    ha='center',va='center',color='green')
        ax.annotate('Duration: ' + str(self.xdata.duration.value), xy=(1.2,1.3),
                    xycoords='axes fraction',ha='center',va='center')
 
        divider = make_axes_locatable(ax)
        axHistx = divider.append_axes("top", size=1.6, pad=0.2, sharex=ax)
        axHisty = divider.append_axes("right", size=1.6, pad=0.2, sharey=ax)
        bins = 50.
        axHistx.hist(self.xdata.value[::timer],bins=bins,histtype='step')
        axHistx.grid(which='major',axis='both')
        axHistx.set_ylabel('Counts')
        axHistx.hist(self.xdata_comp.value[::timer],bins=bins,histtype='step')

        axHisty.hist(self.ydata.value[::timer],bins=bins,histtype='step',orientation='horizontal')
        axHisty.grid(which='major',axis='both')
        axHisty.set_xlabel('Counts')
        axHisty.hist(self.ydata_comp.value[::timer],bins=bins,histtype='step',orientation='horizontal')

        if median:
            Q1, Q2, Q3, Q4 = self.quadrants()
            Q1_comp, Q2_comp, Q3_comp, Q4_comp = self.quadrants_comp()
            ax.annotate('%.2f - %.2f' % (Q1,Q1_comp), xy=(0.90,0.95), xycoords='axes fraction',
                        ha='center',va='center')
            ax.annotate('%.2f - %.2f' % (Q2,Q2_comp), xy=(0.10,0.95), xycoords='axes fraction',
                        ha='center',va='center')
            ax.annotate('%.2f - %.2f' % (Q3,Q3_comp), xy=(0.10,0.05), xycoords='axes fraction',
                        ha='center',va='center')
            ax.annotate('%.2f - %.2f' % (Q4,Q4_comp), xy=(0.90,0.05), xycoords='axes fraction',
                        ha='center',va='center')
            ax.axhline(self.ydata.median().value,ls='dashed',c='k',alpha=0.6)
            ax.axvline(self.xdata.median().value,ls='dashed',c='k',alpha=0.6)
            axHistx.axvline(self.xdata.median().value,ls='dashed',c='k',alpha=0.6)
            axHisty.axhline(self.ydata.median().value,ls='dashed',c='k',alpha=0.6)

        plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),visible=False)
        return fig

    def plot_2d_scatter_hist(self,timer=16):
        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(self.xdata.value[::timer],self.ydata.value[::timer],
                   s=5,c='c',alpha=0.8,edgecolors='none')
        ax.axhline(self.ydata.median().value,ls='dashed',c='k')
        ax.axvline(self.xdata.median().value,ls='dashed',c='k')
        ax.grid(which='major',axis='both')
        ax.set_xlabel(self.xdata.channel.name.replace(':','-').replace('_','-'))
        ax.set_ylabel(self.ydata.channel.name.replace(':','-').replace('_','-'))

        Q1, Q2, Q3, Q4 = self.quadrants()
        ax.annotate('%.2f' % Q1, xy=(0.95,0.95), xycoords='axes fraction',ha='center',va='center')
        ax.annotate('%.2f' % Q2, xy=(0.05,0.95), xycoords='axes fraction',ha='center',va='center')
        ax.annotate('%.2f' % Q3, xy=(0.05,0.05), xycoords='axes fraction',ha='center',va='center')
        ax.annotate('%.2f' % Q4, xy=(0.95,0.05), xycoords='axes fraction',ha='center',va='center')

        divider = make_axes_locatable(ax)
        axHistx = divider.append_axes("top", size=1.6, pad=0.1, sharex=ax)
        axHisty = divider.append_axes("right", size=1.6, pad=0.1, sharey=ax)
        bins = 50.
        axHistx.hist(self.xdata.value[::timer],bins=bins,histtype='step')
        axHistx.grid(which='major',axis='both')
        axHistx.axvline(self.xdata.median().value,ls='dashed',c='k')
        axHistx.set_ylabel('Counts')

        axHisty.hist(self.ydata.value[::timer],bins=bins,histtype='step',orientation='horizontal')
        axHisty.grid(which='major',axis='both')
        axHisty.axhline(self.ydata.median().value,ls='dashed',c='k')
        axHisty.set_xlabel('Counts')

        plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),visible=False)
        return fig


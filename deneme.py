'''
How to create a simple Taylor diagram

A first example of how to create a simple Taylor diagram given one set of
reference observations and multiple model predictions for the quantity.
The Python code is kept to a minimum.

This example shows how to calculate the required statistics and produce
the Taylor diagram.

All functions in the Skill Metrics library are designed to only work with
one-dimensional arrays, e.g. time series of observations at a selected
location. The one-dimensional data are read in as dictionaries via a
pickle file: ref['data'], pred1['data'], pred2['data'],
and pred3['data']. The plot is written to a file in Portable Network
Graphics (PNG) format.

The reference data used in this example are cell concentrations of a
phytoplankton collected from cruise surveys at selected locations and
time. The model predictions are from three different simulations that
have been space-time interpolated to the location and time of the sample
collection. Details on the contents of the dictionary (once loaded) can
be obtained by simply executing the following two statements

>> key_to_value_lengths = {k:len(v) for k, v in ref.items()}
>> print key_to_value_lengths
{'units': 6, 'longitude': 57, 'jday': 57, 'date': 57, 'depth': 57,
'station': 57, 'time': 57, 'latitude': 57, 'data': 57}

Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com

Created on Dec 3, 2016

@author: prochford@thesymplectic.com
'''

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pickle
import skill_metrics as sm
from sys import version_info
import pandas as pd

def load_obj(name):
    # Load object from file in pickle format
    if version_info[0] == 2:
        suffix = 'pkl'
    else:
        suffix = 'pkl3'

    with open(name + '.' + suffix, 'rb') as f:
        return pickle.load(f)  # Python2 succeeds


class Container(object):

    def __init__(self, pred1, pred2, pred3, ref):
        self.pred1 = pred1
        self.pred2 = pred2
        self.pred3 = pred3
        self.ref = ref


if __name__ == '__main__':
    # Set the figure properties (optional)
    rcParams["figure.figsize"] = [8.0, 6.4]
    rcParams['lines.linewidth'] = 1  # line width for plots
    rcParams.update({'font.size': 12})  # font size of axes text

    # Close any previously open graphics windows
    # ToDo: fails to work within Eclipse
    plt.close('all')

    # Read data from pickle file
    data = load_obj('taylor_data')

    filep = pd.read_excel("TahminSon_Grafik.xlsx", sheet_name="pol-reg")
    filer = pd.read_excel("TahminSon_Grafik.xlsx", sheet_name="random forest")
    filek = pd.read_excel("TahminSon_Grafik.xlsx", sheet_name="KNN")
    fileg = pd.read_excel("TahminSon_Grafik.xlsx", sheet_name="GBM")
    filed = pd.read_excel("TahminSon_Grafik.xlsx", sheet_name="DTree")

    # filep["kayma-tahmin"]
    # filep["Fs(kay) gercek"]
    files = [filep,filer,filek,fileg,filed]
    names = [("kayma-tahmin", "Fs(kay) gercek", np.arange(0, 0.1, 0.01), 1.5),
             ("devrilme-tahmin", "Fs(dev) gercek", np.arange(0, 0.1, 0.01), 3),
             ("toptan goc-tahmin", "Fs(topgoc) gercek", np.arange(0, 0.1, 0.01), 1)]
    names = [("kayma-tahmin", "Fs(kay) gercek", [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15], [0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.1], 1.5),
             ("devrilme-tahmin", "Fs(dev) gercek", [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2], [2.5,2.51,2.52,2.53,2.54,2.55,2.56,2.57,2.58,2.59,2.6,2.61,2.62,2.63,2.64,2.65,2.66,2.67,2.68,2.69,2.7], 3),
             ("toptan goc-tahmin", "Fs(topgoc) gercek", [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15],[0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6], 1)]


    names2 = [("kayma-tahmin", "Fs(kay) gercek", [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15], 1.5),
             ("devrilme-tahmin", "Fs(dev) gercek", [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2], 3),
             ("toptan goc-tahmin", "Fs(topgoc) gercek", [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15], 1)]
    for name, f in zip(names, files) :
        taylor_stats1 = sm.taylor_statistics(filep[name[0]], filep[name[1]], 'data')
        taylor_stats2 = sm.taylor_statistics(filer[name[0]], filer[name[1]], 'data')
        taylor_stats3 = sm.taylor_statistics(filek[name[0]], filek[name[1]], 'data')
        taylor_stats4 = sm.taylor_statistics(fileg[name[0]], fileg[name[1]], 'data')
        taylor_stats5 = sm.taylor_statistics(filed[name[0]], filed[name[1]], 'data')

        # Calculate statistics for Taylor diagram
        # The first array element (e.g. taylor_stats1[0]) corresponds to the
        # reference series while the second and subsequent elements
        # (e.g. taylor_stats1[1:]) are those for the predicted series.
        # taylor_stats1 = sm.taylor_statistics(data.pred1["data"], data.ref["data"], 'data')
        # taylor_stats2 = sm.taylor_statistics(data.pred2, data.ref, 'data')
        # taylor_stats3 = sm.taylor_statistics(data.pred3, data.ref, 'data')

        # Store statistics in arrays
        sdev = np.array([taylor_stats1['sdev'][0], taylor_stats1['sdev'][1],
                         taylor_stats2['sdev'][1], taylor_stats3['sdev'][1],
                         taylor_stats4['sdev'][1], taylor_stats5['sdev'][1]])
        crmsd = np.array([taylor_stats1['crmsd'][0], taylor_stats1['crmsd'][1],
                          taylor_stats2['crmsd'][1], taylor_stats3['crmsd'][1],
                          taylor_stats4['crmsd'][1], taylor_stats5['crmsd'][1]])
        ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats1['ccoef'][1],
                          taylor_stats2['ccoef'][1], taylor_stats3['ccoef'][1],
                          taylor_stats4['ccoef'][1], taylor_stats5['ccoef'][1]])

        '''
        Produce the Taylor diagram
    
        Note that the first index corresponds to the reference series for 
        the diagram. For example sdev[0] is the standard deviation of the 
        reference series and sdev[1:4] are the standard deviations of the 
        other 3 series. The value of sdev[0] is used to define the origin 
        of the RMSD contours. The other values are used to plot the points 
        (total of 3) that appear in the diagram.
    
        For an exhaustive list of options to customize your diagram, 
        please call the function at a Python command line:
        >> taylor_diagram
        '''
        label = ['Observation','Pol-Reg', 'Rand.Forest', 'KNN','GBM','DTree']
        labelcol = ['red','blue','cyan','green','yellow','orange']

        '''
        Produce the Taylor diagram
        Label the points and change the axis options for SDEV, CRMSD, and CCOEF.
        Increase the upper limit for the SDEV axis and rotate the CRMSD contour 
        labels (counter-clockwise from x-axis). Exchange color and line style
        choices for SDEV, CRMSD, and CCOEFF variables to show effect. Increase
        the line width of all lines. Suppress axes titles and add a legend.
        For an exhaustive list of options to customize your diagram, 
        please call the function at a Python command line:
        >> taylor_diagram
        '''
        # sm.taylor_diagram(sdev, crmsd, ccoef, markerLabel=label,
        #                   markerLabelColor='r',
        #                   markerColor='r', markerLegend='on',
        #                    tickRMSangle=135.0,
        #                   colRMS='m', styleRMS=':', widthRMS=2.0,
        #                   titleRMS='on',
        #                   axismax=1.5, colSTD='b', styleSTD='-.',
        #                   widthSTD=1.5, titleSTD='on',
        #                   colCOR='k', styleCOR='--', widthCOR=1.0,
        #                   titleCOR='on',markerObs=".")

        sm.taylor_diagram(sdev, crmsd, ccoef, markerLabel=label,
                          markerLabelColor='r',markerSize=10,
                          markerColor='r', markerLegend='on',
                           tickRMSangle=90.0,
                          colRMS='m', styleRMS=':', widthRMS=0.8,
                          titleRMS='on',titleSTD='on',titleCOR='on',titleOBS='on',
                          axismax=name[4], colSTD='b', styleSTD='-.',
                          widthSTD=1.0,
                          colCOR='k', styleCOR='--', widthCOR=1.0,
                           markerObs = ".",
                          tickRMS=name[2],
                          tickSTD=name[3],
                          rincSTD=0.1)

        # Write plot to file
        #plt.savefig("result"+name[0]+".png", dpi=200)

        # Show plot
        plt.show()
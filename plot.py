# -*- coding: utf-8 -*-
'''グラフプロット処理部分'''
import csv

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from PyQt5.QtWidgets import QSizePolicy
from base_func.calc import normarize_data
from base_func.base_plot import PlotCanvas

PLOTMODE_1 = '1 graph in 1 figure'
PLOTMODE_2 = 'all graph in 1 figure'


class PlotGraphCanvas(PlotCanvas):

    def plot(self, file_list, output_directly, plot_style, legend_plot, legend, legend_loc, line_plot, normarize, ylog):
        '''plot data'''

        if legend_plot:
            while(len(file_list) > len(legend)):
                legend.append('')
        for file_num, path in enumerate(file_list):
            xy_list = np.loadtxt(path, dtype='float')
            x_list = xy_list[:,0]
            y_list = xy_list[:,1]
            if normarize:
                if ylog:
                    y_list = normarize_data(y_list, log=True)
                else:
                    y_list = normarize_data(y_list)
            if line_plot:
                self.plot_canvas.plot(x_list, y_list, linewidth=1)
            else:
                self.plot_canvas.plot(
                    x_list, y_list, linestyle='None', marker='o')
            self.draw()
            # 出力
            if plot_style == PLOTMODE_1:
                if legend_plot:
                    self.plot_canvas.legend(legend[file_num], loc=legend_loc, fontsize=35, prop={
                        'size': 9}, labelspacing=0)
                self.fig.savefig(output_directly + '/' + str(path).split('/')
                                 [-1].split('.')[0] + '.png')
                self.plot_canvas.clear()
        if plot_style == PLOTMODE_2:
            if legend_plot:
                self.plot_canvas.legend(legend, loc=legend_loc, fontsize=35, prop={
                    'size': 9}, labelspacing=0)
            self.fig.savefig(output_directly + '/' +
                             'output.png')

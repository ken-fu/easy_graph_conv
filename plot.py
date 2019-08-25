# -*- coding: utf-8 -*-
'''グラフプロット処理部分'''
import csv

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from PyQt5.QtWidgets import QSizePolicy

PLOTMODE_1 = '1 graph in 1 figure'
PLOTMODE_2 = 'all graph in 1 figure'


class PlotCanvas(FigureCanvas):
    def __init__(self, file_list, output_directly, parent=None):

        self.file_list = file_list
        self.output_directly = output_directly

        self.fig = Figure(figsize=(4.8, 3), dpi=200)
        self.fig.subplots_adjust(left=0.2, right=0.95, bottom=0.16, top=0.95)
        self.axes = self.fig.add_subplot(111)

        self.xlog = False
        self.ylog = False
        self.xtics_label = True
        self.ytics_label = True
        self.xrange = []
        self.yrange = []
        self.xlabel = ''
        self.ylabel = ''
        self.line_plot = True
        self.legend_plot = False
        self.legend = ['']
        self.legend_loc = 'upper right'
        self.normarize = False

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def file_opener(self, file_path):
        '''tsv or csv opened and return x,y parameter'''
        f_1 = open(file_path, 'r')
        if('.csv' in file_path):
            f1list = list(csv.reader(f_1, delimiter=','))
        else:
            f1list = list(csv.reader(f_1, delimiter='\t'))
        x_list = []
        y_list = []
        for i in f1list:
            x_list.append(float(i[0]))
            y_list.append(float(i[1]))
        return x_list, y_list

    def fig_init(self):
        '''initialize fig axes'''
        self.axes = self.fig.add_subplot(111)
        self.axes.tick_params(which='minor', direction="in")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)

        if not self.xtics_label:
            self.axes.tick_params(labelbottom=False)
        if not self.ytics_label:
            self.axes.tick_params(labelleft=False)
        if self.xrange:
            self.axes.set_xlim(float(self.xrange[0]), float(self.xrange[1]))
        if self.yrange:
            self.axes.set_ylim(float(self.yrange[0]), float(self.yrange[1]))
        if self.xlog:
            self.axes.set_xscale('log')
        if self.ylog:
            self.axes.set_yscale('log')
        self.axes.tick_params(which='minor', labelleft=False)

        self.axes.tick_params(direction="in")

    def normarize_data(self, x_data, y_data):
        '''normarize input data (y_data)'''
        min_y_data = min(y_data)
        print(min_y_data)
        temp_y_list = []
        for i, _ in enumerate(y_data):
            temp_y_list.append(y_data[i] - min_y_data)
        max_y_data = max(temp_y_list)
        output_y_list = []
        for j, _ in enumerate(temp_y_list):
            output_y_list.append(temp_y_list[j] / max_y_data)
        return x_data, output_y_list
    
    def normarize_log_data(self, x_data, y_data):
        '''normarize input data (y_data)'''
        y_data = np.log10(y_data)
        max_y_data = max(y_data)
        output_y_list = []
        for j, _ in enumerate(y_data):
            output_y_list.append(10**(y_data[j] / max_y_data))
        return x_data, output_y_list

    def plot(self, plot_style):
        '''plot data. plot_style: PLOTMODE_1 1graph in 1fig 
            PLOTMODE_2 all graph in 1fig'''
        if self.legend_plot:
            while(len(self.file_list) > len(self.legend)):
                self.legend.append('')

        for file_num, path in enumerate(self.file_list):
            self.fig_init()
            x_list, y_list = self.file_opener(path)
            if self.normarize:
                if self.ylog:
                    x_list, y_list = self.normarize_log_data(x_list, y_list)
                else:
                    x_list, y_list = self.normarize_data(x_list, y_list)

            if self.line_plot:
                self.axes.plot(x_list, y_list, linewidth=1)
            else:
                self.axes.plot(x_list, y_list, linestyle='None', marker='o')
            self.draw()
            # 出力
            if plot_style == PLOTMODE_1:
                if self.legend_plot:
                    self.axes.legend(self.legend[file_num], loc=self.legend_loc, fontsize=35, prop={
                                     'size': 9}, labelspacing=0)
                self.fig.savefig(self.output_directly + '/' + str(path).split('/')
                                 [-1].split('.')[0] + '.png')
                self.axes.clear()
        if plot_style == PLOTMODE_2:
            if self.legend_plot:
                self.axes.legend(self.legend, loc=self.legend_loc, fontsize=35, prop={
                                 'size': 9}, labelspacing=0)
            self.fig.savefig(self.output_directly + '/' +
                             'output.png')

# -*- coding: utf-8 -*-
'''Base Class of PlotCanvas'''
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


class PlotCanvas(FigureCanvas):
    '''FigureCanvas Class'''

    def __init__(self, parent=None, width=4.8, height=3, dpi=200):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.subplots_adjust(left=0.2, right=0.95, bottom=0.16, top=0.95)
        self.plot_canvas = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        #Turn main and sub ticks inward
        self.plot_canvas.tick_params(
            which="major", direction='in', labelleft=False)
        self.plot_canvas.tick_params(
            which="minor", direction='in', labelleft=False)

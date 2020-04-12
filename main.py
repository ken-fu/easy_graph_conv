# -*- coding: utf-8 -*-
'''plot tool'''
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTextEdit, QComboBox
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.Qt import Qt, QDoubleValidator

from plot import PlotGraphCanvas
from base_func.gui_widget import TableWidgetDragRows

PLOTMODE_1 = '1 graph in 1 figure'
PLOTMODE_2 = 'all graph in 1 figure'


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(800, 650)
        self.setAcceptDrops(True)
        self.move(100, 100)
        self.setWindowTitle('easy_graph_conv')
        self.create_widgets()

        self.show()

    def create_widgets(self):
        '''create widgets on main window'''
        self.main_listview = TableWidgetDragRows(self)
        self.main_listview.move(10, 60)
        self.main_listview.setFixedSize(200, 500)
        self.main_listview.setColumnCount(2)
        self.main_listview.setHorizontalHeaderLabels(
            ['file name', 'file path'])
        self.main_listview.setEditTriggers(QTableWidget.NoEditTriggers)
        self.main_listview.setColumnWidth(0, 140)
        self.main_listview.setColumnWidth(1, 400)
        self.main_listview.hideColumn(1)

        self.label_drop_here = QLabel('File Drop Here', self)
        self.label_drop_here.move(25, 30)

        self.pbutton_remove_row = QPushButton('remove', self)
        self.pbutton_remove_row.move(15, 570)
        self.pbutton_remove_row.clicked.connect(self.remove_row)

        self.pbutton_remove_row = QPushButton('remove all', self)
        self.pbutton_remove_row.move(15, 590)
        self.pbutton_remove_row.clicked.connect(self.remove_row_all)

        self.label_legend = QLabel('Graph Legend', self)
        self.label_legend.move(235, 30)

        self.textedit_legend = QTextEdit(self)
        self.textedit_legend.setFixedSize(200, 480)
        self.textedit_legend.move(220, 80)

        self.label_legend_unit = QLabel('Legend unit', self)
        self.label_legend_unit.move(220, 570)
        self.textbox_legend_unit = QLineEdit(self)
        self.textbox_legend_unit.move(220, 590)

        self.label_xlabel = QLabel('xlabel', self)
        self.label_xlabel.move(465, 30)
        self.textbox_xlabel = QLineEdit(self)
        self.textbox_xlabel.move(465, 50)
        self.textbox_xlabel.setFixedWidth(300)

        self.label_ylabel = QLabel('ylabel', self)
        self.label_ylabel.move(465, 80)
        self.textbox_ylabel = QLineEdit(self)
        self.textbox_ylabel.move(465, 100)
        self.textbox_ylabel.setFixedWidth(300)

        self.checkbox_xlog = QCheckBox('x logscale', self)
        self.checkbox_xlog.move(465, 130)
        self.checkbox_ylog = QCheckBox('y logscale', self)
        self.checkbox_ylog.move(465, 150)

        self.checkbox_xtick_label = QCheckBox('without xtick label', self)
        self.checkbox_xtick_label.move(630, 130)
        self.checkbox_ytick_label = QCheckBox('without ytick label', self)
        self.checkbox_ytick_label.move(630, 150)

        self.checkbox_wline_plot = QCheckBox('without line plot', self)
        self.checkbox_wline_plot.move(465, 180)
        self.checkbox_normarize_plot = QCheckBox('normarized plot', self)
        self.checkbox_normarize_plot.move(465, 200)

        self.checkbox_legend_plot = QCheckBox('with legend', self)
        self.checkbox_legend_plot.move(630, 180)
        self.combobox_legend_position = QComboBox(self)
        self.combobox_legend_position.move(630, 195)
        self.combobox_legend_position.addItems(
            ['upper right', 'upper left', 'lower right', 'lower left'])
        self.combobox_legend_position.setFixedWidth(140)

        self.checkbox_xrange = QCheckBox('set x range', self)
        self.checkbox_xrange.move(465, 240)
        self.textbox_xmin = QLineEdit(self)
        self.textbox_xmin.move(470, 260)
        self.textbox_xmin.setValidator(QDoubleValidator())
        self.label_x_to = QLabel('to', self)
        self.label_x_to.move(600, 260)
        self.textbox_xmax = QLineEdit(self)
        self.textbox_xmax.move(620, 260)
        self.textbox_xmax.setValidator(QDoubleValidator())

        self.checkbox_yrange = QCheckBox('set y range', self)
        self.checkbox_yrange.move(465, 290)
        self.textbox_ymin = QLineEdit(self)
        self.textbox_ymin.move(470, 310)
        self.textbox_ymin.setValidator(QDoubleValidator())
        self.label_y_to = QLabel('to', self)
        self.label_y_to.move(600, 310)
        self.textbox_ymax = QLineEdit(self)
        self.textbox_ymax.move(620, 310)
        self.textbox_ymax.setValidator(QDoubleValidator())

        self.label_plot_style = QLabel('Plot Style', self)
        self.label_plot_style.move(465, 535)
        self.combobox_plot_style = QComboBox(self)
        self.combobox_plot_style.move(550, 530)
        self.combobox_plot_style.addItems(
            [PLOTMODE_1, PLOTMODE_2])
        self.combobox_plot_style.setFixedWidth(200)

        self.pbutton_save = QPushButton('Plot and Save', self)
        self.pbutton_save.move(465, 570)
        self.pbutton_save.clicked.connect(self.graph_save)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                row_count = self.main_listview.rowCount()
                self.main_listview.setRowCount(row_count+1)
                self.main_listview.setItem(
                    row_count, 0, QTableWidgetItem(str(path).split('/')[-1]))
                self.main_listview.setItem(
                    row_count, 1, QTableWidgetItem(path))
                self.main_listview.item(row_count, 0).setToolTip(path)

    def remove_row(self):
        self.main_listview.removeRow(self.main_listview.currentRow())

    def remove_row_all(self):
        self.main_listview.clear()
        self.main_listview.setRowCount(0)

    def check_option(self, canvas):
        '''check option parameter'''
        canvas.plot_canvas.tick_params(labelleft=True)
        if(self.checkbox_xlog.checkState() == Qt.Checked):
            canvas.plot_canvas.set_xscale('log')
        if(self.checkbox_ylog.checkState() == Qt.Checked):
            canvas.plot_canvas.set_yscale('log')
        if(self.checkbox_xtick_label.checkState() == Qt.Checked):
            canvas.plot_canvas.tick_params(labelbottom=False)
        if(self.checkbox_ytick_label.checkState() == Qt.Checked):
            canvas.plot_canvas.tick_params(labelleft=False)
        canvas.plot_canvas.set_xlabel(self.textbox_xlabel.text())
        canvas.plot_canvas.set_ylabel(self.textbox_ylabel.text())
        if self.checkbox_xrange.checkState() == Qt.Checked:
            canvas.plot_canvas.set_xlim(float(self.textbox_xmin.text()), float(self.textbox_xmax.text()))
        if self.checkbox_yrange.checkState() == Qt.Checked:
            canvas.plot_canvas.set_ylim(float(self.textbox_ymin.text()), float(self.textbox_ymax.text()))

        

    def graph_save(self):
        '''graph output .png'''
        path_list = []
        for path_item in range(self.main_listview.rowCount()):
            path_list.append(self.main_listview.item(path_item, 1).text())
        directly_name = QFileDialog.getExistingDirectory(self)
        if len(directly_name) == 0:
            return
        self.main_graph = PlotGraphCanvas()
        self.check_option(self.main_graph)

        normarize = (self.checkbox_normarize_plot.checkState() == Qt.Checked)
        plot_style = self.combobox_plot_style.currentText()
        legend_plot = (self.checkbox_legend_plot.checkState() == Qt.Checked)
        legend_loc = self.combobox_legend_position.currentText()
        ylog = (self.checkbox_ylog.checkState() == Qt.Checked)
        line_plot = (self.checkbox_wline_plot.checkState() != Qt.Checked)

        temp_legend = self.textedit_legend.toPlainText().split('\n')
        legend_unit = self.textbox_legend_unit.text()
        legend_list = []
        if legend_unit:
            for legend in temp_legend:
                legend_list.append(legend + legend_unit)
        else:
            legend_list = temp_legend

        self.main_graph.plot(path_list, directly_name, plot_style, legend_plot, legend_list, legend_loc, line_plot, normarize, ylog)


def main():
    main_app = QApplication(sys.argv)
    main_window = MainWidget()
    sys.exit(main_app.exec_())


if __name__ == '__main__':
    main()

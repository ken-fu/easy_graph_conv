# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QAbstractItemView, QTextEdit, QComboBox
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.Qt import Qt, QDropEvent, QDoubleValidator

from plot import PlotCanvas

PLOTMODE_1 = '1 graph in 1 figure'
PLOTMODE_2 = 'all graph in 1 figure'


class TableWidgetDragRows(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()


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

    def check_option(self):
        '''check option parameter'''
        if self.checkbox_xlog.checkState() == Qt.Checked:
            self.main_graph.xlog = True
        if self.checkbox_ylog.checkState() == Qt.Checked:
            self.main_graph.ylog = True

        if self.checkbox_xtick_label.checkState() == Qt.Checked:
            self.main_graph.xtics_label = False
        if self.checkbox_ytick_label.checkState() == Qt.Checked:
            self.main_graph.ytics_label = False

        if self.checkbox_wline_plot.checkState() == Qt.Checked:
            self.main_graph.line_plot = False

        self.main_graph.normarize = self.checkbox_normarize_plot.checkState() == Qt.Checked
        self.plot_style = self.combobox_plot_style.currentText()

        self.main_graph.xlabel = self.textbox_xlabel.text()
        self.main_graph.ylabel = self.textbox_ylabel.text()

        if self.checkbox_xrange.checkState() == Qt.Checked:
            self.main_graph.xrange = [
                self.textbox_xmin.text(), self.textbox_xmax.text()]
        if self.checkbox_yrange.checkState() == Qt.Checked:
            self.main_graph.yrange = [
                self.textbox_ymin.text(), self.textbox_ymax.text()]

        self.main_graph.legend_plot = self.checkbox_legend_plot.checkState() == Qt.Checked
        self.main_graph.legend_loc = self.combobox_legend_position.currentText()
        self.temp_legend = self.textedit_legend.toPlainText().split('\n')

        self.legend_unit = self.textbox_legend_unit.text()
        self.temp_2_legend = []
        if self.legend_unit:
            for _ , legend in enumerate(self.temp_legend):
                print(type(legend))
                print(type(self.legend_unit))
                self.temp_2_legend.append(legend + self.legend_unit)
        else:
            self.temp_2_legend = self.temp_legend
        self.main_graph.legend = self.temp_2_legend

    def graph_save(self):
        '''graph output .png'''
        self.path_list = []
        for path_item in range(self.main_listview.rowCount()):
            self.path_list.append(self.main_listview.item(path_item, 1).text())
        directly_name = QFileDialog.getExistingDirectory(self)
        print(directly_name)
        if len(directly_name) == 0:
            return
        self.main_graph = PlotCanvas(self.path_list, directly_name)
        self.check_option()
        self.main_graph.plot(self.plot_style)


def main():
    main_app = QApplication(sys.argv)
    main_window = MainWidget()
    sys.exit(main_app.exec_())


if __name__ == '__main__':
    main()

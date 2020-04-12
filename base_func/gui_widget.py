# -*- coding: utf-8 -*-
'''original widgets by PyQt5 '''
import os

from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QAbstractItemView, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.Qt import Qt, QDropEvent


class PathTextBox(QLineEdit):
    '''text box for file path'''

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                self.setText(path)


class FileDropArea(QTextEdit):
    '''widget for drop file area'''

    def __init__(self, tree, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.main_listview = tree

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        '''output the dropped file to the argument tree'''
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


class TableWidgetDragRows(QTableWidget):
    '''Table widget for filename and path'''
    # Tree where items can be sorted

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
        # Sorting item process
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


class ImportFileWidget(QDialog):
    '''import file widget (window)'''

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(280, 360)
        self.setAcceptDrops(True)
        self.move(100, 100)
        self.setWindowTitle('import file')
        self.create_widgets()
        self.create_widgets_add()
        self.path_list = []

        self.show()

    def create_widgets(self):
        '''create widgets on window'''
        self.main_listview = TableWidgetDragRows(self)
        self.main_listview.move(10, 35)
        self.main_listview.setFixedSize(150, 250)
        self.main_listview.setColumnCount(2)
        self.main_listview.setHorizontalHeaderLabels(
            ['file name', 'file path'])
        self.main_listview.setEditTriggers(QTableWidget.NoEditTriggers)
        self.main_listview.setColumnWidth(0, 140)
        self.main_listview.setColumnWidth(1, 400)
        self.main_listview.hideColumn(1)

        self.label_drop_here = QLabel('File Drop Here', self)
        self.label_drop_here.move(25, 10)

        self.pbutton_remove_row = QPushButton('remove', self)
        self.pbutton_remove_row.move(170, 190)
        self.pbutton_remove_row.clicked.connect(self.remove_row)

        self.pbutton_remove_row = QPushButton('reset', self)
        self.pbutton_remove_row.move(170, 220)
        self.pbutton_remove_row.clicked.connect(self.remove_row_all)

        self.pbutton_go = QPushButton('Go', self)
        self.pbutton_go.move(170, 260)
        self.pbutton_go.clicked.connect(self.file_list_go)

    def create_widgets_add(self):
        '''add widgets'''
        pass

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        '''Import file and output to list'''
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
        '''remove select row from table'''
        self.main_listview.removeRow(self.main_listview.currentRow())

    def remove_row_all(self):
        '''all row from table'''
        self.main_listview.clear()
        self.main_listview.setRowCount(0)

    def file_list_go(self):
        '''get file list from table and close this window'''
        for path_item in range(self.main_listview.rowCount()):
            self.path_list.append(self.main_listview.item(path_item, 1).text())
        self.accept()

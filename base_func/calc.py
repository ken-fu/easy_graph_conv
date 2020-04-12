# -*- coding: utf-8 -*-
'''base functions for calc'''
import numpy as np


def normarize_data(data_list, log=False):
    '''normarize input data (y_data)'''
    y_data = np.array(data_list)
    output_y_list = np.array([])

    if log:
        y_data = np.log10(y_data)
        output_y_list = 10**(y_data - max(y_data))

    else:
        min_y_data = min(y_data)
        max_y_data = max(y_data)
        output_y_list = (y_data-min_y_data)/(max_y_data-min_y_data)

    return output_y_list


def get_nearest_value_index(data_list, num):
    '''get nearest value index of list'''
    return np.abs(np.asarray(data_list) - num).argmin()

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap


def df2table(data, col_width=1.8, row_height=0.4, font_size=14,
           header_face_color='#3333B2', header_font_color='w',
           row_colors=('#e6e6e6', 'w'), edge_color='w',
           save_path=None, show_table=False, index_name=None,
           title=None, date_format='%d-%b-%Y', rounding=None):
    """
    :param data: pandas.DataFrame
    :param col_width: width of the columns
    :param row_height: heigth of the rows
    :param font_size: font size for the values. The title's font size will be 'font_size+2'
    :param header_face_color: background color for the row with the column titles
    :param header_font_color: font color for the columns titles
    :param row_colors: tuple with 2 color names or values. The background of the cells
                       will be painted with these colors to facilitate reading.
    :param edge_color: color of the edges of the table
    :param save_path: path to save the table as pdf file
    :param show_table: If True, shows a preview of the table
    :param index_name: Name of the column that will hold the index of the DataFrame
    :param title: Title of the Table
    :param date_format: formatting string to be passed to python's 'strftime', in case
                        the DataFrame has a panda DateTimeIndex
    :param rounding: Number of decimal places to round numeric values.
    :return: matplotlib axis object, in case you want to make further modifications.
    """
    # TODO col_width and row_height should be automatically set based on the length of titles and font_size.

    data = data.copy()

    if rounding is not None:
        data = data.round(rounding)

    if index_name is not None:
        data.index.name = index_name

    if isinstance(data.index, pd.DatetimeIndex):
        data.index = data.index.strftime(date_format)

    data = data.reset_index()

    size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])

    fig, ax = plt.subplots(figsize=size)
    ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=[0, 0, 1, 1], colLabels=data.columns, cellLoc='center')
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table.get_celld().items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0:
            cell.set_text_props(weight='bold', color=header_font_color)
            cell.set_facecolor(header_face_color)
        elif k[1] == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])

    plt.title(title, fontsize=font_size + 2, weight='bold')
    plt.tight_layout()

    if not (save_path is None):
        plt.savefig(save_path)

    if show_table:
        plt.show()

    plt.close()

    return ax.get_figure()


def df2heatmap(data, show_table=False, figsize=(9, 9), nodes=None, colors=None, cmap='rwb', cbar=False,
               fontsize=12, table_title=None, normalize='percentile', save_path=None, ax=None):
    """
    Creates a heatmap table from a pandas dataframe. The heatmap color scale can be based on either the
    percentage of the value relative to the range or based on its percentile.
    @param data: pandas.DataFrame, already sorted in the way you want to see it.
    @param show_table: bool. If True, previews the table during runtime.
    @param figsize: tuple with the dimensions of the figure.
    @param nodes: list of the thresholds (float) to be passed to the matplotlib's colormap building tool.
    @param colors: list of color names or codes (strings) to be passed to the matplotlib's colormap building tool.
    @param cmap: str with name of colormap or matplolib.colormap object.
                 https://matplotlib.org/stable/gallery/color/colormap_reference.html
    @param cbar: bool. If True, plots the colorbar on the figure.
    @param fontsize: Fontsize for the text in the table.
    @param table_title: str, title of the table. Its fontsize is 'fontsize' + 2
    @param normalize: 'percentile' or 'range'. If 'percentile', the heatmap is independent for each column and
                      based on the percentile of the observation. If 'range', the heatmap is independent for
                      each column and based on the percentage of the observation relative to the maximum range.
    @param save_path: str with the path to save the figure. File name must end with '.pdf' or '.png'.
    @param ax: matplotlib.Axis object. Allows to pass an axis that already exists. Used to creat a figure
               with multiple tables
    @return: matplotlib.Figure and matplotlib.Axis objects that can still be manipulated before plotting.
    """
    # TODO heatmap based on the full dataframe and not independent for each column. Add 'percentile-all'
    #  and 'range-all' normalization methods.

    # TODO heatmap based on the values themselves, with the possibilities to choose the range. 'values'

    assert len(colors) == len(nodes), "Length of 'colors' and 'nodes' must be the same"

    myfont = {'fontname': 'Century Gothic'}
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Century Gothic']

    if (nodes is not None) and (colors is not None):
        cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

    # normalize data by columns
    if normalize == 'percentile':
        df_plot = (data.rank() - 1) / (data.shape[0] - 1)

    elif normalize == 'range':
        df_plot = (data - data.min())/(data.max() - data.min())

    else:
        raise AssertionError('Normalization method not implemented.')

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    ax = sns.heatmap(df_plot, ax=ax, cbar=cbar, annot=data, cmap=cmap,
                     fmt='.2f', annot_kws={'fontsize': fontsize, 'weight': 'normal'},
                     linewidths=1, linecolor='lightgrey')

    ax.xaxis.tick_top()

    ax.set_xticklabels(ax.get_xticklabels(),
                       fontdict={'fontweight': 'bold',
                                 'fontsize': fontsize})

    ax.set_yticklabels(ax.get_yticklabels(),
                       fontdict={'fontweight': 'bold',
                                 'fontsize': fontsize})

    if table_title is not None:
        ax.set_title(table_title,
                     fontdict={'fontweight': 'bold', 'fontsize': fontsize + 2},
                     **myfont)

    plt.tick_params(axis='x', which='both', top=False, bottom=False)
    plt.tick_params(axis='y', which='both', left=False)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontsize)

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path)

    if show_table:
        plt.show()

    return fig, ax

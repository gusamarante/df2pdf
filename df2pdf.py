import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def df2pdf(data, col_width=1.8, row_height=0.4, font_size=14,
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


# TODO The example below should be removed before opening the pull request
# ===== EXAMPLE =====
df = pd.DataFrame(data={'Series A': [0, 1, 2, 3, 4],
                        'Series B': [4, 3, 2, 1, 0]},
                  index=pd.date_range('2021-01-01', periods=5, freq='M'))

df2pdf(df, index_name='Índice', title='Título da Tabela', show_table=True,
       save_path=r'/Users/gustavoamarante/Desktop/df2pdf.pdf')





import pandas as pd
from df2pdf import df2table, df2heatmap

df = pd.DataFrame(data={'Series A': [0, 1, 2, 3, 4],
                        'Series B': [4, 3, 2, 1, 0]},
                  index=pd.date_range('2021-01-01', periods=5, freq='M'))

df2table(df, index_name='Index Name', title='This is the title', show_table=True)

df2heatmap(df, table_title='This is the title', show_table=True,
           nodes=[0.0, 0.2, 0.8, 1.0],
           colors=['green', 'white', 'white', 'red'])

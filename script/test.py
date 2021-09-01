import pandas as pd
dict = {}

dict['column'] = {'row 1':3}
dict['column2'] = {'row 1':2}

pd.DataFrame.from_dict(data=dict, orient='index').to_csv('dict_file.csv', header=True)
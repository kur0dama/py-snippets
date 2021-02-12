# Tested with Python 3.7.6 and re 2.2.1
# Receives pd.Dataframe.columns, returns a list of cleaned column names (only [a-zA-Z0-9]) in upper snake-case 
# If first char is [0-9], it appends an underscore to the front of the string (follows SQL naming convention)
#
# Example:
# df has columns ['col #1: addr1','col #2: addr2','col #4: city','col #4: state','5zip']
# output of clean_colnames(df.columns) is ['COL_1_ADDR1', 'COL_2_ADDR2', 'COL_4_CITY', 'COL_4_STATE', '_5ZIP']

import re

def clean_colnames(colnames):
    out_list = []
    for header in colnames:
        step1 = re.findall('([a-zA-Z0-9]+)',header)
        step2 = str.upper('_'.join(step1))
        step3 = '_' + step2 if step2[0] in [ str(i) for i in range(0,10) ] else step2
        out_list.append(step3)
    return out_list

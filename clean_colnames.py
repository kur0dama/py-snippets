# Tested with Python 3.7.6 and re 2.2.1
# Receives pandas.Dataframe.columns, returns a list of cleaned column names (only [a-zA-Z0-9]) in upper snake-case.
# If first char is [0-9], it appends an underscore to the front of the string (follows SQL naming convention).
#
# In the event of duplicate column name values -- which Pandas allows, see Example #1 below -- will automatically
# append a number to the end of each duplicate column name, creating a distinct list. Due to the potential presence
# of duplicates, recoding via a dict to the pandas.DataFrame.rename() method is not advised since Python dicts cannot
# have duplicate keys.
#
# Note #1: There is no substitute for careful examination of column values on import when receiving a file with
# unclear (or non-existent) data specifications.
#
# Note #2: Reliance on ASCII in regex used for string cleaning means this function will ONLY handle English language
# headers properly.
#
# Example #1:
# data = [[1, 2, 1], [1, 3, 1], [1, 4, 1]]
# df = pd.DataFrame(data, columns=['A','B','B']).columns
# clean_colnames(df.columns) returns ['A', 'B_0', 'B_1']
#
# Example #2:
# df is a pandas.DataFrame with columns ['col #1: addr1','col #2: addr2','col #4: city','col #4: state','5zip','5zip']
# output of clean_colnames(df.columns) is ['COL_1_ADDR1', 'COL_2_ADDR2', 'COL_4_CITY', 'COL_4_STATE', '_5ZIP_1', '_5ZIP_2']


import re


def find_dupes(in_list, return_dupe_recs_only=False):
    """
    Takes a list and returns a dictionary identifying the count of occurrences of each distinct element in the list
    Required arguments:
        in_list: a list to be checked for duplicates; may contain multiple types
    Optional arguments:
        return_dupe_recs_only: if True, function returns a dictionary containing only elements occurring more than once;
                                if False, function returns a dictionary containing all elements with their counts
    Returns:
        A dict in the format { distinct element: count of element in list }
    """
    dupe_map = { elem: 0 for elem in in_list }
    for elem in in_list:
        dupe_map[elem] = dupe_map[elem]+1
    if return_dupe_recs_only==False:
        return dupe_map
    else:
        return { key: val for key, val in dupe_map.items() if val>1 }


def clean_colnames(col_list):
    """
    Cleans column names in a pandas DataFrame (follows SQL format rules).
    Required arguments:
        col_list: a list-like of column name strings; typically pandas.DataFrame.columns
    Returns:
        A list of transformed strings that can be directly assigned back to pandas.DataFrame.columns
    Notes:
        In the event of duplicate values (either because input list contained duplicates, or because
        differentiating information was removed during string-cleaning process, function will alter
        output strings to ensure list contains only distinct values.
    """
    process_dict = {} # to preserve initial order, all cleaning and substitutions will be performed in a temporary dict
    for col_order, header in enumerate(col_list): # initial string cleaning
        step1 = re.findall('([a-zA-Z0-9]+)',header)
        step2 = str.upper('_'.join(step1))
        step3 = '_' + step2 if step2[0] in [ str(i) for i in range(0,10) ] else step2
        process_dict[col_order] = [header, step3]
    dupes = find_dupes([ val[1] for val in process_dict.values() ], True)  # find any duplicate values in output list
    for dupe_key in dupes.keys(): # process duplicate values and change to distinct strings
        recode_recs = { key: val for key, val in process_dict.items() if val[1] == dupe_key }
        for i, recode_key in enumerate(recode_recs.keys()):
            process_dict[recode_key][1] = process_dict[recode_key][1] + '_{:0d}'.format(i+1)
    out_list = [ val[1] for val in process_dict.values() ] # return list of cleaned strings as output
    return out_list

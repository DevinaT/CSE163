"""
Niyat Efrem, Claire Lai, Devina Tavahia
TA Mentor: Paolo Pan
This file contains the functions needed to clean all three datasets.
"""
import pandas as pd


def tabacco_clean(file: str) -> pd.DataFrame:
    '''
    This function takes in the tabacco dataset and returns a cleaned
    dataset with only the 50 states and the columns of interest.
    '''
    tabacco_df = pd.read_csv(file, dtype={'YEAR': "string"})
    tabacco_df = tabacco_df[['YEAR', 'LocationAbbr', 'TopicDesc',
                             'MeasureDesc', 'Data_Value', 'Gender',
                             'Race', 'Age', 'Education']]
    tabacco_df = tabacco_df[(tabacco_df['TopicDesc'] ==
                            'Cigarette Use (Adults)') &
                            (tabacco_df['MeasureDesc'] == 'Current Smoking') &
                            (tabacco_df['LocationAbbr'] != 'PR') &
                            (tabacco_df['LocationAbbr'] != 'GU') &
                            (tabacco_df['LocationAbbr'] != 'US') &
                            (tabacco_df['LocationAbbr'] != 'DC') &
                            (tabacco_df['YEAR'] != '2016-2017') &
                            (tabacco_df['YEAR'] != '2017-2018') &
                            (tabacco_df['YEAR'] != '2018-2019') &
                            (tabacco_df['YEAR'] != '2011-2012') &
                            (tabacco_df['YEAR'] != '2012-2013') &
                            (tabacco_df['YEAR'] != '2014-2015') &
                            (tabacco_df['YEAR'] != '2015-2016')]
    return tabacco_df


def obesity_cleaned(filename: str) -> pd.DataFrame:
    """
    This function takes in the obesity dataframe and filters out all the
    locations that are not the 50 US states. For these states it returns
    only the relevant columns to our anaylsis.
    """
    obesity_df = pd.read_csv(filename)
    is_state = ((obesity_df["Locationdesc"] != "Puerto Rico") &
                (obesity_df["Locationdesc"] != "Virgin Islands") &
                (obesity_df["Locationdesc"] != "District of Columbia") &
                (obesity_df["Locationdesc"] != "Guam"))
    obesity_df = obesity_df.loc[is_state, ["Year", "Locationabbr",
                                           "Response", "Break_Out",
                                           "Data_value", "GeoLocation"]]
    return obesity_df


def cardiovascular_cleaned(filename: str) -> pd.DataFrame:
    """
    This function takes in the cardiovascular dataframe and filters out all the
    locations that are not the 50 US states. For these states it returns
    only the relevant columns to our anaylsis.
    """
    c_df = pd.read_csv(filename)
    c_df = c_df[(c_df['LocationAbbr'] != 'DC') &
                (c_df['LocationAbbr'] != 'USM')]
    return c_df

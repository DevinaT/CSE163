def main():
    import pandas as pd
    cardiovascular_df = pd.read_csv('https://raw.githubusercontent.com/DevinaT/CSE163/main/Cardiovascular.csv')
    obesity_df = pd.read_csv('https://raw.githubusercontent.com/DevinaT/CSE163/main/Obesity.csv')
    tabacco_df = pd.read_csv('https://raw.githubusercontent.com/DevinaT/CSE163/main/Tobacco.csv')

    # tobacco dataset cleaning
    tabacco_df = tabacco_df[['YEAR', 'LocationAbbr', 'TopicDesc',
                             'MeasureDesc', 'Data_Value', 'Gender',
                             'Race', 'Age', 'Education']]
    tabacco_df = tabacco_df[(tabacco_df['TopicDesc'] == 'Cigarette Use (Adults)') &
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

    # obesity dataset cleaning
    is_state = ((obesity_df["Locationdesc"] != "Puerto Rico") &
                (obesity_df["Locationdesc"] != "Virgin Islands") &
                (obesity_df["Locationdesc"] != "District of Columbia") &
                (obesity_df["Locationdesc"] != "Guam"))
    obesity_filtered = obesity_df.loc[is_state, ["Year", "Locationabbr",
                                                 "Response", "Break_Out",
                                                 "Data_value"]]

    # cardiovascular dataset cleaning
    cardiovascular_df = cardiovascular_df[(cardiovascular_df['LocationAbbr'] != 'DC') & (cardiovascular_df['LocationAbbr'] != 'USM')]

if __name__ == '__main__':
    main()

'''
Devina Tavathia
TA Mentor Paolo Pan

This module contains the functions needed to answer
reserach question 2, using the cardiovascular and
obesity datasets.
'''
import pandas as pd
import cleanedData as cd
import plotly.express as px

topTenList = []


def find_top_ten(cardio_vasc: pd.DataFrame) -> list[str]:
    """
    Finds the top 10 states in the dataset
    with the highest risk of cardiovascular disease.
    Return a list of the top 10 states.
    """
    # filter cardiovascualr
    cardio_vasc = cardio_vasc[cardio_vasc['Data_Value_Alt'] > 0]
    # find top 10 states with highest rate of cardiovascular disease
    cardio_vasc_10 = cardio_vasc.groupby('LocationAbbr')['Data_Value_Alt']
    cardio_vasc_10 = cardio_vasc_10.mean().reset_index(name='Percentage')
    cardio_vasc_10 = cardio_vasc_10.nlargest(10, 'Percentage')
    topTenList.append(cardio_vasc_10["LocationAbbr"].values.tolist())
    return topTenList


def format_cardiovasc(df: pd.DataFrame, ten_list: list[str]) -> pd.DataFrame:
    """
    Filters the cardiovasular dataset down to only
    the states contained within the top 10 list made earlier.
    Also filters down the dataset to only the years we want
    (2011-2018). Then, group by states and subgroup by year. Find
    the mean value of cardiovscular rates for each of these
    subgroups and rename the column for plotting.
    """
    df = df[(df['LocationAbbr'] == ten_list[0][0]) |
            (df['LocationAbbr'] == ten_list[0][1]) |
            (df['LocationAbbr'] == ten_list[0][2]) |
            (df['LocationAbbr'] == ten_list[0][3]) |
            (df['LocationAbbr'] == ten_list[0][4]) |
            (df['LocationAbbr'] == ten_list[0][5]) |
            (df['LocationAbbr'] == ten_list[0][6]) |
            (df['LocationAbbr'] == ten_list[0][7]) |
            (df['LocationAbbr'] == ten_list[0][8]) |
            (df['LocationAbbr'] == ten_list[0][9])]
    df = df[(df['Year'] >= 2011) & (df['Year'] <= 2018)]
    vals = ['LocationAbbr', 'Year']
    colName = 'Average Cardiovascular Disease Percentage Rate'
    df = df.groupby(vals)['Data_Value_Alt'].mean()
    df = df.reset_index(name=colName)
    return df


def format_obesity(obesity: pd.DataFrame, ten_list: list[str]) -> pd.DataFrame:
    """
    Filters the obesity dataset down to only
    the states contained within the top 10 list made earlier.
    Also filters down the dataset to only the years we want
    (2011-2018). Then, group by states and subgroup by year. Find
    the mean value of obesity percentages for each of these
    subgroups and rename the column for plotting.
    """
    # filter obesity dataset
    obesity = obesity[(obesity['Response'] == 'Obese (BMI 30.0 - 99.8)') |
                      (obesity['Response'] == 'Overweight (BMI 25.0-29.9)')]
    obesity = obesity[(obesity['Locationabbr'] == ten_list[0][0]) |
                      (obesity['Locationabbr'] == ten_list[0][1]) |
                      (obesity['Locationabbr'] == ten_list[0][2]) |
                      (obesity['Locationabbr'] == ten_list[0][3]) |
                      (obesity['Locationabbr'] == ten_list[0][4]) |
                      (obesity['Locationabbr'] == ten_list[0][5]) |
                      (obesity['Locationabbr'] == ten_list[0][6]) |
                      (obesity['Locationabbr'] == ten_list[0][7]) |
                      (obesity['Locationabbr'] == ten_list[0][8]) |
                      (obesity['Locationabbr'] == ten_list[0][9])]
    obesity = obesity[(obesity['Year'] >= 2011) & (obesity['Year'] <= 2018)]
    # perform 2 groupby operations, first group by location and then year
    obesity = obesity.groupby(['Locationabbr', 'Year'])['Data_value'].mean()
    obesity = obesity.reset_index(name='Average Obesity Percentage Rate')
    return obesity


def main():
    # load the data
    cardio_vasc = cd.cardiovascular_cleaned('https://raw.githubusercontent'
                                            '.com/'
                                            'DevinaT/CSE163/main/'
                                            'Cardiovascular.csv')
    obesity = cd.obesity_cleaned('https://raw.githubusercontent.com/'
                                 'DevinaT/CSE163/main/Obesity.csv')
    # Call your test functions here!
    top10 = find_top_ten(cardio_vasc)
    cardio_vasco = format_cardiovasc(cardio_vasc, top10)
    obesity_df = format_obesity(obesity, top10)
    # print(obesity_df)
    # plotting time!
    # this is for obesity
    fig = px.line(obesity_df, x='Year',
                  y='Average Obesity Percentage Rate',
                  color='Locationabbr', markers=True)
    fig.update_layout(
        title="Average Obesity Rate Trends Over Time for States of " +
              "Highest Cardiovascular Risk",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        legend_title="State Abbreviation"
    )
    fig.show()

    # this is for cardiovascular
    fig = px.line(cardio_vasco, x='Year',
                  y='Average Cardiovascular Disease Percentage Rate',
                  color='LocationAbbr', markers=True)
    fig.update_layout(
        title="Average Cardiovascular Rate Trends Over Time for" +
              "States at Highest Risk",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        legend_title="State Abbreviation"
    )
    fig.show()


if __name__ == '__main__':
    main()

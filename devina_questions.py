import cleanedData as cd
import pandas as pd
import plotly.express as px

# load the data
cardio_vasc = cd.cardiovascular_df
obesity = cd.obesity_df
topTenList = []


def find_top_ten(cardio_vasc: pd.dataframe) -> None:
    """
    Finds the top 10 states in the dataset
    with the highest risk of cardiovascular disease.
    Return a list of the top 10 states.
    """
    # filter cardiovascualr
    cardio_vasc = cardio_vasc[cardio_vasc['Data_Value_Alt'] > 0]
    # find top 10 states with highest rate of cardiovascular disease
    cardio_vasc_10 = cardio_vasc.groupby('LocationAbbr')['Data_Value_Alt'].mean()
    cardio_vasc_10 = cardio_vasc_10.reset_index(name='Percentage')
    cardio_vasc_10 = cardio_vasc_10.nlargest(10, 'Percentage')
    topTenList.append(cardio_vasc_10["LocationAbbr"].values.tolist())


def format_cardiovasc(df: pd.dataframe) -> pd.dataframe:
    """
    Filters the cardiovasular dataset down to only
    the states contained within the top 10 list made earlier.
    Also filters down the dataset to only the years we want
    (2011-2018). Then, group by states and subgroup by year. Find
    the mean value of cardiovscular rates for each of these
    subgroups and rename the column for plotting.
    """
    df = df[(df['LocationAbbr'] == topTenList[0]) |
            (df['LocationAbbr'] == topTenList[1]) |
            (df['LocationAbbr'] == topTenList[2]) |
            (df['LocationAbbr'] == topTenList[3]) |
            (df['LocationAbbr'] == topTenList[4]) |
            (df['LocationAbbr'] == topTenList[5]) |
            (df['LocationAbbr'] == topTenList[6]) |
            (df['LocationAbbr'] == topTenList[7]) |
            (df['LocationAbbr'] == topTenList[8]) |
            (df['LocationAbbr'] == topTenList[9])]
    df = df[(df['Year'] >= 2011) & (df['Year'] <= 2018)]
    vals = ['LocationAbbr', 'Year']
    colName = 'Average Cardiovascular Disease Percentage Rate'
    df = df.groupby(vals)['Data_Value_Alt'].mean()
    df = df.reset_index(name=colName)
    return df


def format_obesity(obesity: pd.dataframe) -> pd.dataframe:
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
    obesity = obesity[(obesity['Locationabbr'] == topTenList[0]) |
                      (obesity['Locationabbr'] == topTenList[1]) |
                      (obesity['Locationabbr'] == topTenList[2]) |
                      (obesity['Locationabbr'] == topTenList[3]) |
                      (obesity['Locationabbr'] == topTenList[4]) |
                      (obesity['Locationabbr'] == topTenList[5]) |
                      (obesity['Locationabbr'] == topTenList[6]) |
                      (obesity['Locationabbr'] == topTenList[7]) |
                      (obesity['Locationabbr'] == topTenList[8]) |
                      (obesity['Locationabbr'] == topTenList[9])]
    obesity = obesity[(obesity['Year'] >= 2011) & (obesity['Year'] <= 2018)]
    # perform 2 groupby operations, first group by location and then year
    obesity = obesity.groupby(['Locationabbr', 'Year'])['Data_value'].mean()
    obesity = obesity.reset_index(name='Average Obesity Percentage Rate')
    return obesity


def main():
    # Call your test functions here!
    find_top_ten(cardio_vasc)
    format_cardiovasc(cardio_vasc)
    format_obesity(obesity)
    # plotting time!
    # this is for obesity
    fig = px.line(format_obesity(obesity), x='Year',
                  y='Average Obesity Percentage Rate',
                  color='Locationabbr', markers=True)
    fig.show()

    # this is for cardiovascular
    fig = px.line(format_cardiovasc(cardio_vasc), x='Year',
                  y='Average Cardiovascular Disease Percentage Rate',
                  color='LocationAbbr', markers=True)
    fig.show()


if __name__ == '__main__':
    main()

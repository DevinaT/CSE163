import cleanedData as cd
import pandas as pd
import plotly.graph_objects as go


def tabacco_filtered(tabacco: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes in the tabacco dataframe and returns a
    filtered data frame that has the columns of intrest.
    '''
    # Removing rows that have the following race
    tabacco = tabacco[(tabacco['Race'] != 'All Races') & (tabacco['Race'] !=
                                                          'American Indian/Alaska Native')]
    # Renaming the data value column to avoid confusion
    tabacco = tabacco.rename(columns={'Data_Value': 'smoker_percent'})

    return tabacco


def cardio_filtered(cardio_vasc: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes in the cleaned cardiovascular
    dataframe and returns a filtered version with columns
    of interest to make joining easier.
    '''
    # cardio_vasc = cd.cardiovascular_df
    # Choosing the rows that have breakout categories of intrest which is race
    cardio_vasc = cardio_vasc[(cardio_vasc['Break_Out_Category'] == 'Race') &
                              ((cardio_vasc['Break_Out'] == 'Non-Hispanic Black') |
                               (cardio_vasc['Break_Out'] == 'Non-Hispanic Asian') |
                               (cardio_vasc['Break_Out'] == 'Non-Hispanic White') |
                               (cardio_vasc['Break_Out'] == 'Hispanic'))]
    # Choosing the rows that have category of cardiovascular disease
    cardio_vasc = cardio_vasc[cardio_vasc['Category'] == 'Cardiovascular Diseases']
    # Choosing rows that have valid percentages
    cardio_vasc = cardio_vasc[cardio_vasc['Data_Value_Alt'] > 0]
    # Renaming the rows to make it easier for joining
    cardio_vasc['Break_Out'] = cardio_vasc['Break_Out'].replace(['Non-Hispanic Black'], 'African American')
    cardio_vasc['Break_Out'] = cardio_vasc['Break_Out'].replace(['Non-Hispanic Asian'], 'Asian/Pacific Islander')
    cardio_vasc['Break_Out'] = cardio_vasc['Break_Out'].replace(['Non-Hispanic White'], 'White')
    return cardio_vasc


def join_cardio_tabacco(tabacco: pd.DataFrame, cardio_vasc: pd.DataFrame) -> pd.DataFrame:
    '''
    This function returns the joined dataframe
    of tabacco and the cardiovascular 'Race'.
    '''
    combined_data = cardio_vasc.merge(tabacco, left_on='Break_Out', right_on='Race', how='outer')

    return combined_data


def final_table(combined_data: pd.DataFrame) -> pd.DataFrame:
    '''
    This fucntion returns the final combined dataframe
    where each row is a race and the columns show
    the avergae smoking and cardiovasucalr disease percentages.
    '''
    # Find each races avg disease percentage
    race_cardio = combined_data.groupby('Race')['Data_Value_Alt'].mean()
    # Find each races avg smoking rate
    race_smoke = combined_data.groupby('Race')['smoker_percent'].mean()
    # Combining the two
    results_by_race = pd.DataFrame(race_smoke).join(race_cardio)
    # Reseting index so that Race is a column
    results_by_race = results_by_race.reset_index()
    results_by_race = results_by_race.rename(columns=
                                             {'Data_Value_Alt':
                                              'cardiovascular_disease'})
    return results_by_race


def question_3_graph(results_by_race: pd.DataFrame) -> None:
    '''
    This fucntion returns a bar chart comparing smoking
    percentage and cardiovascualr disease percentage by race.
    '''
    fig = go.Figure()

    fig.add_trace(go.Bar(x=results_by_race['Race'],
                         y=results_by_race['cardiovascular_disease'],
                         text='Sick', name='ill',
                         marker=dict(color=results_by_race
                                     ['cardiovascular_disease'],
                                     coloraxis="coloraxis")))

    fig.add_trace(go.Bar(x=results_by_race['Race'],
                         y=results_by_race['smoker_percent'],
                         text='Smoker', name='Smoker',
                         marker=dict(color=results_by_race['smoker_percent'],
                                     coloraxis="coloraxis")))
    fig.update_layout(
        title="Comparing Percentage of People with Cardiovascular Disease vs. " +
              "Current Smokers by Race",
        xaxis_title="Race",
        yaxis_title="Percentage (%)",
        legend_title="Status"
    )
    fig.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=False)
    fig.show()


def main():
    tabacco = cd.tabacco_clean('https://raw.githubusercontent.com/DevinaT/CSE163/main/Tobacco.csv')
    cardio_vasc = cd.cardiovascular_cleaned('https://raw.githubusercontent.com/DevinaT/CSE163/main/Cardiovascular.csv')

    c_filtered = cardio_filtered(cardio_vasc)
    t_filtered = tabacco_filtered(tabacco)

    joined_tables = join_cardio_tabacco(t_filtered, c_filtered)

    final_df = final_table(joined_tables)

    question_3_graph(final_df)


if __name__ == "__main__":
    main()

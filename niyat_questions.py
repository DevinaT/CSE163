import cleanedData as cd
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go
# from plotly.subplots import make_subplots

tabacco = cd.tabacco_df
tabacco = tabacco[(tabacco['Race'] != 'All Races') & (tabacco['Race'] != 'American Indian/Alaska Native')]
tabacco = tabacco.rename(columns={'Data_Value':'smoker_percent'})
# print(tabacco)
cardio_vasc = cd.cardiovascular_df
cardio_vasc = cardio_vasc[(cardio_vasc['Break_Out_Category'] == 'Race') &
                          ((cardio_vasc['Break_Out'] == 'Non-Hispanic Black') |
                          (cardio_vasc['Break_Out'] == 'Non-Hispanic Asian') |
                          (cardio_vasc['Break_Out'] == 'Non-Hispanic White') |
                          (cardio_vasc['Break_Out'] == 'Hispanic'))]
cardio_vasc = cardio_vasc[cardio_vasc['Category'] == 'Cardiovascular Diseases']
cardio_vasc = cardio_vasc[cardio_vasc['Data_Value_Alt'] > 0]
cardio_vasc['Break_Out'] = cardio_vasc['Break_Out'].replace(['Non-Hispanic Black'], 'African American')
cardio_vasc['Break_Out'] = cardio_vasc['Break_Out'].replace(['Non-Hispanic Asian'], 'Asian/Pacific Islander')
cardio_vasc['Break_Out'] = cardio_vasc['Break_Out'].replace(['Non-Hispanic White'], 'White')
combined_data = cardio_vasc.merge(tabacco, left_on='Break_Out', right_on='Race', how='outer')

# find for race find the max data value
race_cardio = combined_data.groupby('Race')['Data_Value_Alt'].mean()
# find races with the mac smoking rate
race_smoke = combined_data.groupby('Race')['smoker_percent'].mean()
# combining the two
results_by_race = pd.DataFrame(race_smoke).join(race_cardio)
results_by_race = results_by_race.reset_index()
results_by_race = results_by_race.rename(columns={'Data_Value_Alt':
                                                  'cardiovascular_disease'})

# graph:
fig = go.Figure()

fig.add_trace(go.Bar(x=results_by_race['Race'],
                     y=results_by_race['cardiovascular_disease'],
                     text='Sick', name='ill',
                     marker=dict(color=results_by_race['cardiovascular_disease'],
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

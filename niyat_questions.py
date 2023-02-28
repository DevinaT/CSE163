import cleanedData as cd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
# print(tabacco)
# print(cardio_vasc)
combined_data = cardio_vasc.merge(tabacco, left_on='Break_Out', right_on='Race', how='outer')
# print(combined_data.head())
# find for race find the max data value
race_cardio = combined_data.groupby('Race')['Data_Value_Alt'].mean()
# print(race_cardio)
# find races with the mac smoking rate
race_smoke = combined_data.groupby('Race')['smoker_percent'].mean()
# print(type(race_smoke))
# combining the two
# using pandas series merge()
results_by_race = pd.DataFrame(race_smoke).join(race_cardio)
results_by_race = results_by_race.reset_index()
results_by_race = results_by_race.rename(columns={'Data_Value_Alt': 'cardiovascular_disease'})
print(results_by_race)

# using plotly
# plotting the line chart
# fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
fig = go.Figure()

fig.add_trace(go.Bar(x=results_by_race['Race'], y=results_by_race['cardiovascular_disease'], name='cardiovascularly ill'))

fig.add_trace(go.Bar(x=results_by_race['Race'], y=results_by_race['smoker_percent'], name='smoker'))

fig.show()
# # fig = px.bar(results_by_race, x="Race", y="smoker_percent", title='smoking graph')
# # fig.add_bar(x='Race', y='cardiovascular_disease')
# # fig.show()

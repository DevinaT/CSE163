import cleanedData as cd
import pandas as pd
import plotly.express as px

# load the data
cardio_vasc = cd.cardiovascular_df
obesity = cd.obesity_df

# filter cardiovascualr
cardio_vasc = cardio_vasc[cardio_vasc['Data_Value_Alt'] > 0]

# find top 10 states with highest rate of cardiovascular disease
cardio_vasc_10 = cardio_vasc.groupby('LocationAbbr')['Data_Value_Alt'].mean().nlargest(10)
#format cardiovascular data for graph
cardio_vasc = cardio_vasc[(cardio_vasc['LocationAbbr'] == 'WV') |(cardio_vasc['LocationAbbr'] == 'KY') |
                  (cardio_vasc['LocationAbbr'] == 'IA') | (cardio_vasc['LocationAbbr'] == 'TN') |
                  (cardio_vasc['LocationAbbr'] == 'AL') | (cardio_vasc['LocationAbbr'] == 'OH') |
                  (cardio_vasc['LocationAbbr'] == 'AR') | (cardio_vasc['LocationAbbr'] == 'DE') |
                  (cardio_vasc['LocationAbbr'] == 'WI') | (cardio_vasc['LocationAbbr'] == 'ND')]
cardio_vasc = cardio_vasc[(cardio_vasc['Year'] >= 2011) & (cardio_vasc['Year'] <= 2018)]
cardio_vasc = cardio_vasc.groupby(['LocationAbbr', 'Year'])['Data_Value_Alt'].mean().reset_index(name ='Average Cardiovascular Disease Percentage Rate')
# print(cardio_vasc)

# filter obesity dataset
obesity = obesity[(obesity['Response'] == 'Obese (BMI 30.0 - 99.8)') | (obesity['Response'] == 'Overweight (BMI 25.0-29.9)')]
obesity = obesity[(obesity['Locationabbr'] == 'WV') |(obesity['Locationabbr'] == 'KY') |
                  (obesity['Locationabbr'] == 'IA') | (obesity['Locationabbr'] == 'TN') |
                  (obesity['Locationabbr'] == 'AL') | (obesity['Locationabbr'] == 'OH') |
                  (obesity['Locationabbr'] == 'AR') | (obesity['Locationabbr'] == 'DE') |
                  (obesity['Locationabbr'] == 'WI') | (obesity['Locationabbr'] == 'ND')]
obesity = obesity[(obesity['Year'] >= 2011) & (obesity['Year'] <= 2018)]

# perform 2 groupby operations, first group by location and then year
obesity = obesity.groupby(['Locationabbr', 'Year'])['Data_value'].mean().reset_index(name ='Average Obesity Percentage Rate')
# print(obesity)

# plotting time!

# this is for obesity
fig = px.line(obesity, x='Year', y='Average Obesity Percentage Rate', color='Locationabbr', markers=True)
fig.show()

#this is for cardiovascular
fig = px.line(cardio_vasc, x='Year', y='Average Cardiovascular Disease Percentage Rate', color='LocationAbbr', markers=True)
fig.show()
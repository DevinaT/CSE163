import cleanedData as cd
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# load the data
tabacco = cd.tabacco_df
obesity = cd.obesity_df

# filter the tobacco df
all_races = tabacco["Race"] == "All Races"
all_education = tabacco["Education"] == "All Grades"
all_genders = tabacco["Gender"] == "Overall"

young_adult = tabacco["Age"] == "18 to 24 Years"
early_adult = tabacco["Age"] == "25 to 44 Years"
middle_adult = tabacco["Age"] == "45 to 64 Years"
older_adult = tabacco["Age"] == "65 Years and Older"

filtered_tabacco = tabacco.loc[all_races & all_genders & all_education &
                               (young_adult | early_adult |
                                middle_adult | older_adult)]
# print(filtered_tabacco)

# filter the obesity df
young_adult = obesity["Break_Out"] == "18-24"
early_adult = ((obesity["Break_Out"] == "25-34") |
               (obesity["Break_Out"] == "35-44"))
middle_adult = ((obesity["Break_Out"] == "45-54") |
                (obesity["Break_Out"] == "55-64"))
older_adult = obesity["Break_Out"] == "65+"

is_obese = obesity["Response"] == "Obese (BMI 30.0 - 99.8)"


filtered_obesity = obesity.loc[is_obese & (young_adult | older_adult)].copy()
filtered_obesity["Break_Out"] = filtered_obesity["Break_Out"].replace({"18-24": "18 to 24 Years"})
filtered_obesity["Break_Out"] = filtered_obesity["Break_Out"].replace({"65+": "65 Years and Older"})
# print(filtered_obesity)

early_adult_df = obesity.loc[is_obese & early_adult]
early_adult_grouped = early_adult_df.groupby(["GeoLocation", "Year"])["Data_value"].mean()
early_adult_grouped = early_adult_grouped.reset_index()
early_adult_grouped["Break_Out"] = ["25 to 44 Years"] * 398
# print(early_adult_grouped)
new_df = pd.concat([filtered_obesity, early_adult_grouped])

middle_adult_df = obesity.loc[is_obese & middle_adult]
middle_adult_grouped = middle_adult_df.groupby(["GeoLocation", "Year"])["Data_value"].mean()
middle_adult_grouped = middle_adult_grouped.reset_index()
middle_adult_grouped["Break_Out"] = ["45 to 64 Years"] * 398
# print(middle_adult_grouped)
new_df = pd.concat([new_df, middle_adult_grouped])
# print(new_df)

fig = go.Figure()

fig.add_trace(go.Violin(y=filtered_tabacco["Data_Value"], x=filtered_tabacco["Age"], box_visible=True, name="Rates of Tobacoo Use"))
fig.add_trace(go.Violin(y=new_df["Data_value"], x=new_df["Break_Out"], box_visible=True, name="Rates of Obesity"))
fig.show()

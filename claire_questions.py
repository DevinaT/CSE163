import cleanedData as cd
import pandas as pd
import plotly.graph_objects as go


# filter the tobacco df
def q1_filter_tabacoo(tabacco: pd.DataFrame) -> pd.DataFrame:
    """
    This function further filters down the tobacco dataset to the
    vlaues needed for this analysis only.
    """
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
    return filtered_tabacco


def q1_filter_obesity(obesity: pd.DataFrame) -> pd.DataFrame:
    # create masks to get the data needed
    young_adult = obesity["Break_Out"] == "18-24"
    early_adult = ((obesity["Break_Out"] == "25-34") |
                   (obesity["Break_Out"] == "35-44"))
    middle_adult = ((obesity["Break_Out"] == "45-54") |
                    (obesity["Break_Out"] == "55-64"))
    older_adult = obesity["Break_Out"] == "65+"
    is_obese = obesity["Response"] == "Obese (BMI 30.0 - 99.8)"

    # make a copy of the dataframe to rename columns
    filtered_obesity = obesity.loc[is_obese & (young_adult |
                                               older_adult)].copy()
    filtered_obesity["Break_Out"] = filtered_obesity["Break_Out"]. \
        replace({"18-24": "18 to 24 Years"})
    filtered_obesity["Break_Out"] = filtered_obesity["Break_Out"].\
        replace({"65+": "65 Years and Older"})
    # print(filtered_obesity)

    # create an early adult df to combine the two early adult age ranges
    early_adult_df = obesity.loc[is_obese & early_adult]
    early_adult_grouped = early_adult_df.groupby(["GeoLocation",
                                                  "Year"])["Data_value"].mean()
    early_adult_grouped = early_adult_grouped.reset_index()
    early_adult_grouped["Break_Out"] = ["25 to 44 Years"] * \
        len(early_adult_grouped)
    # print(early_adult_grouped)
    new_df = pd.concat([filtered_obesity, early_adult_grouped])

    # create an middle adult df to combine the two middle adult age ranges
    middle_adult_df = obesity.loc[is_obese & middle_adult]
    middle_adult_grouped = middle_adult_df.groupby(
        ["GeoLocation", "Year"])["Data_value"].mean()
    middle_adult_grouped = middle_adult_grouped.reset_index()
    middle_adult_grouped["Break_Out"] = ["45 to 64 Years"] * \
        len(early_adult_grouped)
    # print(middle_adult_grouped)
    new_df = pd.concat([new_df, middle_adult_grouped])
    # print(new_df)
    return new_df


def main():
    # load the data
    tabacco = cd.tabacco_clean('https://raw.githubusercontent.com/DevinaT'
                               '/CSE163/main/Tobacco.csv')
    obesity = cd.obesity_cleaned('https://raw.githubusercontent.com/DevinaT'
                                 '/CSE163/main/Obesity.csv')

    tabacco = q1_filter_tabacoo(tabacco)
    obesity = q1_filter_obesity(obesity)

    fig = go.Figure()
    fig.add_trace(go.Violin(y=tabacco["Data_Value"], x=tabacco["Age"],
                            box_visible=True, name="Tabacco"))
    fig.add_trace(go.Violin(y=obesity["Data_value"], x=obesity["Break_Out"],
                            box_visible=True, name="Obesity"))

    fig.update_layout(title="Change in Distribution of Obesity and"
                            " Tabacco Use With Age",
                      xaxis_title="Age Range",
                      yaxis_title="Percent With Risk Factor",
                      legend_title="Risk Factor")
    fig.update_xaxes(categoryorder='array',
                     categoryarray=["18 to 24 Years", "25 to 44 Years",
                                    "45 to 64 Years", "65 Years and Older"])

    fig.show()


if __name__ == "__main__":
    main()

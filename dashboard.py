from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils.DashCard import CardFactory
from utils.DashDropdownMenu import DropDownMenuFactory

data = pd.read_csv("data/Churn_Modelling.csv")

# prepare proportions to display
eq_data_not_exited = data.query('Exited == 0').sample(
    data.query('Exited == 1').shape[0], replace=False)
eq_data = pd.concat([eq_data_not_exited, data.query('Exited == 1')], axis=0)
mean_exited_females = eq_data.query('Gender == "Female"').Exited.mean()
mean_exited_inactive = eq_data.query('IsActiveMember == 0').Exited.mean()
total_exited = data["Exited"].sum()

# stacked bar chart for exited by gender

df_gender_exited = data.groupby(
    'Gender')['Exited'].value_counts(normalize=True).rename('count').to_frame().reset_index()
bar_chart_gender = px.bar(df_gender_exited, x='Gender',
                          y='count', color='Exited', width=922)
bar_chart_gender.update_layout(
    title_text="Exited members per gender", title_x=0.5)

# stacked bar chart for exited by member activity
df_activity_exited = data.groupby(
    'IsActiveMember')['Exited'].value_counts(normalize=True).rename('count').to_frame().reset_index()
bar_chart_activity = px.bar(df_activity_exited, x='IsActiveMember',
                            y='count', color='Exited', width=922)
bar_chart_activity.update_layout(
    title_text="Exited members per activity", title_x=0.5)


# Create navbar for pie chart filters
genders = ['Male', 'Female', 'All']
member_activity = ['Active', 'Inactive', 'All']
age_groups = ['18-25', '25-45', '45-60', '60+', 'All']


def create_pie_chart_filters():
    return dbc.NavbarSimple(
        children=[
            DropDownMenuFactory(dcc).get_instance(
                'dd_gender', genders),
            DropDownMenuFactory(dcc).get_instance(
                'dd_activity', member_activity),
            DropDownMenuFactory(dcc).get_instance(
                'dd_age', age_groups)

        ],
        color="secondary",
        dark=True,
    )


# ---------- Main app ------------------
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

server = app.server


cardFactory = CardFactory(dbc, html)
app.layout = html.Div(
    children=[
        html.H1('Bank Members Exited Dashboard',
                style={"text-align": "center", "margin": "80px", "font-weight": "bold"}),
        html.Div(children=[
            cardFactory.get_simple_card(
                "Total exited", total_exited, [255, 49, 49]),
            cardFactory.get_simple_card(
                "Females who exited", "{:.0f}%".format(mean_exited_females*100), [251, 158, 119]),
            cardFactory.get_simple_card(
                "Inactive members who exited", "{:.0f}%".format(mean_exited_inactive*100), [168, 101, 201])
        ], style={"margin": "30px 100px"}),
        # filters
        create_pie_chart_filters(),
        # graph for proportions per geography
        html.Div(dcc.Graph(id='chart_geography')),
        # graph for actif members per gender
        # TODO need to have same proportions of gender
        html.Div(dcc.Graph(figure=bar_chart_gender),
                 style={"display": "inline-block"}),
        html.Div(dcc.Graph(figure=bar_chart_activity),
                 style={"display": "inline-block"})

    ]
)

# ---------- Callbacks ----

# create callbacks for each drop down item in the navbar


@app.callback(
    Output(component_id="chart_geography", component_property="figure"),
    [
        Input("dd_gender", "value"),
        Input("dd_activity", "value"),
        Input("dd_age", "value")
    ]
)
def get_gender(input_gender, input_activity, input_age):
    gender_filter = "All"
    activity_filter = "All"
    df = data.copy(deep=True)
    if input_gender or input_activity or input_age:
        gender_filter = input_gender
        activity_filter = 0 if input_activity == 'Inactive' else 1
        age_min, age_max = 0, 0
        if input_age:
            if "-" in input_age:
                age_min, age_max = tuple(age for age in input_age.split("-"))
            elif "+" in input_age:
                age_min = input_age.strip("+")
        if input_gender:
            df = df.loc[df.Gender == gender_filter]
        if input_activity:
            df = df.loc[df.IsActiveMember == activity_filter]
        age_min, age_max = int(age_min), int(age_max)
        if age_min > 0:
            if age_max > 0:
                df = df.loc[(df.Age >= age_min) & (df.Age <= age_max)]
            else:
                df = df.loc[df.Age >= age_min]

    df_geography = df.groupby("Geography").Exited.mean().reset_index()
    chart = px.pie(df_geography, values='Exited', names='Geography', hole=0.3)
    chart.update_layout(
        title_text='Exited per country proportions', title_x=0.5)
    return chart


if __name__ == '__main__':
    app.run_server(debug=True)

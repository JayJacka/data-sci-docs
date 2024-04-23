import streamlit as st
import pandas as pd
import pydeck as pdk

# Function to load data


@st.cache_data
def load_data():
    df = pd.read_csv("./RainDaily_Tabular.csv")
    return df


df = load_data()

# Sidebar controls
province = st.sidebar.selectbox(
    'Province', df['province'].unique(), index=None)
start_date = st.sidebar.selectbox(
    'Start Date', df['date'].unique(), index=None)
if start_date:
    end_date_options = df[df['date'] >= start_date]['date'].unique()
    end_date = st.sidebar.selectbox('End Date', end_date_options, index=None)

if start_date:
    if end_date:
        if province:
            filtered_df = df[(df['date'] >= start_date) & (
                df['date'] <= end_date) & (df['province'] == province)]
        else:
            filtered_df = df[(df['date'] >= start_date)
                             & (df['date'] <= end_date)]
    else:
        if province:
            filtered_df = df[(df['date'] >= start_date) &
                             (df['province'] == province)]
        else:
            filtered_df = df[df['date'] >= start_date]
else:
    if province:
        filtered_df = df[df['province'] == province]
    else:
        filtered_df = df


# Main app
st.title('Rain Daily Data Analysis')

# Line chart showing rain in each day
st.write('### Rain in Each Day')
line_chart_data = filtered_df.pivot_table(
    index='date', columns='province', values='rain')
st.line_chart(line_chart_data)

# Bar chart showing rain in each province
st.write('### Rain in Each Province')
bar_chart_data = filtered_df.groupby(
    'province')['rain'].sum().reset_index()
st.bar_chart(bar_chart_data.set_index('province'))

# Function to create map


def create_map(dataframe):
    layer = pdk.Layer(
        "HeatmapLayer",
        dataframe,
        get_position=["longitude", "latitude"],
        get_weight="rain",
        opacity=0.5,
        pickable=True
    )

    if province:
        province_data = dataframe[dataframe['province'] == province]
        view_state = pdk.ViewState(
            longitude=province_data['longitude'].mean(),
            latitude=province_data['latitude'].mean(),
            zoom=9
        )
    else:
        view_state = pdk.ViewState(
            longitude=dataframe['longitude'].mean(),
            latitude=dataframe['latitude'].mean(),
            zoom=9
        )

    return pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/dark-v11", tooltip={"text": "{name}\n{address}"})


# Display Map
st.write('### Map')
map = create_map(filtered_df)
st.pydeck_chart(map)

# Display data
st.dataframe(filtered_df)

max_average_rain_row = filtered_df.groupby('province')['rain'].mean().idxmax()
max_date_with_total_rain = filtered_df.groupby('date')['rain'].sum().idxmax()

st.markdown(f"Province with the highest average rain: {max_average_rain_row}")
st.markdown(f"Date with the highest total rain: {max_date_with_total_rain}")

st.header("Source Code")
with open("./assignment11.py", "r") as f:
    code = f.read()
st.code(code, language="python")

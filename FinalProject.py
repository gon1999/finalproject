'''
Name: Gonzalo de las Casas Stiglich
Date: 04-28-2021
Section: CS230-HB3
File: Final Project
Description: Data Analytics and Streamlit for car crashes in New York from 2015 till now.
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student.
'''
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import random as random

st.title('Vehicle Collisions in New York City')
st.markdown('This applications is a Streamlit dashboard that can be used to analyze vehicle collisions in NYC')


def load_data(nrows):
    data = pd.read_csv('datafile.csv', nrows=nrows)
    data.dropna(subset=['LATITUDE', 'LONGITUDE', 'BOROUGH'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


data = load_data(6000)


def read_file(datafile):
    df = pd.read_csv(datafile)
    df.dropna(subset=['LATITUDE', 'LONGITUDE', 'BOROUGH'], inplace=True)
    df_new = df.rename(columns={'LONGITUDE': 'lon', 'LATITUDE': 'lat'})
    return df_new


def bar_chart(borough, persons_injured, title):
    a = random.random()
    b = random.random()
    c = random.random()
    color = (a, b, c)

    plt.bar(borough, persons_injured, color=color, linewidth=4)
    plt.title(title)


# Map
st.sidebar.title('Map of the vehicle crashes in NYC')

st.header('Where are the most people injured in NYC?')
injured_people = st.sidebar.slider("Number of persons injured in vehicle collisions", 0, 9)
new_data = data[data['persons injured'] == injured_people]
st.map(new_data)


def display_map(data, boroughs, per_injured):
    loc = []
    for i in range(len(data)):
        if data[i][2] in boroughs and per_injured == data[i][5]:
            loc.append([data[i][2], data[i][3], data[i][4]])

    map_df = pd.DataFrame(loc, columns=['boroughs', 'lat', 'lon'])

    view_state = pdk.ViewState(latitude=map_df['lat'].mean(), longitude=map_df['lon'].mean(), zoom=10, pitch=0)
    layer = pdk.Layer("ScatterplotLayer", data=map_df, get_position='[lon, lat]', get_radius=50,
                      get_color=[0, 255, 255], pickable=True)
    tool_tip = {'html': 'Borough:<br/>{Borough}', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer],
                   tooltip=tool_tip)

    st.pydeck_chart(map)


def droplist():
    st.header('Top 5 dangerous streets by affected type')
    select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])
    if select == 'Pedestrians':
        df = data[['on street name', 'pedestrians injured', 'vehicle 1 type']].sort_values(by=['pedestrians injured'],
                                                                                           ascending=[False]).dropna()
        df = df.nlargest(5, 'pedestrians injured')
    elif select == 'Cyclists':
        df = data[['on street name', 'cyclists injured', 'vehicle 1 type']].sort_values(by=['cyclists injured'],
                                                                                        ascending=[False]).dropna()
        df = df.nlargest(5, 'cyclists injured')
    elif select == 'Motorists':
        df = data[['on street name', 'motorists injured', 'vehicle 1 type']].sort_values(by=['motorists injured'],
                                                                                         ascending=[False]).dropna()
        df = df.nlargest(5, 'motorists injured')
    st.write(df)


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df_new = read_file("datafile.csv")
    st.sidebar.header('Vehicle crashes in NYC by borough')

    borough = df_new["BOROUGH"].unique().tolist()
    boroughselection = st.sidebar.multiselect("Select borough", borough)
    borough_dict = {}
    for borough in boroughselection:
        count = 0
        for item in df_new["BOROUGH"].iteritems():
            if item[1] == borough:
                count += 1
            borough_dict[borough] = count

    dictionary = borough_dict.keys()
    updated_dict = list(dictionary)
    new = ', '.join(updated_dict)

    st.write("Selection: ", new)
    title = f'Count of accidents in {new}'
    st.pyplot(bar_chart(borough_dict.keys(), borough_dict.values(), title))

    st.header('Rates of accident in vehicle types in each borough')
    pivot1 = pd.pivot_table(data, values='persons injured', index=['borough'], columns=['vehicle 1 type'])
    st.write("\n", pivot1, "\n")

    droplist()


main()

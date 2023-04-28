import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Covid Spain", page_icon="🦠")

provincias = pd.read_excel("covid_provincias.xlsx")

st.dataframe(provincias)

select_y, select_x = st.columns(2)

with select_y:
    y_field = st.selectbox('Data for Y Axis', options = [e for e in provincias.columns if 'N_' in e])
with select_x:
    x_filed = st.selectbox('Data for X Axis', options = ['Provincia', 'Year_Month'])
    
st.bar_chart(data=provincias, y = y_field, x = x_filed)

st.subheader("ZOOM PROVINCIA")

select_prov, select_y = st.columns(2)

with select_prov:
    provincia_zoom = st.selectbox('Select Provincia: ', options = sorted(list(provincias['Provincia'].unique())))
with select_y:
    y_field_zoom = st.selectbox('Data Y Axis', options = [e for e in provincias.columns if 'N_' in e])
    
st.bar_chart(data = provincias[provincias['Provincia'] == provincia_zoom], y = y_field_zoom, x = 'Year_Month')

st.subheader('MAP')

provincias_map = provincias.groupby('Provincia', as_index = False).sum().drop(['Longitude', 'Latitude'], axis = 1)
provincias_map = pd.merge(provincias_map, provincias[['Provincia', 'Longitude', 'Latitude']].drop_duplicates(), on = 'Provincia', how = 'left')
provincias_map.columns = [e.lower() for e in provincias_map.columns]

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=provincias_map['latitude'].mean(),
        longitude=provincias_map['longitude'].mean(),
        zoom=5,
        pitch=45,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=provincias_map,
           get_position='[longitude, latitude]',
           get_elevation_weight = 'n_cases',
           radius=18000,
           elevation_scale=0.2,
           elevation_range=[provincias_map['n_cases'].min(), provincias_map['n_cases'].max()],
           pickable=True,
           extruded=True,
           coverage = 1,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=provincias_map[['n_cases', 'latitude', 'longitude']],
            get_position='[longitude, latitude]',
            get_color='[300, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))


st.dataframe(provincias_map)


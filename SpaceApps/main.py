import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import openai

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key' #add open ai api key

# Title of your web app
st.title('Pluto Emissions Map')

# Load the 2018 and 2022 emission data
data_2018 = pd.read_csv('2018.csv')
data_2022 = pd.read_csv('2022.csv')

# Coordinates for Seattle map center
map_center = [47.6062, -122.3321]  # Seattle coordinates

# Sidebar: ChatGPT Assistant
st.sidebar.title("ChatGPT Assistant")
st.sidebar.write("Ask me anything about emissions or environmental data!")

# Text input for user query
user_input = st.sidebar.text_input("You:", "")

# # Function to get a response from the OpenAI API
# def get_chatgpt_response(user_input):
#     if user_input:
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant that provides information about carbon emissions and environmental data in seattle. Make the answer understandable for people of all ages. Your goal is help people get answers about carbon emmision in their neighborhood and help take actions like contacting goverment offices to make change happen"},
#             {"role": "user", "content": user_input}
#         ]
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages
#         )
#         return response['choices'][0]['message']['content']
#     return ""

# # Display response if the user enters a query
# if st.sidebar.button("Send"):
#     if user_input:
#         with st.spinner("Thinking..."):
#             bot_response = get_chatgpt_response(user_input)
#             st.sidebar.text_area("Assistant:", bot_response, height=200)
#     else:
#         st.sidebar.error("Please enter a message!")

def get_chatgpt_response(user_input):
    if user_input:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides information about carbon emissions and environmental data in Seattle. Make the answer understandable for people of all ages. Your goal is to help people get answers about carbon emissions in their neighborhood and help take actions like contacting government offices to make change happen. Make the answer understandable for people of all ages. Make the answers brief as well"},
            {"role": "user", "content": user_input}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response['choices'][0]['message']['content']
    return ""

# Display response if the user enters a query
if st.sidebar.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            bot_response = get_chatgpt_response(user_input)
            st.sidebar.markdown(f"### Assistant:\n\n{bot_response}")  # Display response in Markdown for better readability
    else:
        st.sidebar.error("Please enter a message!")

# st.text('Currently showing total carbon emissions (ppm) in Seattle from 2018 to 2022')
import streamlit.components.v1 as components
# # components.html("<p>Currently showing total carbon emissions (ppm) in Seattle from 2018 to 2022</p>")

components.html("""
    <p style="color:white; font-size:24px;">
        Currently showing total carbon emissions (metric tons) in Washington from 2018 to 2022
    </p>
""")


# First Map: 2018 Emissions Map
st.subheader('2018 Emissions Map')

# Create a Folium map centered on Seattle for 2018
emission_map_2018 = folium.Map(location=map_center, zoom_start=12)

# Prepare data for the heatmap for 2018
heat_data_2018 = [[row['Latitude'], row['Longitude'], row['Emission Value']] for index, row in data_2018.iterrows()]

# Add heatmap layer to the map for 2018
HeatMap(heat_data_2018, radius=50).add_to(emission_map_2018)

# Add markers (pinpoints) with clickable links in the popup for 2018 map
pinpoint_data_2018 = [
    {"location": [47.9790, -122.2021], "title": "Everett Electric Battery Bus", "link": "https://seattletransitblog.com/2018/09/22/everett-transit-debuts-its-first-electric-battery-bus/"},
    {"location": [47.6221, -122.3541], "title": "Climate Pledge Arena", "link": "https://www.seattletimes.com/opinion/editorials/climate-pledge-arena-sure-lets-skate-with-it/"},
    {"location": [47.5952, -122.3328], "title": "Seattle Building Emissions Change", "link": "https://www.seattle.gov/environment/climate-change/buildings-and-energy/building-emissions-performance-standard/beps-policy-development"}
]

# Adding the pinpoints with popups to the 2018 map
for pinpoint in pinpoint_data_2018:
    folium.Marker(
        location=pinpoint["location"],
        popup=f'<strong>{pinpoint["title"]}</strong><br><a href="{pinpoint["link"]}" target="_blank">More info</a>',
        icon=folium.Icon(icon="info-sign", color="blue")
    ).add_to(emission_map_2018)

# Add markers (or circles) with tooltips for 2018 emissions
for index, row in data_2018.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=7,  # Size of the marker
        color='transparent',  # Marker color
        fill=False,
        fill_opacity=0.0,
        tooltip=f"Total Emission: {row['Emission Value']} meteric tons"
    ).add_to(emission_map_2018)

# Display the 2018 map in Streamlit
folium_static(emission_map_2018)

# Add some space between the maps
st.write("\n")  # or use st.markdown("<br><br>", unsafe_allow_html=True) for more spacing

# Second Map: 2022 Emissions Map
st.subheader('2022 Emissions Map')

# Create a Folium map centered on Seattle for 2022
emission_map_2022 = folium.Map(location=map_center, zoom_start=12)

# Prepare data for the heatmap for 2022
heat_data_2022 = [[row['Latitude'], row['Longitude'], row['Emission Value']] for index, row in data_2022.iterrows()]

# Add heatmap layer to the map for 2022
HeatMap(heat_data_2022, radius=50).add_to(emission_map_2022)

# Add markers (pinpoints) with clickable links in the popup for 2022 map
pinpoint_data_2022 = [
    {"location": [47.9790, -122.2021], "title": "Everett Electric Battery Bus", "link": "https://seattletransitblog.com/2018/09/22/everett-transit-debuts-its-first-electric-battery-bus/"},
    {"location": [47.6221, -122.3541], "title": "Climate Pledge Arena", "link": "https://www.seattletimes.com/opinion/editorials/climate-pledge-arena-sure-lets-skate-with-it/"},
    {"location": [47.5952, -122.3328], "title": "Seattle Building Emissions Change", "link": "https://www.seattle.gov/environment/climate-change/buildings-and-energy/building-emissions-performance-standard/beps-policy-development"}
]

# Adding the pinpoints with popups to the 2022 map
for pinpoint in pinpoint_data_2022:
    folium.Marker(
        location=pinpoint["location"],
        popup=f'<strong>{pinpoint["title"]}</strong><br><a href="{pinpoint["link"]}" target="_blank">More info</a>',
        icon=folium.Icon(icon="info-sign", color="green")
    ).add_to(emission_map_2022)

# Add markers (or circles) with tooltips for 2022 emissions
for index, row in data_2022.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=7,  # Size of the marker
        color='transparent',  # Marker color
        fill=False,
        fill_opacity=0.0,
        tooltip=f"Total Emission: {row['Emission Value']} meteric tons"
    ).add_to(emission_map_2022)

# Display the 2022 map in Streamlit
folium_static(emission_map_2022)

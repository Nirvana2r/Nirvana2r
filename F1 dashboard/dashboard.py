# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 11:39:20 2022

@author: nirva
"""

import streamlit as st
import plotly.express as px
from f1_scraping import df_team
from f1_scraping import df_fast1
from f1_scraping import df_fast2
from f1_scraping import df_fast3
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from PIL import Image
import requests
from io import BytesIO
#from utils import chart
#df = pd.read_csv('C:/Users/nirva/Desktop/Python scripts/F1 dashboard/dff11111.csv')




#df.info()

# selectbox
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Navigation",
    ("Home", "1st study", "2nd study","Souces")
)




if add_selectbox == "Home":
    
    st.title(' The evolution of F1 constructors performance')
    st.markdown('Interested in the evolution of technology, the world of motorsport has piqued my interest in recent years. Formua 1 has a huge history of car evolution and technology breakthroughs. Having the single goal to be the fastest car on the track, constructors develop innovative ways to improve their cars each year. Being a recent F1 fan I would like to know the evolutions of the constructors.')
    
    

    response = requests.get('https://cdn.wallpapersafari.com/43/51/MCqx04.png')
    image = Image.open(BytesIO(response.content))
    #image = Image.open('https://cdn.wallpapersafari.com/43/51/MCqx04.png')

    st.image(image, caption='F1 Teams logos')

    st.caption('Study by Nirvana Ouedraogo')    

if add_selectbox == "1st study":    
    
    ## First study
    st.header('Constructor Standings from 2012 to 2021 ') 
    st.markdown('This is the official data of the constructors standings')
    
    #Interactive table
    
    options = GridOptionsBuilder.from_dataframe(df_team, enableRowGroup=True, enableValue=True, enablePivot=True )
    options.configure_side_bar()
    options.configure_selection("single")
    
    selection = AgGrid(
        df_team,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,)
    
    if selection:
        st.write("You selected:")
        st.json(selection["selected_rows"])
    
    st.caption('The official constructor names have changed through the years whit the changes of owner and sponsorships. For the purpose of the study, we updates the passt constructor names to there 2021 names.')
    
    '''
    #Interactive chart
    source = df_team.team()
    all_symbols = source.symbol.unique()
    symbols = st.multiselect("Choose the team to visualize", all_symbols, all_symbols[:3])
    
    source = source[source.symbol.isin(symbols)]
    chart = chart.get_chart(source)
    st.altair_chart(chart, use_container_width=True)
    '''
    
    #Line chart
    st.header('The Evolution of all 10 constructors')
    
    chart_data = px.line(df_team, x='year', y='pts', color='team',template='presentation')
    chart_data.update_yaxes(categoryorder="category ascending")  
    st.plotly_chart(chart_data)
    
    st.markdown("As we can see from the graph, today's top construstor evolved gradualy though the years while some left their top spot."
                "This can be expleind by the change budget, sponsors and team pricipal." )
    
    #Bar chart
    st.subheader('Close comparation of all 10 constructors')
    
    fig_bar = px.bar(df_team, x= 'year', y='pts', color ='team', barmode="group", orientation='v',)
    st.plotly_chart(fig_bar)
    
    st.markdown("Here we can have a close comparation of all team per year.")

if add_selectbox == "2nd study":
    ## Second study
    st.header('Every fast car per Grand Prix from 2020 to 2022') 
    
    #Dot Plots chart
    
    st.subheader('Fastest in 2021')
    fig = px.scatter(df_fast1, x="Time", y="Grand Prix", color="Car")
    fig.update_xaxes(categoryorder='category descending')
    fig.update_traces(marker_size=10)
    st.plotly_chart(fig)
    
    st.subheader('Fastest in 2020')
    fig2 = px.scatter(df_fast2, x="Time", y="Grand Prix", color="Car")
    fig2.update_xaxes(categoryorder='category descending')
    fig2.update_traces(marker_size=10)
    st.plotly_chart(fig2)
    
    st.subheader('Fastest in 2019')
    fig3 = px.scatter(df_fast3, x="Time", y="Grand Prix", color="Car")
    fig3.update_xaxes(categoryorder='category descending')
    fig3.update_traces(marker_size=10)
    st.plotly_chart(fig3)
    st.markdown(" It's intresting to have a look on the cars that made the fastes lap time in each grand prix."
                "Every circuit is diferent and can change whit weather conditions"
                "We can see that the best Teams haves won most of the DHL fastes lap due to the amazing performence of their cars.")

if add_selectbox == "Souces": 
    st.header('Souces') 
    
    txt = """
    Data Playground courses by Lars Heemskerk

    - Webscraping
    
    HU course in Week 3: Webscraping 
    -Scrape a single webpage (Video)
    -Scraping multiple webpages (Video)
    https://www.formula1.com/en/results.html
    https://www.studytonight.com/python/web-scraping/scraping-multiple-urls
    https://www.geeksforgeeks.org/print-lists-in-python-4-different-ways/
    https://statisticsglobe.com/rename-columns-of-pandas-dataframe-in-python
    https://wtf1.com/post/these-are-all-the-f1-team-changes-in-the-last-decade/
    https://pythonguides.com/pandas-replace-multiple-values/
    https://datascienceparichay.com/article/pandas-delete-rows-based-on-column-values/
    
    - Dashbord
    
    https://docs.streamlit.io/library
    https://www.codegrepper.com/code-examples/python/how+to+import+a+variable+from+another+python+file
    https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
    https://plotly.com/python/basic-charts/
    https://plotly.com/python/categorical-axes/
    https://share.streamlit.io/streamlit/example-app-interactive-table/main
    https://docs.streamlit.io/library/api-reference/layout/st.sidebar
    https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
        """
    st.markdown(txt)
    st.caption("Credits: This projet would not be posible whit the help of professor lars Heemskerk cours and classmates")
    
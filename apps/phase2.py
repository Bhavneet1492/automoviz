# importing the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit.components.v1 as components

def app():

    # adding the title of the app
    st.title("Data Visualization")
    st.markdown("""<hr>""",True)

    # components.iframe("https://app.powerbi.com/reportEmbed?reportId=e515157c-e94f-42d5-9130-1814f656d83f&autoAuth=true&ctid=17d0548a-56d6-4f84-91f7-2ca19d833d8c&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLXdlc3QtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQvIn0%3D",width=930,height=550)

    sample=pd.read_csv("./datasets/cars_cat.csv")
        
    #selecting a dataset (sample/uploaded)
    choice=st.radio("Select the dataset you want to use",['sample dataset','upload a dataset'],key=154)
        
    # setting the df variable as the selected dataset
    if choice=='sample dataset':
        df=sample
    else:
        # uploading the dataset
        data=st.file_uploader("upload here")
        st.markdown("""
                <style>
                    .note{
                        color:#FF855E;
                        font-size:1rem;
                        font-weight:200;
                        transition:0.3s linear;
                        cursor:default;
                    }
                </style>

                <h2 class="note">Note: the uploaded dataset miust have the same format as the sample dataset (column names may be different but their positioning should be the same). You can refer to the sample dataset under the 'View Data' tab.</h2>
                
                """,True)
        if data:df=pd.read_csv(data)
        else:
            df=sample
            st.markdown("""
                
                <style>
                .warning{
                    color:#64ADFF;
                    font-size:1rem;
                    font-family:monospace;
                    font-weight:200;
                }
                </style>
                <h2 class="warning">Currently viewing sample dataset. Please upload a dataset in order to view it.</h2>
                
                """,True)

        # raise an error if the upploaded dataset needs to be viewed but no dataset has been uploaded 
    try:
        with st.expander("View Data"):
            with st.spinner(text="Spreading the table..."):
                time.sleep(1)
                st.dataframe(df,None,None)
                st.write(df.shape)    
    except:
        st.error("⚠️ Upload a datset")

    col1,col2=st.columns(2)
    col3,col4=st.columns(2)
    col5,col6=st.columns(2)

    with col1:
        cols=st.multiselect("LINE CHART",df.columns,key=876890,default=["Displacement","Ex-Showroom_Price"])
        if len(cols)!=2:
            st.error("⚠️ Select two columns")
        else:
            line = alt.Chart(df).mark_line(color="#7CE39F").encode(x=cols[0],y=cols[1],tooltip=cols).interactive()
            st.altair_chart(line,use_container_width=True)
    
    with col2:
        cols=st.multiselect("BAR CHART",df.columns,key=8812920,default=["2019","Audiosystem"])
        if len(cols)!=2:
            st.error("⚠️ Select two columns")
        else:
            bar = alt.Chart(df).mark_bar(color="#FF855E").encode(x=cols[0],y=cols[1],tooltip=cols).interactive()
            st.altair_chart(bar,use_container_width=True)
    
    with col3:
        cols=st.multiselect("AREA CHART",df.columns,key=8876920,default=["2019","Cylinders"])
        if len(cols)!=2:
            st.error("⚠️ Select two columns")
        else:
            chart=alt.Chart(df).mark_area(color="#2A86CA").encode(
            x=cols[0],y=cols[1],tooltip=cols).interactive()
            st.altair_chart(chart,use_container_width=True)
    
    with col4:
        cols=st.multiselect("LAYERED HISTOGRAM",df.columns,key=8863920,default=["Length","Width","Height"])
        if len(cols)!=3:
            st.error("⚠️ Select three columns")
        else:
            chart=alt.Chart(df).transform_fold(
            [cols[0], cols[1],cols[2]],
            as_=['Experiment', 'Measurement']
            ).mark_bar(
            opacity=1,
            binSpacing=0
            ).encode(
            alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
            alt.Y('count()', stack=None),
            alt.Color('Experiment:N'),tooltip=cols).interactive()
            st.altair_chart(chart,use_container_width=True)
    
    with col5:
        cols=st.multiselect("PIE CHART",df.columns,key=8834920,default=["Fuel_Type","2020"])
        if len(cols)!=2:
            st.error("⚠️ Select two columns")
        else:
            #The plot
            fig = go.Figure(
                go.Pie(
                labels = df[cols[0]],
                values = df[cols[1]],
                hoverinfo = "label+percent"
            ))
            st.plotly_chart(fig,use_container_width=True)
    
    with col6:
        cols=st.multiselect("BOX PLOT",df.columns,key=88965420,default=["Body_Type","Displacement"])
        if len(cols)!=2:
            st.error("⚠️ Select two columns")
        else:
            fig = px.box(df, x=cols[0], y=cols[1])
            st.plotly_chart(fig,use_container_width=True)
        
    
    cols=st.multiselect("SCATTER PLOT",df.columns,key=8896520,default=["Make","2010","Seats_Material"])
    if len(cols)!=3:
        st.error("⚠️ Select three columns")
    else:
        chart=alt.Chart(df).mark_circle().encode(
        x=cols[0],
        y=cols[1],
        color=cols[2],tooltip=cols
        ).interactive()
        st.altair_chart(chart,use_container_width=True)
    
    
        
        
            
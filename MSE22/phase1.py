# importing the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import seaborn as sns
import scipy as sc
import matplotlib.pyplot as plt
import plotly.express as px

def isaln(x):
    for c in x:
        if c.isdigit():return True

st.set_page_config(
     page_title="Data cleaning",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",
)

st.title('Data Cleaning')
st.markdown("""<hr>""",True)


# st.markdown("""<style>
# .banner{width:100%;
# background:linear-gradient(to right, #005DB4 , #73DDFF);
# animation: gradient 8s linear infinite;
# display:flex;
# align-items:center;
# justify-content:center;
# color:transparent;
# font-size:0.1rem;
# }
# @keyframes gradient {
#   0%,
#   100% {
#     filter: hue-rotate(-30deg);
#   }
#   50% {
#     filter: hue-rotate(60deg);
#   }
# }

# </style>
# <br>
# <div class="banner">
# hello
# </div>
# <br>
# """, unsafe_allow_html=True)


st.sidebar.selectbox("select operation",['Data Cleaning','Data Visualization','Make Predictions','Business Insights','Customer Segmentation'])
col1, col2= st.columns(2)

with col1:
  st.markdown(""" ### The data """)

  # the sample dataset
  sample=pd.read_csv("./datasets/specifications.csv")
  
  choice=st.radio("select the dataset you want to use",['sample dataset','upload a dataset'],key=14)
  
  # selecting a dataset (sample/uploaded)
  if choice=='sample dataset':
    df=sample
  else:
    data=st.file_uploader("upload here")
    if data:df=pd.read_csv(data)
      
  try:
    with st.expander("View Data"):
      with st.spinner(text="Spreading the table..."):time.sleep(1)
      st.dataframe(df,None,None)
      st.write(df.shape)    
  except:
    st.error("⚠️ Upload a datset")

    # ---------------------------------------- #
    
  st.markdown(""" <hr> """,True)
  st.markdown(""" ### Cleaning booth """)
  with st.expander("Drop unnecessary columns "):
      cols=st.multiselect("select the column(s) to drop",df.columns,key=15)
      df.drop(cols,axis=1,inplace=True)
      if st.button('view updated dataset',key=90):
          st.dataframe(df)
          st.write(df.shape)

  with st.expander("Handle missing values"):
      choice=st.radio("Select the desired method",['None','Drop column(s)','Drop row(s)','Fill in null values','Imputation'],key=34)
      if choice=='Drop column(s)':
        df.dropna(how='any',axis=1,inplace=True)
        if st.button('view updated dataset',key=78):
            st.dataframe(df)
            st.write(df.shape)
        if choice=='Drop row(s)':
            df.dropna(how='any',inplace=True)
            if st.button('view updated dataset',key=114):
                st.dataframe(df)
                st.write(df.shape)
  with st.expander("Filter digits from string"):
      cols=st.multiselect("select the column(s)",df.columns,key=5252)
  with st.expander("Datatype conversion"):
      cols=st.multiselect("select the column(s) to convert",df.columns,key=525)
      choice=st.radio("Change the datatype to",['None','integer','float','string'],key=514)
  with st.expander("Encode categorical data"):
      choice=st.radio("Select the desired method",['None','Label encoder','One hot encoder'],key=54)
      cols=st.multiselect("select the column(s) to encode",df.columns,key=55)
  with st.expander("Smoothen the data"):st.write('hello')
  with st.expander("Normalization / with Standard scaling"):st.write('hello')
  with st.expander("Outliers and plots"):st.write('hello')
  with st.expander("Heatmaps / Correlation matrices"):st.write('hello')


with col2:
  st.markdown(""" ### Raw data profile """)

  try:
      choice=st.radio("Viewing format",['Overall','Column-wise'],key=24)
      if choice=='Overall':
          num,alnum,alpha,integer,flt=0,0,0,0,0
          null=df.isnull().sum().sum()
          for i in df:
              for e in df[i]:
                  if type(e)==int:integer+=1
                  elif type(e)==float:flt+=1
                  elif type(e)==str:
                      if e.isnumeric():num+=1
                      if e.isalpha():alpha+=1
                      if isaln(e):alnum+=1
          
          source = pd.DataFrame({
          'Datatype': ['null', 'integers', 'float', 'categorical', 'numbers as pure strings', 'strings with digits'],
          'Number of columns': [null,integer,flt,alpha,num,alnum]
      })
            
  
          chart=alt.Chart(source).mark_arc(innerRadius=45).encode(
    theta=alt.Theta(field="Number of columns", type="quantitative"),
    color=alt.Color(field="Datatype", type="nominal"),tooltip=['Datatype','Number of columns']
)
          st.altair_chart(chart,use_container_width=True)
  
      elif choice=='Column-wise':
          num,alnum,alpha,integer,flt=0,0,0,0,0
          for i in df.columns:
                  if type(df[i][0])==int:integer+=1
                  elif type(df[i][0])==float:flt+=1
                  elif type(df[i][0])==str:
                      if df[i][0].isnumeric():num+=1
                      if df[i][0].isalpha():alpha+=1
                      if isaln(df[i][0]):alnum+=1
          
          source = pd.DataFrame({
          'Datatype': ['null', 'integers', 'float', 'categorical', 'numbers as pure strings', 'strings with digits'],
          'Number of columns': [df.isnull().any().sum(),integer,flt,alpha,num,alnum]
      })
          
          chart=alt.Chart(source).mark_bar().encode(
          x='Datatype',
          y='Number of columns',tooltip=['Datatype','Number of columns']
      )   
      
          st.altair_chart(chart,use_container_width=True)
  
          col=st.selectbox("select column",df.columns,key=1)
  
          num,alnum,alpha,integer,flt=0,0,0,0,0
          for i in df[col]:
                  if type(i)==int:integer+=1
                  elif type(i)==float:flt+=1
                  elif type(i)==str:
                      if i.isnumeric():num+=1
                      if i.isalpha():alpha+=1
                      if isaln(i):alnum+=1
          
          source = pd.DataFrame({
          'Datatype': ['null', 'integers', 'float', 'categorical', 'numbers as pure strings', 'strings with digits'],
          'Number of elements': [df[col].isnull().sum(),integer,flt,alpha,num,alnum]
      })
          
          chart=alt.Chart(source).mark_bar().encode(
          x='Datatype',
          y='Number of elements',tooltip=['Datatype','Number of elements']
      )   
  
          st.altair_chart(chart,use_container_width=True)
  
  except:
      st.error("⚠️ Select a datset")

  st.markdown(""" <hr> """,True)
  st.markdown(""" ### Raw data visualization """)
    
  

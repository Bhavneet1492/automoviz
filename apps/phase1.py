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
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, LabelEncoder,StandardScaler
import plotly.figure_factory as ff
import streamlit.components.v1 as components

#function to check if a string contains any digits
def isaln(x):
    for c in x:
        if c.isdigit():return True

# #setting the page configuration
# st.set_page_config(
#     page_title="Data cleaning",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

def app():

    # adding the title of the app
    st.title('Data Cleaning')
    st.markdown("""<hr>""",True)
    
    st.markdown("""

    <style>
     a{
         text-decoration:none;
         color:cyan;
         transition:0.2s ease-in-out;
         font-size:1.5rem;
      }
     a:hover{
         opacity:0.6;
         text-decoration:none;
      }
    </style>

    <a href="https://bhavneet1492.github.io/Data-Cleaning/" target=“_blank”>How to clean your data?</a>
    """,True)

    col1, col2= st.columns(2)

    with col1:
        st.markdown(""" ### The data """)

        # the sample dataset
        sample=pd.read_csv("./datasets/specifications.csv")
        
        #selecting a dataset (sample/uploaded)
        choice=st.radio("select the dataset you want to use",['sample dataset','upload a dataset'],key=14)
        
        # setting the df variable as the selected dataset
        if choice=='sample dataset':
            df=sample
        else:
            # uploading the dataset
            data=st.file_uploader("upload here")
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
            with st.expander("View Data",expanded=True):
                with st.spinner(text="Spreading the table..."):
                    time.sleep(1)
                    st.dataframe(df,None,None)
                    st.write(df.shape)    
        except:
            st.error("⚠️ Upload a datset")

            # ---------------------------------------- #
            


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
    st.markdown(""" ### Cleaning booth """)
        
    """
        Each of the following functions can be performed in order to clean the dataset:
            ->feature reduction
            ->handling missing values
            ->filterring digits from strings
            ->encoding categorical data
            ->smoothening the data
            ->handling outliers
            ->viewing correlations
    """
    colq,colx,coly,colz=st.columns(4)
    with colx:        
        with st.expander("Filter digits from string"):
            cols=st.multiselect("select the column(s)",df.columns,key=5252)
            for i in cols:
                if df[i].dtype=="object":
                    df[i]=df[i].str.replace(r'\D','')
                    df[i]=pd.to_numeric(df[i])
            if cols:
                col=st.selectbox("view converted columns",cols)
                st.write(df[col])
    with coly:
        with st.expander("Datatype conversion"):
            cols=st.multiselect("select the column(s) to convert",df.columns,key=525)
            choice=st.radio("Change the datatype to",['None','integer','float','category'],key=514)
            if choice=='integer':
                for i in cols:
                    try:
                        df[i]=df[i].astype('int64')
                    except:
                        st.error(f"conversion of {i} is not possible")
            if choice=='float':
                for i in cols:
                    try:
                        df[i]=df[i].astype('float')
                    except:
                        st.error(f"conversion of {i} is not possible")
            if choice=='category':
                for i in cols:
                    try:
                        df[i]=df[i].astype('category')
                    except:
                        st.error(f"conversion of {i} is not possible")
    with colz:
        with st.expander("Encode categorical data"):
            choice=st.radio("Select the desired method",['None','Label encoder','One hot encoder'],key=54)
            cols=st.multiselect("select the column(s) to encode",df.columns,key=55)
            if choice=="Label encoder":
                le=LabelEncoder()
                for i in cols:
                        if df[i].dtypes==object:
                            df[i]=le.fit_transform(df[[i]])
            if choice=="One hot encoder":
                ohe=OneHotEncoder()
                for i in cols:
                        if df[i].dtypes==object:
                            df[i]=ohe.fit_transform(df[[i]])
            if cols:
                col=st.selectbox("view converted columns",cols)
                st.write(df[col])
    
    
        with colq:
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
    
    with colq:
        with st.expander("Feature reduction"):
            choice=st.radio("Select the desired method",['None','PCA','Drop column(s)'],key=343)
            if choice=='Drop column(s)':
                cols=st.multiselect("select the column(s) to drop",df.columns,key=15)
                df.drop(cols,axis=1,inplace=True)
                if st.button('view updated dataset',key=90):
                    st.dataframe(df)
                    st.write(df.shape)
            if choice=='PCA':
                st.markdown("""
                
                <style>
                a{
                    text-decoration:none;
                    color:cyan;
                    transition:0.2s ease-in-out;
                }
                a:hover{
                    opacity:0.6;
                    text-decoration:none;
                }
                </style>
                <a href="https://en.wikipedia.org/wiki/Principal_component_analysis">What is PCA?</a>
                
                """,True)
                
                n = st.slider('Choose the number of components', 0, df.shape[1], 1)
                
                pca = PCA(n_components = n)

                try:
                    pca.fit(df)
                    df = pca.transform(df)
                except:
                    st.error("An error occured")
                
                if st.button('view updated dataset',key=940):
                    st.dataframe(df)
                    st.write(df.shape)        
        
        with colx:
            with st.expander("Smoothen the data"):
                cols=st.multiselect("select the column(s) to drop",df.columns,key=15)
                alpha=st.slider("Set alpha",0.0,1.0,step=0.1)
                for i in cols:
                    if ((df[i].dtype=='int64') or (df[i].dtype=="float")):
                        df[i]=df[i].ewm(alpha=alpha).mean()
                if cols:
                    col=st.selectbox("view converted columns",cols)
                    st.write(df[col])
        with coly:
            with st.expander("Standard scaling"):
                cols=st.multiselect("select the column(s) to drop",df.columns,key=1325)
                scale= StandardScaler()
                for i in cols:
                    if ((df[i].dtype=='int64') or (df[i].dtype=="float")):
                        df[i]=scale.fit_transform(np.array(df[i]).reshape(-1,1))
                if cols:
                    col=st.selectbox("view converted columns",cols)
                    st.write(df[col])
        with colz:
            # downoading the cleaned data file
            @st.cache
            def convert_df(df):
                return df.to_csv().encode('utf-8')
            csv = convert_df(df)
            st.download_button(
                label="Download the cleaned data",
                data=csv,
                file_name='cleaned_df.csv',
                mime='text/csv',
            )
    st.markdown("""
     <style>
        .note{
            color:coral;
            font-size:1rem;
            font-family:monospace;
            font-weight:200;
            }
        </style>
     <h2 class="note">Note: Standard scaling, feature reduction using pca, normalization and data smoothening is not recommended for all columns since it may cause loss of important information such as the price of each car and its sales</h2> """,True)
    st.markdown(""" <hr> """,True)  
    st.markdown(""" ### Raw data visualization """)

    cola,colb=st.columns(2)
    with cola:
        cols=st.multiselect("Select upto two columns for visualization",df.columns,key=8890,default=['Audiosystem','Ex-Showroom_Price'])

        def display_error(n):
            st.error("⚠️ Select ",n, "columns")
            
        st.markdown("#### datatypes")
        st.write(cols[0],":",df[cols[0]].dtype)
        st.write(cols[1],":",df[cols[1]].dtype)

        if st.checkbox('View Box Plot',value=True):
            if len(cols)!=2:display_error(2)
            else:
                fig = px.box(df, x=cols[0], y=cols[1])
                st.plotly_chart(fig,use_container_width=True)

    with colb:

        col=st.selectbox("Select a feature",df.columns,key=88940)

        st.markdown("#### datatype")
        st.write(col,":",df[col].dtype)

        if st.checkbox('View Histogram',value=True):
            fig = px.histogram(df, x=col)
            st.plotly_chart(fig,use_container_width=True)
              

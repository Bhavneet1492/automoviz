# importing the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from PIL import Image

def app():

    # adding the title of the app
    st.title("Customer segmentation")
    st.markdown("""<hr>""",True)

    # components.iframe("https://app.powerbi.com/reportEmbed?reportId=e515157c-e94f-42d5-9130-1814f656d83f&autoAuth=true&ctid=17d0548a-56d6-4f84-91f7-2ca19d833d8c&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLXdlc3QtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQvIn0%3D",width=930,height=550)

    sample=pd.read_csv("./datasets/customers.csv")
        
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

    #handling missing data values
    for i in df.columns:
        df[i].fillna(df[i].mode()[0], inplace=True)
    
    # raise an error if the upploaded dataset needs to be viewed but no dataset has been uploaded 
    try:
        with st.expander("View Data",expanded=True):
            with st.spinner(text="Spreading the table..."):
                time.sleep(1)
                st.dataframe(df,None,None)
                st.write(df.shape)    
    except:
        st.error("⚠️ Upload a datset")
    
    st.markdown("""<hr>""",True)

    #creating histograms of the count of features
    st.header("Visualizations")
    def hist(feature,color,size=20,binned=False):
        if binned:
            hist = alt.Chart(df).mark_bar(color=color,size=size).encode(x=alt.X(feature, bin = alt.BinParams(maxbins = 10)),y = 'count()',tooltip=[feature,'count()']).interactive()
        else:
            hist = alt.Chart(df).mark_bar(color=color,size=size).encode(x=feature,y = 'count()',tooltip=[feature,'count()']).interactive()
        st.altair_chart(hist,use_container_width=True)
    col1,col2,col3=st.columns(3)
    with col1:
        hist('Gender',"#7CE39F")
        hist('Profession',"#FF855E",10)
        hist('FamilySize',"#B0E37C",10)
    with col2:
        hist('Married',"#B0E37C")
        hist('WorkExperience',"#2CCDCD",binned=True)
        hist('Category',"#E3DF7C")
    with col3:
        hist('Graduated',"orange")        
        hist('SpendingScore',"#7CE39F")
        hist('Segmentation',"#FF855E")
    hist('Age',"#2CCDCD",binned=True)

    cols=st.columns(4)
    for i in range(len(df.columns)):
        with cols[i%4]:st.metric(f"number of {df.columns[i]}(s)", df[df.columns[i]].nunique())



    st.markdown("""<hr>""",True)

    cola,colb=st.columns(2)
    
    with cola:

        st.subheader("data after cleaning:")

        # categorical encoding of data
        for i in df.columns:
            if df[i].dtype=="object":
                df[i]=pd.factorize(df[i])[0]

        # scaling the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_df=scaler.fit_transform(df)
        scaled_df = pd.DataFrame(data=scaled_df, columns=df.columns)

        # dropping unnecessary coolumns
        scaled_df.drop(["CustomerID","Segmentation"],axis=1,inplace=True)

        # viewing the cleaned data file
        with st.expander("View Data",expanded=True):
            with st.spinner(text="Spreading the table..."):
                time.sleep(1)
                st.dataframe(scaled_df,None,None)
                st.write(scaled_df.shape) 
        
        # downoading the cleaned data file
        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        csv = convert_df(scaled_df)
        st.download_button(
                label="Download cleaned data",
                data=csv,
                file_name='cleaned_df.csv',
                mime='text/csv',
            )
    
    with colb:

        #applying k means clustering to the data
    
        # set the number of clusters
        k = df.Segmentation.nunique()

        # initialize k-means method
        kmeans = KMeans(n_clusters=k, random_state=0, max_iter=1000, n_init=10, verbose=False)

        # predicting the labels
        labels = kmeans.fit_predict(scaled_df)

        # columns without "Category"
        cols = scaled_df.columns[:-1]
        df_res = scaled_df[cols]
        
        # adding the predicted labels
        df_res["Cluster"] = labels
        
        # inserting "CustomerID" column
        df_res.insert(0, "CustomerID", df["CustomerID"])

        st.subheader("data after clustering:")

        # viewing the clustered data file
        with st.expander("View Data",expanded=True):
            with st.spinner(text="Spreading the table..."):
                time.sleep(1)
                st.dataframe(df_res,None,None)
                st.write(df_res.shape) 
        
        # downoading the clustered data file
        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        csv = convert_df(df_res)
        st.download_button(
                label="Download clustered data",
                data=csv,
                file_name='clustered_df.csv',
                mime='text/csv',
            )
    #k means result visualization   
    df_res['index']=np.arange(df_res.shape[0])
    y=np.sort(df_res.CustomerID.unique())
    chart=alt.Chart(df_res).mark_circle(size=25).encode(
    x=alt.Y('index:Q',
        scale=alt.Scale(domain=(0, df_res.shape[0]))
    ),
    y=alt.Y('CustomerID:Q',
        scale=alt.Scale(domain=(y[0], y[df_res.shape[0]-1]))
    ),
    color=alt.Color('Cluster', scale=alt.Scale(scheme='plasma')),
    tooltip=['CustomerID', 'Cluster',"index"]
    ).properties ( width = 'container' , height = 500 ).interactive()
    st.altair_chart(chart,use_container_width=True,)

    st.markdown("""<hr>""",True)

    #reducing dimensions using pca
    st.subheader("Reducing dimensions using PCA")     

    # reduce data to 2 features
    pca = PCA(n_components=2).fit_transform(scaled_df)

    # initializing k-means
    kmeans = KMeans(n_clusters=k, random_state=0, max_iter=1000, n_init=10, verbose=False)

    # predicting the labels of clusters
    labels = kmeans.fit_predict(pca)

    pca_res = pd.DataFrame(pca)
    pca_res["Cluster"] = labels
    pca_res.insert(0, "CustomerID", df["CustomerID"])

    # viewing the reduced data file
    with st.expander("View reduced data"):
         with st.spinner(text="Spreading the table..."):
            time.sleep(1)
            st.dataframe(pca_res,None,None)
            st.write(pca_res.shape) 
        
    # downoading the reduced data file
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(pca_res)
    st.download_button(
            label="Download reduced data",
            data=csv,
            file_name='reduced_df.csv',
            mime='text/csv',
        )
        
    pca_res.columns=["CustomerID","x","y","Cluster"]        
    
    #visualizing results

    st.markdown("#### visualizing results")

    # finding the centroids and labels
    centroids = kmeans.cluster_centers_

    # plotting the results:
    a=alt.Chart(pca_res).mark_circle(size=25).encode(
    x="x",
    y="y",
    color=alt.Color('Cluster', scale=alt.Scale(scheme='plasma')),
    tooltip=["x","y","Cluster"]
    ).properties ( width = 'container').interactive()

    centroids=pd.DataFrame(centroids)
    centroids.columns=["x","y"]
    b=alt.Chart(centroids).mark_circle(size=80,color="white",opacity=1).encode(x="x",y="y",tooltip=["x","y"]).interactive()

    c=alt.layer(b,a)
    st.altair_chart(c, use_container_width=True)


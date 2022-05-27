# importing the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import time
import copy
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import streamlit.components.v1 as components
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

def app():

    # adding the title of the app
    st.title('Make Predictions')
    st.markdown("""<hr>""",True)
    
    #creating columns
    col1, col2= st.columns(2)

    with col1:
        st.markdown(""" 
                <style>
                .data_head{
                    color:#50B4FF;
                    font-size:2rem;
                    transition:0.3s linear;
                    cursor:pointer;
                }
                .data_head:hover{
                    color:#D8BE75;
                }
                </style>
                <h2 class="data_head">The data</h2>
                
                """,True )

        # the sample dataset
        sample=pd.read_csv("./datasets/cars.csv")
        sample.drop("Unnamed: 0",axis=1,inplace=True)
        
        #selecting a dataset (sample/uploaded)
        choice=st.radio("select the dataset you want to use",['sample dataset','upload a dataset'],key=14)
        
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
        
        st.markdown("""
                <hr>
                <h2 class="warning">Correlation Heatmap</h2>
                
                """,True)
        correlations = df.corr()
        fig, ax = plt.subplots()
        sns.heatmap(correlations, cmap="Blues")
        sns.set(rc={'axes.facecolor':'#1A4C85', 'figure.facecolor':'#1A4C85'})
        st.write(fig)

        st.markdown("""
                <h2 class="warning">Find correlation between the selected columns</h2>
                
                """,True)

        cols=st.multiselect("Select upto two columns for visualization",df.columns,key=8890,default=["Ex-Showroom_Price","Displacement"])
        if len(cols)!=2:
            st.error("⚠️ Select upto two columns")
        else:
            st.write('Correlation:',round(df[cols[0]].corr(df[cols[1]]),2))

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
            <a href="https://bhavneet1492.github.io/Sales-and-Price-Prediction/" target=“_blank”>look behind the scenes 👀</a>
            """,True)
        
    
    with col2:
        st.markdown(""" 
                <h2 class="data_head">Car price prediction</h2>
                
                """,True )
        price=st.selectbox("Select the price column",df.columns,key=126)

        st.markdown("""###### distribution of the values of the price column""")

        sns.set(rc={'axes.facecolor':'#1A4C85', 'figure.facecolor':'#1A4C85'})
        fig,ax=plt.subplots()
        sns.distplot(df[price])
        st.write(fig)

        st.markdown("""
                
                <style>
                .warning{
                    color:#7CE39F;
                    font-size:1rem;
                    font-family:monospace;
                    font-weight:200;
                    transition:0.3s linear;
                    cursor:default;
                }
                .warning:hover{
                    opacity:0.5;
                }
                </style>
                <h2 class="warning">Select feautres for making price prediction</h2>
                
                """,True)

        choice=st.radio("",['auto select','select manually'],key=1414)

        thr=0.37

        if choice=='auto select':
            thr=st.slider('Set corrrelation threshold (default=0.37)', 0.0, 1.0,0.37)
            df_new=copy.deepcopy(df)
            for col in df_new.columns:
                if abs(df_new[price].corr(df_new[col]))<thr:
                    df_new. drop (col, axis= 1 ,inplace= True )
            df_new['Ex-Showroom_Price']=df_new[price]

        elif choice=='select manually':
            df_new=pd.DataFrame()
            features=st.multiselect("",df.columns,key=88900)
            if features:            
                for i in features:
                    df_new[i]=df[i]
            df_new['Ex-Showroom_Price']=df_new[price]
        
        st.markdown("""
                
                <style>
                .pred{
                    color:white;
                    font-size:1.7rem;
                    font-family:monospace;
                    font-weight:200;
                }
                </style>
                <hr>
                <h2 class="pred">MAKE PREDICTIONS ></h2>
                
                """,True)
                
        input_set=[]
        for i in df_new.columns:
            if i!='Ex-Showroom_Price':
                input_set.append(st.number_input(i,value=100))

        # decision tree model for price prediction (tested in jupyter notebook--->see 'behind the scenes')
        model = DecisionTreeRegressor()
        model.fit(np.array(df_new.drop('Ex-Showroom_Price',axis=1)),np.array(df_new['Ex-Showroom_Price']).reshape(-1,1))
        prediction = model.predict(np.array(input_set).reshape(1,-1))[0]

        if st.button("View Price"):st.write("Predicted price: ",int(prediction))

    st.markdown(""" 
                <h2 class="data_head">Best time to launch a new car</h2>
                
                """,True )
    col3, col4= st.columns(2)
    with col3:        

        st.markdown("""
                
                <style>
                .sales{
                    color:#99D9C8;
                    font-size:1.5rem;
                    border:2px solid #7CE39F;
                    dislpay:flex;
                    align-items:center;
                    justify-content:center;
                    text-align:center;
                    padding:0.5rem;
                    transition:0.3s linear;
                }
                .sales:hover{
                    background:#99D9C8;
                    opacity:0.5;
                    color:#1A4C85;
                }
                </style>
                <h2 class="sales">Based on Sales</h2>
                <h2 class="warning">Sales trends from 2001 to 2020</h2>
                
                """,True)

        
        sales=[df.iloc[:,i].sum()for i in range(52,32,-1)]
        def pred(sales,key): 
                year=[i for i in range(2001,2021)]
                trend = pd.DataFrame({'sales': sales, 'year': year}, columns=['sales', 'year'])
                chart=alt.Chart(trend).mark_line(color="orange").encode(x='year',y='sales',tooltip=['year','sales'])
                st.altair_chart(chart,use_container_width=True)


                
                stepwise_fit = auto_arima(trend['sales'], start_p = 1, start_q = 1,
                                        max_p = 3, max_q = 3, m = 12,
                                        start_P = 0, seasonal = True,
                                        d = None, D = 1, trace = True,
                                        error_action ='ignore',
                                        suppress_warnings = True,
                                        stepwise = True)  
                st.markdown("""
                        <h2 class="warning">Parameter Analysis</h2>                """,True)
                st.write("Best model for the data:")
                st.write(stepwise_fit)
                st.markdown("""<br>""",True)
                best_model=st.selectbox("Select the above model from the list:",['ARIMA','SARIMA','SARIMAX'],key=key)

                st.write("Select the numbers (a,b,c)(d,e,f)[g] as shown in the image above")

                a=st.number_input("a",value=0,key=key)
                b=st.number_input("b",value=0,key=key)
                c=st.number_input("c",value=1,key=key)
                d=st.number_input("d",value=0,key=key)
                e=st.number_input("e",value=1,key=key)
                f=st.number_input("f",value=0,key=key)
                g=st.number_input("g",value=12,key=key)

                if best_model=='ARIMA':model = model = ARIMA(trend['sales'],order=(a,b,c), seasonal_order=(d,e,f,g))
                    
                else:model = model = ARIMA(trend['sales'],order=(a,b,c), seasonal_order=(d,e,f,g))

                result = model.fit()

                n=st.slider("select the number of years to forecast ahead", min_value=1, max_value=20, value=10,key=key)

                
                # Forecast for the next n years
                forecast = result.predict(start = len(trend),end = (len(trend)-1) + n,typ = 'levels').rename('Forecast')

                year=[i for i in range(2020,2020+n)]

                final=pd.DataFrame({'year': year, 'sales': forecast}, columns=['year', 'sales'])
                
                # Plot the forecast values
                a = alt.Chart(trend).mark_line(color="#7CE39F").encode(x='year', y='sales',tooltip=['year','sales'])

                b = alt.Chart(final).mark_line(color="orange").encode(x='year',y='sales',tooltip=['year','sales'])

                c = alt.layer(a, b)

                st.altair_chart(c, use_container_width=True)

                #best time to launch a new car
                y=2020+list(forecast).index(forecast.max())

                st.markdown(f"""
                        <h1 class="best">{y}</h1>                
                        """,True)
                return y

        y=pred(sales,13245)
        st.markdown(f"""<font color="#64ADFF" size="10px"><b>Best time to launch a new car according to sales data is in <font color="#7CE39F">{y}</font>""",True)
                

            
    with col4:   

        st.markdown("""
                <h2 class="sales">Based on Profit</h2> 
                <h2 class="warning">Profit trends from 2001 to 2020</h2>               
                """,True)
        
        def prof(year):
            profit=0
            for i in range(len(df[str(year)])):
                profit+=df[str(year)][i]*df['Ex-Showroom_Price'][i]
            return profit   

        profit=[]
        for i in range(2001,2021):
            profit.append(prof(i)) 
        
        y=pred(profit,10987)

        st.markdown(f"""<font color="#64ADFF" size="10px"><b>Best time to launch a new car according to profit data is in <font color="#7CE39F">{y}</font>""",True)
    
    
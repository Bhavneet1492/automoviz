import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
from bokeh.plotting import figure
import plotly.figure_factory as ff

#defining functions

# function to find the best selling feature during a selected period
def bsf_r(df,feature,end,start):
    sales=[]
    start=df.columns.get_loc(str(start))
    end=df.columns.get_loc(str(end))
    for i in range(len(feature)):
        sale=0
        for j in range(start,end+1):
            sale+=df.iloc[:,j][i]
        sales.append([feature[i],sale])
    a=sales
    b=[]
    for i in a:
        if [i[0],0] not in b:b.append([i[0],0])
    for i in a:
        for j in b:
            if i[0]==j[0]:j[1]+=i[1]
    sales=b
    sales=sorted(sales,key=lambda x:x[1],reverse=True)
    max_sold=sales[0][1]
    for i in range(len(sales)):
        if sales[i][1]!=max_sold:
            break
    feat_list=[[sales[j][0],sales[j][1]] for j in range(i)]
    return feat_list

# function to find the most profitable feature during the selected period
def profit_rank_r(df,feature,end,start):
    sales=[]
    start=df.columns.get_loc(str(start))
    end=df.columns.get_loc(str(end))
    for i in range(len(feature)):
        sale=0
        for j in range(start,end+1):
            sale+=df.iloc[:,j][i]
        sales.append([feature[i],sale*df['Ex-Showroom_Price'][i]])
    a=sales
    b=[]
    for i in a:
        if [i[0],0] not in b:b.append([i[0],0])
    for i in a:
        for j in b:
            if i[0]==j[0]:j[1]+=i[1]
    sales=b
    sales=sorted(sales,key=lambda x:x[1],reverse=True)
    rank=1
    max=sales[0][1]
    for i in sales:
        if i[1]>=max:i.append(rank)
        else:
            rank+=1
            max=i[1]
            i.append(rank)
    for i in range(len(sales)):
        if sales[i][2]!=1:
            break
    feat_list=[[sales[j][0],sales[j][1]] for j in range(i)]
    return feat_list

# function to calculate the total profit for a given year
def prof(df,year):
    profit=0
    for i in range(len(df[str(year)])):
        profit+=df[str(year)][i]*df['Ex-Showroom_Price'][i]
    return profit

# function to calculate the total profit during the selected period
def prof_y(df,start,end):
    profit=0
    for i in range(start,end+1):
        profit+=prof(df,str(i))
    return profit

# function to calculate the total sales for a given year
def saless(df,year):
    sales=0
    for i in range(len(df[str(year)])):
        sales+=df[str(year)][i]
    return sales

# function to calculate the total sales during the selected period
def saless_y(df,start,end):
    sales=0
    for i in range(start,end+1):
        sales+=saless(df,str(i))
    return sales

# function to plot the sales of a feature OVERALL
def bsf_bar(df,feature,end,start):
    sales=[]
    start=df.columns.get_loc(str(start))
    end=df.columns.get_loc(str(end))
    for i in range(len(feature)):
        sale=0
        for j in range(start,end+1):
            sale+=df.iloc[:,j][i]
        sales.append([feature[i],sale])
    a=sales
    b=[]
    for i in a:
        if [i[0],0] not in b:b.append([i[0],0])
    for i in a:
        for j in b:
            if i[0]==j[0]:j[1]+=i[1]
    sales=b
    sales=sorted(sales,key=lambda x:x[1],reverse=True)
    max_sold=sales[0][1]
    for i in range(len(sales)):
        if sales[i][1]!=max_sold:
            break
    return sales

# function to plot the profit from a feature OVERALL
def profit_bar(df,feature,end,start):
    sales=[]
    start=df.columns.get_loc(str(start))
    end=df.columns.get_loc(str(end))
    for i in range(len(feature)):
        sale=0
        for j in range(start,end+1):
            sale+=df.iloc[:,j][i]*df['Ex-Showroom_Price'][i]
        sales.append([feature[i],sale])
    a=sales
    b=[]
    for i in a:
        if [i[0],0] not in b:b.append([i[0],0])
    for i in a:
        for j in b:
            if i[0]==j[0]:j[1]+=i[1]
    sales=b
    sales=sorted(sales,key=lambda x:x[1],reverse=True)
    max_sold=sales[0][1]
    for i in range(len(sales)):
        if sales[i][1]!=max_sold:
            break
    return sales

# function to plot sales by feature instance in a selected period
def plot_sales(df,feature,type_name,start,end):
    sales=[]
    for j in range(start,end+1):
        sale=0
        for i in range(len(feature)):
            if feature[i]==type_name:
                sale+=df[str(j)][i]            
        sales.append(sale)
    return sales

# function to plot profits by feature instance in a selected period
def plot_profits(df,feature,type_name,start,end):
    profits=[]
    for j in range(start,end+1):
        profit=0
        for i in range(len(feature)):
            if feature[i]==type_name:
                profit+=df[str(j)][i]*df["Ex-Showroom_Price"][i]
        profits.append(profit)
    return profits

# function to calculate the sales of all the feature instances in the given year
def all_sales(df,feature,year):
    sales=[]
    for i in range(len(feature)):
        sale=df[str(year)][i]
        sales.append([feature[i],sale])
    a=sales
    b=[]
    for i in a:
        if [i[0],0] not in b:b.append([i[0],0])
    for i in a:
        for j in b:
            if i[0]==j[0]:j[1]+=i[1]
    sales=b
    return sales

# function to calculate the sales of all the feature instances in the given year
def all_profits(df,feature,year):
    profits=[]
    for i in range(len(feature)):
        profit=df[str(year)][i]*df["Ex-Showroom_Price"][i]
        profits.append([feature[i],profit])
    a=profits
    b=[]
    for i in a:
        if [i[0],0] not in b:b.append([i[0],0])
    for i in a:
        for j in b:
            if i[0]==j[0]:j[1]+=i[1]
    profits=b
    return profits

def app():
    
    # defining css classes
    st.markdown("""<style>
    .feature_name{
    color:#7CE39F;
    font-size:2rem;
    font-family:monospace;
    font-weight:200;
        }
    .feature{
    color:#D8BE75;
    font-size:2rem;
        }
    .sales{
    color:white;
    opacity:0.8;
    font-size:1.5rem;
        }
    </style>
    """,True)

    # adding the title of the app
    st.title('Business Insights')
    st.markdown("""<hr>""",True)

    
    # the sample dataset
    sample=pd.read_csv("./datasets/cars_cat.csv")
        
    #selecting a dataset (sample/uploaded)
    choice=st.radio("Select the dataset you want to use",['sample dataset','upload a dataset'],key=14)
        
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


    feature=st.selectbox("select a feature",df.columns,key=241,index=2)
    
    st.markdown("""<hr>""",True)
    st.header("Insights") 

    col1,col2=st.columns(2)
    with col1:
        st.markdown(f"""
            <h2 class="feature">Best selling {feature}</h2>                
            """,True) 
        years = st.slider(
        'Select a range',
        2001, 2020, (2015, 2018))
        for i in bsf_r(df,df[feature],years[0],years[1]):
            st.markdown("""
            <h2 class="feature_name">{}</h2>
            <h2 class="sales">{} sold</h2>               
            """.format(i[0],int(i[1])),True) 
        st.markdown("""<hr>""",True)

    with col2:
        st.markdown(f"""
            <h2 class="feature">Most profitable {feature}</h2>                
            """,True) 
        years = st.slider(
        'Select a range',
        2001, 2020, (2010, 2015),key=89)
        for i in profit_rank_r(df,df[feature],years[0],years[1]):
            st.markdown("""
            <h2 class="feature_name">{}</h2> 
            <h2 class="sales">Profit: ₹ {} B</h2>               
            """.format(i[0],round(i[1]/100000000,2)),True)
        st.markdown("""<hr>""",True)
    
    col3,col4=st.columns(2)
    with col3:
        st.markdown(f"""
            <h2 class="feature">Total sales of the company</h2>                
            """,True) 
        years = st.slider(
        'Select a range',
        2001, 2020, (2015, 2018),key=678)
        st.markdown("""<h2 class="feature_name">{} cars</h2>               
        """.format(int(saless_y(df,years[0],years[1]))),True) 
    with col4:
        st.markdown(f"""
            <h2 class="feature">Total profit of the company</h2>                
            """,True) 
        years = st.slider(
        'Select a range',
        2001, 2020, (2010, 2015),key=8289)
        st.markdown("""<h2 class="feature_name">₹ {} B</h2>               
        """.format(round(prof_y(df,years[0],years[1])/100000000,2)),True)
    
    st.markdown("""<hr>""",True)
    st.header("Visualizations")

    cola,colb=st.columns(2)

    with cola:
        st.subheader(f"{feature}s by sales")
        years = st.slider(
            'Select a range',
            2001, 2020, (2015, 2018),key=5678) 
        sales=bsf_bar(df,df[feature],years[0],years[1])
        source=pd.DataFrame(sales, columns =['Features', 'Sales'])
        source.columns=["Feature","Sales"]
        fig = px.bar(source, x='Feature', y='Sales')
        st.plotly_chart(fig, use_container_width=True)
    
    with colb:
        st.subheader(f"{feature}s by profit")
        years = st.slider(
            'Select a range',
            2001, 2020, (2015, 2018),key=4324)
        Profit=profit_bar(df,df[feature],years[0],years[1])
        source=pd.DataFrame(Profit, columns =['Features', 'Profit'])
        source.columns=["Feature","Profit"]
        fig = px.bar(source, x='Feature', y='Profit')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<hr>""",True)
    st.header("Trends")
    colx,coly=st.columns(2)
    with colx:
        st.subheader("By sales")
        type_name=st.selectbox(f"select a {feature} type",df[feature].unique(),key=2441)
        years = st.slider(
            'Select a range',
            2001, 2020, (2006, 2018),key=4343224)
        sales_=plot_sales(df,df[feature],type_name,years[0],years[1])
        Years=[i for i in range(years[0],years[1]+1)]
        dfm=pd.DataFrame(list(zip(sales_, Years)),columns = ['sales','Years'])
        line = alt.Chart(dfm).mark_line(color="#7CE39F").encode(x="Years",y='sales',tooltip=['sales','Years']).interactive()
        st.altair_chart(line,use_container_width=True)

    with coly:
        st.subheader("By profit")
        type_name=st.selectbox(f"select a {feature} type",df[feature].unique(),key=2241,index=1)
        years = st.slider(
            'Select a range',
            2001, 2020, (2015, 2018),key=43403224)
        profits_=plot_profits(df,df[feature],type_name,years[0],years[1])
        Years=[i for i in range(years[0],years[1]+1)]
        dfm=pd.DataFrame(list(zip(profits_, Years)),columns = ['profit','Years'])
        line = alt.Chart(dfm).mark_line(color="#FF855E").encode(x="Years",y='profit',tooltip=['profit','Years']).interactive()
        st.altair_chart(line,use_container_width=True)

    colp,colq=st.columns(2)
    with colp:
        st.subheader("All sales")
        years = st.slider(
            'Select a range',
            2001, 2020, (2015, 2018),key=99990)
        sales_list=[all_sales(df,df[feature],i) for i in range(years[0],years[1]+1)]
        year=years[0]
        for i in sales_list:    
            for j in i:
                j.append(year)
            year+=1
        data=[]
        for i in sales_list:
            for j in i:
                data.append(j)
        source=pd.DataFrame(data, columns =[feature, 'Sales','Year']) 
        chart=alt.Chart(source).mark_line().encode(
            x='Year',
            y='Sales',
            color=feature,strokeDash=feature,tooltip=[feature, 'Sales','Year']
        ).interactive()
        st.altair_chart(chart,use_container_width=True)

        st.subheader("Cumulative sales")
        source.groupby(['Year',feature]).sum().unstack().plot(kind='line',y='Sales', stacked = True).get_figure().savefig('./images/phase4/output.png')
        image = Image.open('./images/phase4/output.png')
        st.image(image,use_column_width =True)
    
    with colq:
        st.subheader("All profits")
        years = st.slider(
            'Select a range',
            2001, 2020, (2015, 2018),key=99090)
        profits_list=[all_profits(df,df[feature],i) for i in range(years[0],years[1]+1)]
        year=years[0]
        for i in profits_list:    
            for j in i:
                j.append(year)
            year+=1
        data=[]
        for i in profits_list:
            for j in i:
                data.append(j)
        source=pd.DataFrame(data, columns =[feature, 'Profit','Year']) 
        chart=alt.Chart(source).mark_line().encode(
            x='Year',
            y='Profit',
            color=feature,strokeDash=feature,tooltip=[feature, 'Profit','Year']
        ).interactive()
        st.altair_chart(chart,use_container_width =True)

        st.subheader("Cumulative profits")
        source.groupby(['Year',feature]).sum().unstack().plot(kind='line',y='Profit', stacked = True).get_figure().savefig('./images/phase4/output.png')
        image = Image.open('./images/phase4/output.png')
        st.image(image,use_column_width =True)


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
            <a href="https://bhavneet1492.github.io/Sales-and-Price-Prediction/" target=“_blank”>look behind the scenes 👀</a>
            """,True)
    
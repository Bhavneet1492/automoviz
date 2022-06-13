import streamlit as st
import pandas as pd
import numpy as np

# defining functions

# function to calculate ranks of features in the selected period
def rank_r(df,feature,end,start):
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
    rank=1
    max=sales[0][1]
    for i in sales:
        if i[1]>=max:i[1]=rank
        else:
            rank+=1
            max=i[1]
            i[1]=rank
    return pd.DataFrame(sales, columns =['Feature', 'Rank'])

#setting the page configuration
st.set_page_config(
    page_title="Customer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# hiding menu and footer
hide_menu_style="""
                <style>
                   #MainMenu {visibility:hidden;} 
                   footer {visibility:hidden;} 
                </style>
                """
st.markdown(hide_menu_style,True)

# adding the introduction
st.markdown("""
    <style>
        .logo{
            font-family:monospace;
            font-weight:400;
            font-size:3.8rem;

        }
        .introduction{
            font-size:1.5rem;
            font-weight:200;
        }

        .heading{
            font-size:3rem;
        }
        .name{
            font-size:1.5rem;
            color:#ff725e;
        }
        .rank{
            font-size:2rem;
            font-weight:400;
            font-family:monospace;
        }
        .rlist{
            display:flex;
            align-items:center;
            justify-content:space-between;
            flex-direction:row;
            flex-wrap:no-wrap;
        }

    </style>

    <h1 class="logo">AUTOMOVIZ</h1>
    <h3 class="introduction">Looking for a new car? You've landed on the right place! Automoviz compares hundreds of features of leading brand models with the most accurate statistics for you so that you can find the best fit for your needs</h3>
    <hr>
    """,True)
    
# the dataset
df=pd.read_csv("../datasets/cars_cat.csv")
df.drop("Unnamed: 0",axis=1,inplace=True)

col1,col2,col3=st.columns(3)
with col1:
    st.markdown("""<h2 class="heading">Best Sellers</h2>""",True)

    feature=st.selectbox("Select a feature",df.columns,index=1)

    years=st.slider("Set the time period",2001,2020,(2015,2018))

    bestSellers=rank_r(df,df[feature],years[0],years[1])

    for i in range(5):
        st.markdown(f"""
            <div class="rlist">
                <h2 class="rank">{bestSellers.Rank[i]}</h2>
                <h2 class="name">{bestSellers.Feature[i]}</h2>
            </div>        
        """,True)

with col2:
    st.markdown("""<h2 class="heading">Cars by price</h2>""",True)

    price=st.slider("Set the price range (in lac)",1,100,(10,20),step=1)

    mask=((df["Ex-Showroom_Price"] >= (price[0]*100000)) & (df["Ex-Showroom_Price"] <= (price[1]*100000)))

    data=pd.DataFrame()
    data["Model"]=df[mask]["Model"].unique()
    st.dataframe(data,height=500)

with col3:
    st.markdown("""<h2 class="heading">Cars by mileage</h2>""",True)

    mileage=st.slider("Set the mileage range (in kmph)",10,2000,(750,1260),step=50)

    mask=((df["Mileage"] >= mileage[0]) & (df["Mileage"] <= mileage[1]))

    data=pd.DataFrame()
    data["Model"]=df[mask]["Model"].unique()
    st.dataframe(data,height=500)

st.markdown("""<hr>""",True)
st.markdown("""<h2 class="heading">Features</h2>""",True)

columns=st.columns(6)
with columns[0]:
    model=st.selectbox("Select a model",df.Model,index=2)
with columns[0]:
    mask = (df["Model"] == model)
    variants=df[mask]["Variant"]
    variant=st.selectbox("Available variants",variants)
    mask=((df["Model"] == model) & (df["Variant"] == variant))
    cols=df.columns
    cols=[cols[0]]+list(cols[3:26])
j=0
for i in cols:
    with columns[j%6]:
        st.write(df[mask][i])
        j+=1

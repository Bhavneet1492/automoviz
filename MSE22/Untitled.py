import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import altair as alt
# st.title("h)ello world")
# st.header("This is the Header")
# st.subheader("this is the subheader")
# st.text("this is some random text")
# st.markdown(""" #h1 tag
# ## h2 tag
# ### h3 tag <br>
# **asterisks** or __ underscores __
# ##### h5 tag
# :heart:
# """,True)
# st.write("hey ter","hell")
# a=[1,2,3,4,5,6,7,8]
# n=np.array(a)
# nd=n.reshape((2,4))
# dic={
#     "name":["sapphire"],
#     "age":[19],
#     "city":["mumbai"]
# }
# data=pd.read_csv("annual_sales.csv")
# st.table(dic)
# st.json(dic)
# st.write(dic)

# @st.cache
# def ret_time(a):
#     time.sleep(5)
#     return time.time()

# if st.checkbox("1"):
#     st.write(ret_time(1))
    
# if st.checkbox("2"):
#     st.write(ret_time(2))  

# data=pd.DataFrame(
# np.random.randn(100,3),
#     columns=['a','b','c']
# )

# st.line_chart(data)
# st.area_chart(data)
# st.bar_chart(data)

# fig,axis=plt.subplots()
# axis.scatter(data['a'],data['b'])
# plt.title("scatter plot")
# st.pyplot(fig)

# chart=alt.Chart(data).mark_circle().encode(
# x='a',y='b',tooltip=['a','b']
# )
# st.altair_chart(chart,use_container_width=True)

# st.graphviz_chart("""
# digraph{
# watch->like
# like->share
# share->sub
# share->watch
# }
# """)

# st.map()

# st.image("./car.svg")

st.title("Widgets")
# if st.button("Encode"):
#     st.write("select the type of encoder:")
#     st.button("Label")
#     st.button("One Hot")
    
# date2=st.date_input("date2")
# date1=st.date_input("date1")
# st.write(date2-date1)
    
# st.slider("multiplier",min_value=0.1)

specs=st.file_uploader("upload specifications dataset")
data=pd.read_csv(specs)
# st.table(dic)
# st.json(dic)
st.write(data)
df=pd.DataFrame(data=data)

st.sidebar.selectbox("select column",df.columns,key=1)
col=st.multiselect("select column",df.columns,key=3)


fig,axis=plt.subplots()
axis.scatter(df["Doors"],df[col])
plt.title("scatter plot")
st.pyplot(fig)
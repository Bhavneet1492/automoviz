<div align="center">
  
  # AUTOMOVIZ 
  
![Status active](https://img.shields.io/badge/Status-active%20development-2eb3c1.svg) ![Streamlit 1.9.0](https://img.shields.io/badge/Streamlit-1.9.0-green.svg) ![Python 3.8.1](https://img.shields.io/badge/Python-3.8.1-blue.svg) 
  
  <p align="center">
  <img 
    height="300"
    src="./images/readme/banner.png"
  >
  <h4 align="center">A data analysis platform for the automotive industry</h4>
</p>

`automoviz` <i>is the go-to place for a smooth analysis experience, be it the customers or the industry experts. With features such as data-cleaning, visualizations, segmentations and more powered by an AI-driven technology, automoviz lets you accurately decide your next move for launching a new car or buying one!</i>

Go to <a href="https://bhavneet1492.github.io/automoviz/" target="_blank">AUTOMOVIZ</a>

[About the App](#-about-the-app) •
[Local Setup](#-local-setup) •
[Tech Used](#-tech-used) •
[Future Scope](#-future-scope) •
[Contact](#-contact)

  
</div>

# 📉 About the App

## Themes:
- serene (default)
- classic

## Sections:
- Explore
  - Demo video on what the app is about and how it works
- Industry Expert
  - Data Cleaning
  - Data Visualization
  - Make Predictions
    - car price predictions
    - business sales and profit prediction
    - best time to launch a new car  
  - Busines Insights
  - Customer Segmentation
  
  ##### available themes: `custom` | `light` | `dark`

- Customer
  - Best Selling Features
  - Cars in selected price range
  - Cars in selected mileage range
  - Features of selected car model and variant
  
  ##### available themes: `custom` | `light` | `dark`

# 🖥️ Local Setup

## Requirements:
- Python 3.8.1 runtime
- Streamlit 1.9.0
- Other dependencies in `requirements.txt`

## Procedure:
- To run the complete app, double click on the index.html file on your local device
- To run the apps individually:
  - Install [python](https://www.python.org/downloads/) in your environment(pre-installed on Ubuntu).
  - Clone this repository on your local device.
  - Navigate to the cloned repository.
    ```
    cd <project_directory_name> 
    ```
    
  - Install `pipenv` for dependency management
    ```
    pip install pipenv
    ```
    
  - Use pip to install other dependencies from `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
    
  - Run development server on localhost (for **Industry Expert** dashboard)
    ```
    streamlit run app.py
    ```
    
  - Navigate to the ***customer*** folder (for **Customer** dashboard)
    ```
    cd customer
    ```   
    
  - Run development server on localhost
    ```
    streamlit run customer.py

# **</>** Tech Used 
- Frontend
  - Home Page
    - HTML5
    - CSS3
    - JS
  - Explore Page
    - HTML5
    - CSS3
  - Industry Expert Page
    - HTML5
    - CSS3
    - Streamlit
  - Customer Page
    - HTML5
    - CSS3
    - Streamlit
- Backend
  - Industry Expert Page
    - Python 3.8.1
    - Streamlit 1.9.0
  - Customer Page
    - Python 3.8.1
    - Streamlit 1.9.0
- Deployment
  - Github Pages
  - Streamlit Cloud
  - Heroku

# 🕒 Future Scope

1. The application currently uses csv files for data. It can be connected to a database like MongoDB
2. The application has a rigid structure. It can handle only the data of the format same as the sample data. It should be flexible to handle any kind of data
3. The application is completely based on functional programming approach. It can be converted into an object-oriented programming application

# 😇 Spread the word!

If you want to support active development of the AUTOMOVIZ app:

- Contribute to the project on Github
- Add a GitHub Star to the project!
- Post about the project on your LinkedIn!
  - Tag [me](https://www.linkedin.com/in/bhavneet-kaur-khalsa-8157a21ba/) 

## ♡ Thank you so much for your interest in AUTOMOVIZ!

# 📧 Contact

[bhavneetkaurkhalsa@gmail.com](https://www.linkedin.com/in/bhavneet-kaur-khalsa-8157a21ba/)





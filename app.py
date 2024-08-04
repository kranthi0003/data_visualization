import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page config as the first command
st.set_page_config(layout="wide", page_title="Heart Attack Risk Prediction Dashboard", page_icon=":heart:", initial_sidebar_state="expanded")

# Center-align the page title using HTML and CSS
st.markdown("""
    <style>
        .title {
            text-align: center;
        }
        .download-button {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the download button using HTML
st.markdown("""
    <a href="data:application/octet-stream;base64,{}" download="data.xlsx" class="download-button">
        Download Data
    </a>
""".format(st.download_button("Download data", data=open('data.xlsx', 'rb').read(), file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key='download-button')), unsafe_allow_html=True)

# Display the centered page title
st.markdown("<h1 class='title'>Heart Attack Risk Prediction Dashboard</h1>", unsafe_allow_html=True)
st.write("\n\n")

# Load your data
@st.cache_data()
def load_data():
    data = pd.read_excel('data.xlsx', engine='openpyxl')
    # Assuming the Excel file has columns for 'Cholesterol', 'Triglycerides', 'Heart Attack Risk', 'Country', etc.
    return data

data = load_data()

# Define thresholds and labels for categorization
cholesterol_thresholds = [0, 200, 239, float('inf')]
cholesterol_labels = ['Normal', 'Borderline High', 'High']
triglycerides_thresholds = [0, 150, 199, 499, float('inf')]
triglycerides_labels = ['Normal', 'Borderline', 'High', 'Very High']

# Categorize cholesterol and triglycerides levels
data['Cholesterol Category'] = pd.cut(data['Cholesterol'], bins=cholesterol_thresholds, labels=cholesterol_labels, include_lowest=True)
data['Triglycerides Category'] = pd.cut(data['Triglycerides'], bins=triglycerides_thresholds, labels=triglycerides_labels, include_lowest=True)

# Create columns for key metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.header('Total Candidates')
    st.subheader(f"{len(data)}")
with col2:
    st.header('Patients at Risk of Heart Attack')
    st.subheader(f"{data['Heart Attack Risk'].sum()}")
with col3:
    st.header('Gender-Wise Risk')
    gender_count = data['Sex'].value_counts()
    fig0 = px.pie(values=gender_count, names=gender_count.index)
    st.plotly_chart(fig0, use_container_width=True)

# Cholesterol Level Distribution
st.subheader('Cholesterol Level Amongst Population')
cholesterol_counts = data['Cholesterol Category'].value_counts().loc[cholesterol_labels]
fig1 = px.bar(x=cholesterol_counts.index, y=cholesterol_counts.values, text=cholesterol_counts.values,
              labels={'y':'Count', 'x':'Cholesterol Category'})
fig1.update_traces(marker_color=['#636EFA','#EF553B','#00CC96'], marker_line_color='rgb(8,48,107)',
                   marker_line_width=1.5, opacity=0.6)
st.plotly_chart(fig1, use_container_width=True)

# Risk of Heart Attack in Asian Countries
st.subheader('Risk of Heart Attack in Asian Countries')
asian_countries = ['South Korea', 'Thailand', 'China', 'Vietnam', 'Japan', 'India']
asian_data = data[data['Country'].isin(asian_countries)]
risk_counts = asian_data.groupby('Country')['Heart Attack Risk'].sum().reindex(asian_countries)
fig7 = px.bar(risk_counts, x=risk_counts.index, y=risk_counts.values, text=risk_counts.values,
              labels={'y':'Number of Cases', 'index':'Country'},
              color_discrete_sequence=px.colors.sequential.Blues_r)
st.plotly_chart(fig7, use_container_width=True)

# Heart Attack Risk by Triglycerides Level
st.subheader('Heart Attack Risk by Triglycerides Level')
triglycerides_risk = data.groupby('Triglycerides Category')['Heart Attack Risk'].mean().reindex(triglycerides_labels)
fig2 = px.line(x=triglycerides_risk.index, y=triglycerides_risk.values, markers=True)
fig2.update_traces(line_color='#FECB52')
st.plotly_chart(fig2, use_container_width=True)

# Heart Attack Risk by Cholestrol Level
st.subheader('Risk by Cholesterol Level')
cholesterol_risk_counts = data['Cholesterol Category'].value_counts()

fig_cholesterol_risk = px.pie(
    values=cholesterol_risk_counts,
    names=cholesterol_risk_counts.index
)

fig_cholesterol_risk.update_layout(
    showlegend=True
)
st.plotly_chart(fig_cholesterol_risk, use_container_width=True)

# Continent-wise Risk of Heart Attack
st.subheader('Continent-wise Risk of Heart Attack')
continent_risk_data = data.groupby('Continent')['Heart Attack Risk'].sum().reset_index()

fig_continent_risk = px.line(
    continent_risk_data,
    x='Continent',
    y='Heart Attack Risk',
    markers=True
)

fig_continent_risk.update_traces(line_color='lightblue', marker=dict(color='darkblue', size=10))
fig_continent_risk.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)
st.plotly_chart(fig_continent_risk, use_container_width=True)

# Risk among Smokers
st.subheader('Risk among Smokers')
smokers_risk = data.groupby('Smoking')['Heart Attack Risk'].sum()
fig5 = px.pie(values=smokers_risk, names=['Non-Smoker', 'Smoker'])
st.plotly_chart(fig5, use_container_width=True)

# Age Wise Risk
st.subheader('Age Wise Risk')
age_bins = [20, 30, 40, 50, 60, 70, 80, 90, 100]
age_labels = ['21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91+']
data['Age Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels)
age_group_risk = data.groupby('Age Group')['Heart Attack Risk'].sum()
fig6 = px.bar(x=age_group_risk.index, y=age_group_risk.values, text=age_group_risk.values,
              labels={'y':'Heart Attack Risk', 'x':'Age Group'})
fig6.update_traces(marker_color='indianred', marker_line_color='rgb(8,48,107)',
                   marker_line_width=1.5, opacity=0.6)
st.plotly_chart(fig6, use_container_width=True)

# Hemisphere-wise Risk of Heart Attack
st.subheader('Hemisphere-wise Risk of Heart Attack')
hemisphere_risk_data = data.groupby('Hemisphere')['Heart Attack Risk'].sum().reset_index()

fig_hemisphere_risk = px.bar(
    hemisphere_risk_data,
    x='Hemisphere',
    y='Heart Attack Risk',
    text='Heart Attack Risk',
    color_discrete_sequence=['#636EFA']
)

fig_hemisphere_risk.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)

fig_hemisphere_risk.update_traces(texttemplate='%{text}', textposition='outside')
st.plotly_chart(fig_hemisphere_risk, use_container_width=True)

# Add a fixed copyright bar attached to the bottom of the screen
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: black;
        padding: 10px;
        text-align: center;
    }
    </style>
    <div class="footer">
        Copyright © 2024 by Kranthi Kiran A. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)

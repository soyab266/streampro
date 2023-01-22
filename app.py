import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt



df=pd.read_csv('startup_cleaned.csv')
df['investor'].fillna('Vinod Khatumal', inplace=True)
df['date']=pd.to_datetime(df['date'], errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_overall_analysis():
    st.title('overall analysis')
    total=round(df['amount'].sum())

    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    num_startups=df['startup'].nunique()
    col1, col2, col3, col4 =st.columns(4)
    with col1:

        total = st.metric('Total', str(total) + 'cr')
    with col2:

        total = st.metric('Max', str(max_funding) + 'cr')

    with col3:

        st.metric('Avg',str(avg_funding)+'cr')

    with col4:
        st.metric('funded startups',num_startups)
        st.header('mom graph')
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '_' + temp_df['year'].astype('str')
        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x_axis'], temp_df['amount'])
        st.pyplot(fig3)


def load_investor_details(investor):
    st.title(investor)
    last5_df=df[df['investor'].str.contains('investors')].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('most recent investment')
    st.dataframe(last5_df)

    col1, col2=st.columns(2)
    with col1:

        big_series=df[df['investor'].str.contains('investors')].groupby('startup')['amount'].sum().sort_values(ascending=False).head(4)
        st.subheader('biggest investment')
        fig,ax=plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        verical_series=df[df['investor'].str.contains('investors')].groupby('vertical')['amount'].sum()
        st.subheader('sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series, labels=verical_series.index,autopct='%0.01f')
        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series=df[df['investor'].str.contains('investors')].groupby('year')['amount'].sum()
    st.subheader('yoy investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)
    st.pyplot(fig2)


st.sidebar.title('Startup funding analysis')
option=st.sidebar.selectbox('select one',['overall analysis','startup','investor'])

if option=='overall analysis':
    btn0=st.sidebar.button('show overall analysis')
    if btn0:
        load_overall_analysis()

elif option=='startup':
    st.sidebar.selectbox('select startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('find startup details')
    st.title('startup analysis')

else:
    selected_investors=st.sidebar.selectbox('select startup',df['investor'].str.split(','))
    btn2 = st.sidebar.button('find investor details')

    if btn2:
        load_investor_details(selected_investors)



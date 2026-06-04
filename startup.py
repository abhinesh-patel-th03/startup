import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time
st.set_page_config(layout="wide",page_title="Startup Analysis")
startup_india=pd.read_csv("cleaned.csv")
investor=sorted(set(startup_india["Investors"].str.split(",").sum()))
st.sidebar.title("Startup Funding Analysis")

# Inject custom CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] h1 {
        color: #1E88E5;
        font-size: 28px;
        font-family: monospace;
    }
    
   
    [data-testid="stSidebar"] p {
        color: #4CAF50;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
def select_investor(investor):
     st.header(investor)
     investment=startup_india[startup_india["Investors"].str.contains(investor)][["Startup","City","Date","InvestmentAmount"]].head()
     big_investment=startup_india[startup_india["Investors"].str.contains(investor)].groupby("Startup")["InvestmentAmount"].sum().sort_values(ascending=False).head()
     st.subheader("All Recent Investment")
     st.dataframe(investment)
     st.subheader("Biggest Investment")
     st.dataframe(big_investment)
     col1,col2=st.columns(2)
     with col1:
         st.subheader("Invested Amount")
         fig,ax=plt.subplots(figsize=(5,4))
         ax.bar(big_investment.index,big_investment.values)
         st.pyplot(fig)
     with col2:
         pie_graph=startup_india[startup_india["Investors"].str.contains(investor)].groupby("Industry")["InvestmentAmount"].sum()
         st.subheader("Sector of Investment")
         fig1,ax1=plt.subplots(figsize=(5,4))
         wedges, texts = ax1.pie(pie_graph, labels=None)
         ax1.legend(wedges, pie_graph.index, title="Sectors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
         ax1.pie(pie_graph,labels=pie_graph.index)
         st.pyplot(fig1,use_container_width=True)
     col3,col4 =st.columns(2)
     with col3:
         city=startup_india[startup_india["Investors"].str.contains(investor)]. groupby("City")["InvestmentAmount"].sum()
         st.subheader("City with investments")
         fig2,ax2=plt.subplots(figsize=(5,4))
         wedges, texts = ax2.pie(city, labels=None)
         ax2.legend(wedges, city.index, title="Cities", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
         ax2.pie(city,labels=city.index)
         st.pyplot(fig2,use_container_width=True)
     with col4:
         startup_india["Date"] = pd.to_datetime(startup_india["Date"], errors="coerce")
         startup_india["Date"]=startup_india["Date"].dt.year
         year_investment=startup_india[startup_india["Investors"].str.contains(investor)]. groupby("Date")["InvestmentAmount"].sum()
         st.subheader("Year wise Investment")
         fig3,ax3=plt.subplots(figsize=(5,4))
         ax3.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
         ax3.plot(year_investment)
         st.pyplot(fig3,use_container_width=True)
# overall analysis
     
def overall(data):
    st.title("Overall Analysis")
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.subheader("Total Investment Between 2020-2025")
        st.metric("india",str(data["InvestmentAmount"].sum())+ "cr")
    with col2:
        st.subheader("Highest Investment between 2020-2025")
        st.metric("india",str(data["InvestmentAmount"].max())+ "cr")
    with col3:
        st.subheader("Overall Average in 5yrs")
        st.metric("india",str(data["InvestmentAmount"].mean())+ "cr")
    with col4:
        st.subheader("Total Funded Startup")
        st.metric("india",str(len(set(data["Startup"]))))
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Year"]=data["Date"].dt.year
    overall_year_investment=data.groupby("Year")["InvestmentAmount"].sum()
    st.subheader("Overall Year wise Investment")
    fig1,ax1=plt.subplots(figsize=(5,2))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax1.plot(overall_year_investment)
    st.pyplot(fig1,use_container_width=True)
    sectors=data.groupby("Industry")["InvestmentAmount"].sum()
    st.subheader("Sector Wise Investment")
    fig2,ax2=plt.subplots(figsize=(5,4))
    wedges, texts = ax2.pie(sectors, labels=sectors.index)
    ax2.legend(wedges, sectors.index, title="Sectors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax2.pie(sectors,labels=sectors.index)
    st.pyplot(fig2,use_container_width=True)
    st.subheader("City Wise Funding")
    city_wise_funding=data.groupby("City")["InvestmentAmount"].sum().sort_values(ascending=False)
    st.dataframe(city_wise_funding)
    st.header("Top Startup With Highest funding")
    top_startup = data.groupby("Startup")["InvestmentAmount"].sum().sort_values(ascending=False).head(5)
    st.dataframe(top_startup)
    st.header("Top Investors With Highest Investment")
    top_startup = data.groupby("Investors")["InvestmentAmount"].sum().sort_values(ascending=False).head(5)
    st.dataframe(top_startup)

    #################
    st.subheader("Funding Heatmap (Sector vs Year)")
    # 2. Pivot the data to create a matrix (Rows: Industry, Columns: Year, Values: Total Investment)
    # Filling missing values with 0 so the heatmap displays continuously
    heatmap_matrix = data.pivot_table(
        index='Industry' if 'Industry' in data.columns else "", 
        columns='Year', 
        values='InvestmentAmount', 
        aggfunc='sum'
    ).fillna(0)
    
    # 3. Take the top 15 sectors so the heatmap stays readable and uncluttered
    top_sectors = heatmap_matrix.sum(axis=1).nlargest(15).index
    heatmap_matrix = heatmap_matrix.loc[top_sectors]
    
    # 4. Generate the plot
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        heatmap_matrix, 
        annot=True,          # Shows total values inside squares
        fmt=".0f",           # Keeps values clean without long decimals
        cmap="YlGnBu",       # Smooth yellow-to-blue gradient scale
        linewidths=0.5,      # Crisp white border between squares
        ax=ax4
    )
    
    # 5. Render directly to your dashboard layout
    st.pyplot(fig4)


    # startup ##################
cleaned=pd.read_csv("indian_cleaned.csv")
startup_name=sorted(set(cleaned["Startup"]))
def startup(startup_name):
    st.header(startup_name)
    startup_city=startup_india[startup_india["Startup"]==startup_name]["City"]
    startup_investor=startup_india[startup_india["Startup"]==startup_name]["Investors"]
    startup_investment=startup_india[startup_india["Startup"]==startup_name][["Investors","InvestmentAmount"]]
    col1,col2,col3 =st.columns(3)
    with col1:
        st.subheader("Biggest Investment Got")
        st.write(str(startup_india[startup_india["Startup"]==startup_name]["InvestmentAmount"].max())+"cr")
    
    st.subheader("Cities")
    st.dataframe(startup_city,hide_index=True)
    
    st.subheader("Investors")
    st.dataframe(startup_investor,hide_index=True)
    
    st.subheader("Amount of Investment By Investors")
    st.dataframe(startup_investment,hide_index=True)
    st.subheader("Invested Amount By Investors")
    fig,ax=plt.subplots(figsize=(5,4))
    ax.bar(x=startup_investment["Investors"],height=startup_investment["InvestmentAmount"])
    ax.tick_params(axis="x",rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    
    
        

option=st.sidebar.selectbox("select one",["Overall Analysis","Startup","Investor"])
if option=="Overall Analysis":
    st.write("Welcome to the India's startup ecosystem. This dynamic dashboard decodes millions of data points into actionable intelligence, mapping the capital flows that shape our economic future. Track high-velocity funding rounds, trace macroeconomic shifts across key tech hubs, and uncover sector-specific trajectories in real time. Designed for investors, founders, and analysts alike, this page bridges the gap between raw financial metrics and the narrative of Indian innovation. Dive in to spot emerging trends, monitor ecosystem health, and see exactly where the next wave of disruption is being capitalized.")
    btn3=st.sidebar.button("Overall Investment")
    if btn3:
      st.balloons()
      overall_investement=overall(startup_india)
elif option=="Startup":
    st.write("Explore the tabs to uncover granular insights into the micro-mobility, fintech, and enterprise solutions shaping the future.")
    selected_startup=st.sidebar.selectbox("Choose Startup" ,sorted(cleaned["Startup"].unique().tolist()))
    btn1=st.sidebar.button("Find Startup Details")
    if btn1:
     startup(selected_startup)
    
elif option=="Investor": 
    st.write("""This interactive dashboard tracks the velocity and distribution of capital across the Indian startup ecosystem from 2020 to 2025.
By eliminating tracking noise and consolidating raw entry duplicates, the data provides an accurate look at true market behaviors.
Investors can dynamically analyze funding rounds, geographic concentration hubs, and sectoral shifts across major tech verticals.
The interface maps investment flow patterns, showcasing where leading venture capitals and consortiums are concentrating their equity.
Use the interactive filters to evaluate funding trends, track historical round values, and uncover emerging market opportunities.""")
    selected_investor=st.sidebar.selectbox("Choose Investors" ,sorted(set(startup_india["Investors"].str.split(",").sum())))
    btn2=st.sidebar.button("Find Investors Details")
    if btn2:
        select_investor(selected_investor)
    
    




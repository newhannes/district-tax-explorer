##### ===== Streamlit Data Explorer ===== #####
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from helper_functions import rank_district_df, rank_district, plot_district, ranked_by_variable, ordinaltg
hunter = "#002829"
emerald = "#004647"
jade = "#84AE95"
pearl = "#D6E5DC"
gold = "#967D4A"

### --- Load Data --- ###
df = pd.read_excel("data/all_agi_mikevars_mems.xlsx")

### --- Streamlit App --- ###
st.image("inputs/HBR_Logo_Primary.png")
st.title("Congressional District Tax Data Explorer")
st.write("Select District Mode to explore a specific district or Variable Mode to rank all districts by a specific variable. Select inputs or enter text to filter the options.")

mode = st.selectbox("Select Mode", ["District Mode", "Variable Mode", "About"])

if mode == "District Mode":
    district = st.selectbox("Select District", df["District"].unique())
    district_df = rank_district_df(district)
    st.header(f"{district} Report, All Variables")
    st.write("Represented by", df[df["District"] == district]["REPRESENTATIVE"].values[0], "(", df[df["District"] == district]["PARTY"].values[0], ")")
    st.write(district_df)
    st.header(f"Selected Variables for {district}")
    variable1 = st.selectbox("Select Variable 1", df.columns[3:])
    variable2 = st.selectbox("Select Variable 2", df.columns[3:])
    if st.button("Run Selected Variables"):
        st.subheader(f"{variable1}")
        rank_district(district, variable1)
        plot_district(district, variable1)
        st.subheader(f"{variable2}")
        rank_district(district, variable2)
        plot_district(district, variable2)
        
if mode == "Variable Mode":
    st.header("Rank Congressional Districts by Variable")
    variable = st.selectbox("Select Variable (or start typing)", df.columns[3:])
    
    if st.button("Rank by Variable"):
        st.header(f"{variable}")
        ranked_df = ranked_by_variable(variable)
        st.write(ranked_df)

elif mode == "About":
    st.header("About")
    st.write("Data are based on the individual income tax returns processed by the IRS during the 2022 calendar year (tax year 2021). The districts are for the 177th Congress. Amounts (not numbers) are in thousands of dollars.")
    st.write("The representative listed is the current (118th Congress) representative. Between redistricting and vacancies, 13 districts do not have a representative in the data.")
    if st.button("Districts without a representative: "):
        st.write(df[df["REPRESENTATIVE"].isnull()]["District"])
    st.write("The IRS has 167 variables for each district. The variables available in this app have been selected for their relevance.")
    if st.button("Selected variables: "):
        st.write(df.columns[3:])
    if st.button("All available variables: "):
        all_vars = pd.read_excel("data/all_variables_clean.xlsx")["description"]
        st.write(all_vars)
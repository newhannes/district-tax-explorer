##### ===== Streamlit Data Explorer ===== #####
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
hunter = "#002829"
emerald = "#004647"
jade = "#84AE95"
pearl = "#D6E5DC"
gold = "#967D4A"

### --- Load Data --- ###
df = pd.read_excel("data/cleaned_cds_all_agi.xlsx")
### --- Helper Functions --- ###
## Helper Functions ##
def rank_district_df(district):
    district_df = df[df["District"] == district].drop(columns="District").T
    district_df.columns = ["Value"]
    district_df["Variable"] = district_df.index
    ranks = []
    for var in district_df["Variable"]:
        ranked_df = df.sort_values(by=var, ascending=False).reset_index() # Create a new DataFrame that ranks each district based on the variable
        rank = ranked_df[ranked_df['District'] == district].index[0] + 1 # Find the rank of the specified district
        ranks.append(rank)
    district_df["Rank"] = ranks
    district_df["Percentile"] = [f"{round(100-(rank/len(df))*100)}%" for rank in ranks]
    district_df = district_df.sort_values(by="Rank", ascending=True).drop(columns="Variable")
    return district_df[["Rank", "Percentile", "Value"]]

def rank_district(district, variable):
    ranked_df = df.sort_values(by=variable, ascending=False).reset_index() # Create a new DataFrame that ranks each district based on the variable
    rank = ranked_df[ranked_df['District'] == district].index[0] + 1 # Find the rank of the specified district
    rank_str = f"Rank: <b>#{rank}</b>"
    return st.markdown(rank_str, unsafe_allow_html=True)

def plot_district(district, variable):
    # Find the highest, lowest, and district's value for the variable
    highest_district = df.loc[df[variable].idxmax()]["District"]
    highest_value = df[variable].max()
    
    lowest_district = df.loc[df[variable].idxmin()]["District"]
    lowest_value = df[variable].min()
    
    district_value = df[df['District'] == district][variable].values[0]

    # Calculate the average value for the variable
    median = df[variable].median()

  # Create a bar chart with the highest, district's, and lowest value
    fig = go.Figure()
    #color_dict = {highest_district: emerald, district: gold, lowest_district: jade}
    hoverlabel = dict(namelength=-1)
    if district == highest_district:
        fig.add_trace(go.Bar(name='District (Highest)', x=[district], y=[district_value], marker=dict(color=gold), hoverlabel=hoverlabel))
        fig.add_trace(go.Bar(name='Lowest', x=[lowest_district], y=[lowest_value], marker=dict(color=jade), hoverlabel=hoverlabel))
        note = f'{district} is the district with the highest {variable}.'
    elif district == lowest_district:
        fig.add_trace(go.Bar(name='District (Lowest)', x=[district], y=[district_value], marker=dict(color=gold), hoverlabel=hoverlabel))
        fig.add_trace(go.Bar(name='Highest', x=[highest_district], y=[highest_value], marker=dict(color=emerald), hoverlabel=hoverlabel))
        note = f'{district} is the district with the lowest {variable}.'
    else:
        fig.add_trace(go.Bar(name='Highest', x=[highest_district], y=[highest_value], marker=dict(color=emerald), hoverlabel=hoverlabel))
        fig.add_trace(go.Bar(name='District', x=[district], y=[district_value], marker=dict(color=gold), hoverlabel=hoverlabel))
        fig.add_trace(go.Bar(name='Lowest', x=[lowest_district], y=[lowest_value], marker=dict(color=jade), hoverlabel=hoverlabel))
        note = None

   # Add a line to the bar chart that represents the median value
    fig.add_shape(type="line",x0=-0.5,y0=median,x1=2.5,y1=median,line=dict(color="grey", width=4, dash="dashdot"))

     # Add a little grey line to the legend
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="Median", line=dict(color="grey", width=2), showlegend=True))


    # Update the layout
    title = f'<b>{variable}</b> in <b>{district}</b> compared to highest and lowest' if note is None else f'<b>{variable}</b> in <b>{district}</b> compared to highest and lowest ({note})'
    fig.update_layout(title="", xaxis_title='District', yaxis_title=variable)

    return st.plotly_chart(fig)

def ranked_by_variable(variable):
    ranked_df = df[["District", variable]].sort_values(by=variable, ascending=False).reset_index(drop=True) # Create a new DataFrame that ranks each district based on the variable
    return ranked_df


### --- Streamlit App --- ###
st.image("inputs/HBR_Logo_Primary.png")
st.title("Congressional District Tax Data Explorer")
st.write("Select District Mode to explore a specific district or Variable Mode to rank all districts by a specific variable. Select inputs or enter text to filter the options.")

mode = st.sidebar.selectbox("Select Mode", ["District Mode", "Variable Mode", "About"])

if mode == "District Mode":
    district = st.sidebar.selectbox("Select District", df["District"].unique())
    district_df = rank_district_df(district)
    st.header(f"{district} Report, All Variables")
    st.write(district_df)
    variable1 = st.sidebar.selectbox("Select Variable 1", df.columns[1:])
    variable2 = st.sidebar.selectbox("Select Variable 2", df.columns[1:])
    
    # if st.sidebar.button("District Summary"):
    #     st.header(f"{district}")
    #     st.write(district_df)
    if st.sidebar.button("Run Selected Variables"):
        st.header(f"Selected Variables for {district}")
        st.subheader(f"{variable1}")
        rank_district(district, variable1)
        plot_district(district, variable1)
        st.subheader(f"{variable2}")
        rank_district(district, variable2)
        plot_district(district, variable2)
        
if mode == "Variable Mode":
    st.header("Rank Congressional Districts by Variable")
    variable = st.sidebar.selectbox("Select Variable (or start typing)", df.columns[1:])
    
    if st.sidebar.button("Rank by Variable"):
        st.header(f"{variable}")
        ranked_df = ranked_by_variable(variable)
        st.write(ranked_df)

elif mode == "About":
    st.header("About")
    st.write("Data are based on the individual income tax returns processed by the IRS during the 2022 calendar year (tax year 2021). The districts are for the 177th Congress. Amounts (not numbers) are in thousands of dollars.")
    st.write("The IRS has 167 variables for each district. The variables available in this app have been selected for their relevance.")
    st.write("Available variables: ")
    st.write(df.columns[1:])
# Import libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
from streamlit_extras.metric_cards import style_metric_cards
import matplotlib.pyplot as plt

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Read the data
df = pd.read_csv("dataset.csv")

# Change value column to numerical values
df["Value to the person"] = df["Value to the person"].map({"High": 3, "Medium": 2, "Low": 1})

# Main title
st.markdown("<h1 style='text-align: center; color: #19A7CE'>Group 12: Facul Team - Activity Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Shared Activity Exploration
st.markdown("<div style='text-align: center;'>"
            "<h3 style='color: #19A7CE'>Shared Activity Exploration</h3>"
            "</div>", unsafe_allow_html=True)

# Duration Metrics Section
st.markdown(
    """
    <style>
    /* Custom CSS to change the font color of metric labels and values to dark gray */
    .stMetricLabel {
        color: #333333 !important;  /* Dark gray color */
    }
    .stMetricValue {
        color: #333333 !important;  /* Dark gray color */
    }
    </style>

    <div style='
        background-color: #19A7CE;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
    '>
    <p style='font-weight: bold; color: white'>How Much Time Do We Spend on Different Activities Every Day? (In Hours and Minutes)</p>
    </div>
    """
    , unsafe_allow_html=True
)

df_duration = df.groupby("Category")["Duration in minutes"].sum().reset_index()
df_duration = df_duration.sort_values(by="Duration in minutes", ascending=False).head(7)

metric_cols = st.columns(len(df_duration))
for col, row in zip(metric_cols, df_duration.itertuples()):
    total_minutes = row._2 / df["Person"].nunique() / df["Date"].nunique()
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    col.metric(label=row.Category, value=f"{hours} hrs {minutes} min")

style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")



# Create 2 columns with equal width
col1, col2 = st.columns(2)

# Place the value plot in the second column
with col1:
  st.markdown(
    """
    <div style='
      background-color: #19A7CE;
      border-radius: 10px;
      padding: 20px;
      margin: 10px;
    '>
    <p style='text-align: center; font-weight: bold; color: white; color: white'>What Activities Matter Most to Us?</p>
    """
    , unsafe_allow_html=True
  )
  # Create a donut chart for activity category by duration for all people
  df_value = df.groupby("Category")["Value to the person"].mean().reset_index()
  fig_value = px.pie(df_value, values="Value to the person", names="Category", hole=0.4)
  fig_value.update_traces(textinfo="percent+label")
  fig_value.update_layout(showlegend=False, autosize=True)  # Set width to col2.width
  st.plotly_chart(fig_value)

# Group the data by category and how they felt
with col2:
  st.markdown(
    """
    <div style='
      background-color: #19A7CE;
      border-radius: 10px;
      padding: 20px;
      margin: 10px;
    '>
    <p style='text-align: center; font-weight: bold; color: white; color: white'>What Dominant Emotions Do We Experience During Different Activities?</p>
    """
    , unsafe_allow_html=True
  )
  grouped = df[df["Category"] != "Waking Up"].groupby(["Category", "How they felt"]).size().reset_index(name="Count")
  most_common = grouped.loc[grouped.groupby("Category")["Count"].idxmax()]
  most_common = most_common.sort_values(by="Count", ascending=False)
  fig = px.bar(most_common, x="Category", y="Count", color="How they felt")
  fig.update_layout(autosize=True)
  most_common = most_common.sort_values(by="Count", ascending=False) # sort in descending order
  st.plotly_chart(fig)

# Define a function to create a word cloud from a dataframe
def create_word_cloud(df, category):
    # Filter the dataframe by category
    df = df[df["Category"] == category]
    # Create a word cloud object
    wc = WordCloud(background_color="white", width=800, height=400)
    # Generate the word cloud from the activity column
    wc.generate(" ".join(df["Activity"]))
    # Create a figure and an axis
    fig, ax = plt.subplots()
    # Plot the word cloud on the axis
    ax.imshow(wc, interpolation="bilinear")
    # Remove the axis labels and ticks
    ax.axis("off")
    # Set the title of the figure
    fig.suptitle(f"{category}", fontsize=15)
    # Return the figure
    return fig

# Add a horizontal line to separate each person
st.markdown("---")

# Create a word cloud for activities for leisure, work, and personal categories
st.markdown("<h3 style='text-align: center; color: #19A7CE'>What Are the Most Popular Activities in Each Category?</h3>", unsafe_allow_html=True)
# Create three columns with equal width
col1, col2, col3 = st.columns(3)
# Place the leisure word cloud in the first column
with col1:
  fig_leisure = create_word_cloud(df, "Leisure")
  st.pyplot(fig_leisure)
# Place the work word cloud in the second column
with col2:
  fig_work = create_word_cloud(df, "Work/Acads")
  st.pyplot(fig_work)
# Place the personal word cloud in the third column
with col3:
  fig_personal = create_word_cloud(df, "Others")
  st.pyplot(fig_personal)

# Add a horizontal line to separate each person
st.markdown("---")

# Loop through all the persons
for person in df["Person"].unique():

  # Create a title for the brochure
  st.subheader(f"Activity Analysis for {person}")

  # Filter the data by the current person
  df_person = df[df["Person"] == person]

  # Create two columns with equal width
  col1, col2, col3 = st.columns(3)
  # Place the duration plot in the first column
  with col1:
    df_person_duration = df_person.groupby("Category")["Duration in minutes"].sum().reset_index()
    df_person_duration["Duration in hours"] = df_person_duration["Duration in minutes"] / 60
    df_person_duration = df_person_duration.sort_values(by="Duration in hours", ascending=False).head(5)
    fig_person_duration = px.bar(df_person_duration, x="Duration in hours", y="Category", orientation="h", color_discrete_sequence=['#0068c9'])
    fig_person_duration.update_layout(xaxis_title="Duration in hours", yaxis_title="Category")
    fig_person_duration.update_layout(showlegend=False, autosize=True)
    fig_person_duration.update_xaxes(tickmode='linear', dtick=10)
    st.plotly_chart(fig_person_duration)
    st.markdown(
    """
    <div style='
      background-color: #19A7CE;
      border-radius: 10px;
      padding: 20px;
      margin: 10px;
    '>
    <p style='text-align: center; font-weight: bold; color: white'>How Do They Spend Most of Their Time?</p>
    """
    , unsafe_allow_html=True
  )
  # Place the value plot in the second column
  with col2:
    df_person_value = df_person.groupby("Category")["Value to the person"].mean().reset_index()
    df_person_value = df_person_value.sort_values(by="Value to the person", ascending=False).head(5)
    fig_person_value = px.bar(df_person_value, x="Value to the person", y="Category", orientation="h", color_discrete_sequence=['#83c9ff'])
    fig_person_value.update_layout(xaxis_title="Value to the person", yaxis_title="Category")
    fig_person_value.update_layout(showlegend=False, autosize=True)
    st.plotly_chart(fig_person_value)
    st.markdown(
    """
    <div style='
      background-color: #19A7CE;
      border-radius: 10px;
      padding: 20px;
      margin: 10px;
    '>
    <p style='text-align: center; font-weight: bold; color: white'>What Activities Matter Most to Them?</p>
    """
    , unsafe_allow_html=True
  )
  with col3:
    # Group the data by category and how the person felt in the loop
    grouped_person = df_person.groupby(["Category", "How they felt"]).size().reset_index(name="Count")
    most_common_person = grouped_person.loc[grouped_person.groupby("Category")["Count"].idxmax()]

    # Calculate the total counts for each category
    total_counts = grouped_person.groupby('Category')['Count'].sum().reset_index()

    # Sort categories by total counts in descending order to get the order
    sorted_categories = total_counts.sort_values(by='Count', ascending=False)['Category']

    # Create a categorical data type with the categories in the order you want
    most_common_person['Category'] = pd.Categorical(most_common_person['Category'], 
                                                    categories=sorted_categories, 
                                                    ordered=True)

    # Now sort the dataframe based on this categorical datatype
    most_common_person.sort_values('Category', inplace=True)

    # Plot the sorted data
    fig_person = px.bar(most_common_person, x='Category', y='Count', color='How they felt')

    # Update layout
    fig_person.update_layout(autosize=True)

    # Display the plot
    st.plotly_chart(fig_person)
    st.markdown(
    """
    <div style='
      background-color: #19A7CE;
      border-radius: 10px;
      padding: 20px;
      margin: 10px;
    '>
    <p style='text-align: center; font-weight: bold; color: white'>What Dominant Emotions Do They Experience During Different Activities?</p>
    """
    , unsafe_allow_html=True
    )

  
  # Add a horizontal line to separate each person
  st.markdown("---")

# Create a list of team members in a paragraph element colored 19A7CE
st.markdown("<p style='text-align: center; color: #19A7CE'>IT 365 - G1- Group 12 - Facul Team<br>Members:<br>Badilla, Mark Kenneth S. - Leader<br>Restauro, Hannah Dylene B.<br>Villanueva, Richelle</p>", unsafe_allow_html=True)

# Import libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv("dataset.csv")

# Change value column to numerical values
df["Value to the person"] = df["Value to the person"].map({"High": 3, "Medium": 2, "Low": 1})

# Create a donut chart for activity category by duration for all people
st.subheader("Activity Category by Duration for All People")
df_duration = df.groupby("Category")["Duration in minutes"].sum().reset_index()
fig_duration = px.pie(df_duration, values="Duration in minutes", names="Category", hole=0.4)
fig_duration.update_traces(textinfo="percent+label")
st.plotly_chart(fig_duration)

# Create a donut chart for activity category by value for all people
st.subheader("Activity Category by Value for All People")
df_value = df.groupby("Category")["Value to the person"].mean().reset_index()
fig_value = px.pie(df_value, values="Value to the person", names="Category", hole=0.4)
fig_value.update_traces(textinfo="percent+label")
st.plotly_chart(fig_value)

# Group the data by category and how they felt
st.subheader("Most Common Feeling Per Category")
grouped = df.groupby(["Category", "How they felt"]).size().reset_index(name="Count")
most_common = grouped.loc[grouped.groupby("Category")["Count"].idxmax()]
fig = px.bar(most_common, x="Category", y="Count", color="How they felt")
st.plotly_chart(fig)

# Loop through all the persons
for person in df["Person"].unique():

  # Create a title for the brochure
  st.title(f"Activity Analysis for {person}")

  # Filter the data by the current person
  df_person = df[df["Person"] == person]

  # Create a bar chart for activity category by duration individually
  st.subheader("Activity Category by Duration Individually")
  df_person_duration = df_person.groupby("Category")["Duration in minutes"].sum().reset_index()
  fig_person_duration = px.bar(df_person_duration, x="Duration in minutes", y="Category", orientation="h")
  fig_person_duration.update_layout(xaxis_title="Duration in minutes", yaxis_title="Category")
  st.plotly_chart(fig_person_duration)

  # Create a bar chart for activity category by value individually
  st.subheader("Activity Category by Value Individually")
  df_person_value = df_person.groupby("Category")["Value to the person"].mean().reset_index()
  fig_person_value = px.bar(df_person_value, x="Value to the person", y="Category", orientation="h")
  fig_person_value.update_layout(xaxis_title="Value to the person", yaxis_title="Category")
  st.plotly_chart(fig_person_value)

  # Group the data by category and how the person felt in the loop
  # This line creates a subheader with the person's name and their most common feeling per category
  st.subheader(f"{person}'s Most Common Feeling Per Category")
  grouped_person = df_person.groupby(["Category", "How they felt"]).size().reset_index(name="Count")
  most_common_person = grouped_person.loc[grouped_person.groupby("Category")["Count"].idxmax()]
  fig_person = px.bar(most_common_person, x="Category", y="Count", color="How they felt")
  st.plotly_chart(fig_person)
  
  # Add a horizontal line to separate each person
  st.markdown("---")

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
    fig.suptitle(f"Word Cloud for {category} Category", fontsize=20)
    # Return the figure
    return fig

# Create a word cloud for activities for leisure category
fig_leisure = create_word_cloud(df, "Leisure")
st.pyplot(fig_leisure)

# Create a word cloud for activities for work category
fig_work = create_word_cloud(df, "Work")
st.pyplot(fig_work)

# Create a word cloud for activities for personal category
fig_personal = create_word_cloud(df, "Others")
st.pyplot(fig_personal)
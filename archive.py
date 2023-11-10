# zephyr: code a plotly streamlit dashboard based on the ff information:
import streamlit as st
import pandas as pd
import plotly.express as px

# load the dataset
df = pd.read_csv("dataset.csv")

# create a sidebar for selecting the person
person = st.sidebar.selectbox("Select a person", df["Person"].unique())

# filter the data by the person
df_person = df[df["Person"] == person]

# create a title and a subtitle
st.title(f"Daily Activities Analysis for {person}")
st.subheader("This dashboard shows the insights about the daily activities of the selected person.")

# add the information for context
st.write(f"""
This report presents the analysis of our daily activities from October 10 to October 23, 2023. The data source is our two-week log of our daily activities, which we recorded using a spreadsheet template. We logged the date, time, activity category, how we felt, value to us, and duration in minutes for each activity we did during the day. We dropped October 9 and 24 from the analysis to keep our dates consistent. The purpose of this report is to gain insights about our daily lives, such as how we spend our time, what activities make us happy or bored, and what activities are valuable or not to us. The main research questions we want to answer are:

- How does the activity category affect our mood and value perception?
- What are the most common and least common activities among us?
- How does the duration of the activity vary by the activity category and the person?
- Is there a relationship between the time of the day and the activity category or our mood?

We grouped our activities into the following categories:

- Sleeping: This group includes activities that involve resting, sleeping, or preparing for bed. Examples are sleeping, bedtime, wind down and relax, nighttime reading, etc.
- Waking up: This group includes activities that involve getting ready for the day, such as waking up, morning routine, morning meditation and stretching, etc.
- Personal hygiene: This group includes activities that involve taking care of one’s body, such as bath, skincare, makeup, exercise and freshen up, etc.
- Eating: This group includes activities that involve preparing or consuming food, such as breakfast, lunch, dinner, snack, cook, eat, etc.
- Commuting: This group includes activities that involve traveling to or from a destination, such as travel to school, travel to home, travel to IT park, go to the mall, etc.
- Class: This group includes activities that involve attending, preparing, or reviewing for class, such as class, attending class, getting ready for class, study, homework, exam, etc.
- Leisure: This group includes activities that involve entertainment, relaxation, or hobbies, such as watch Netflix, watch TikTok videos, watch movies, social media, reading, creative hobbies, etc.
- Work: This group includes activities that involve professional or academic tasks, such as do assignments, project, reporting, consultation, etc.
- Others: This group includes activities that do not fit into any of the above groups, such as shopping, karaoke, met friends for coffee, visit IT park, etc.
""")

# create a pie chart for the activity category
fig1 = px.pie(df_person, names="Activity Category", title="Activity Category Distribution")
st.plotly_chart(fig1)
# add an explanation for the pie chart
st.write(f"""
The pie chart shows the proportion of each activity category in the total time spent by {person} during the two-week period. 
This can help us understand how {person} allocates their time among different types of activities. 
For example, we can see that {person} spent the most time on **{df_person['Activity Category'].value_counts().idxmax()}** and the least time on **{df_person['Activity Category'].value_counts().idxmin()}**.
""")

# create a box plot for the mood
fig2 = px.box(df_person, x="Activity Category", y="How they felt", title="Mood by Activity Category")
st.plotly_chart(fig2)
# add an explanation for the box plot
st.write(f"""
The box plot shows the distribution of the mood for each activity category by {person}. 
This can help us understand how the activity category affects the way {person} feels. 
For example, we can see that {person} felt the most **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmax()[1]}** and the least **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmin()[1]}** when they did **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmax()[0]}** activities, while they felt the most **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmin()[1]}** and the least **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmax()[1]}** when they did **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmin()[0]}** activities.
""")


# create a dictionary to map the string values to numeric values
value_map = {"MediumHigh": 3, "HighLowHigh": 4, "Medium": 2, "High": 5, "Low": 1}

# apply the map to the column
df_person["Value to the person"] = df_person["Value to the person"].map(value_map)

# create a bar chart for the value perception
fig3 = px.bar(df_person, x="Activity Category", y="Value to the person", color="Time", title="Value Perception by Activity Category and Time")
st.plotly_chart(fig3)

st.write(f"""
The bar chart shows the average value perception for each time and activity category by {person}. 
This can help us understand how the time and activity category affect the way {person} values their time. 
For example, we can see that {person} valued their time the highest when they did **{df_person.groupby(['Time', 'Activity Category'])['Value to the person'].mean().idxmax()[1]}** activities in the **{df_person.groupby(['Time', 'Activity Category'])['Value to the person'].mean().idxmax()[0]}** and the lowest when they did **{df_person.groupby(['Time', 'Activity Category'])['Value to the person'].mean().idxmin()[1]}** activities in the **{df_person.groupby(['Time', 'Activity Category'])['Value to the person'].mean().idxmin()[0]}**.
""")

# create a bar chart for the duration of the activity
fig4 = px.bar(df_person, x="Time", y="Duration in minutes", color="Activity Category", title="Duration of the Activity by Time and Category")
st.plotly_chart(fig4)
# add an explanation for the line chart
st.write(f"""
The bar chart shows the duration of each activity by the time and category for {person}. 
This can help us understand how the duration of the activity varies by the time of the day and the type of the activity. 
For example, we can see that {person} tended to do longer activities in the **{df_person.groupby('Time')['Duration in minutes'].mean().idxmax()}** and shorter activities in the **{df_person.groupby('Time')['Duration in minutes'].mean().idxmin()}**, and that the longest activity category was **{df_person.groupby('Activity Category')['Duration in minutes'].mean().idxmax()}** and the shortest activity category was **{df_person.groupby('Activity Category')['Duration in minutes'].mean().idxmin()}**.
""")

# create a scatter plot for the relationship between the time of the day and the mood
fig5 = px.scatter(df_person, x="Time", y="How they felt", color="Activity Category", title="Relationship between the Time of the Day and the Mood")
st.plotly_chart(fig5)
# add an explanation for the scatter plot
st.write(f"""
The scatter plot shows the relationship between the time of the day and the mood for each activity category by {person}. 
This can help us understand how the time of the day influences the way {person} feels when they do different types of activities. 
For example, we can see that {person} felt more **{df_person.groupby('Time')['How they felt'].value_counts().idxmax()[1]}** in the **{df_person.groupby('Time')['How they felt'].value_counts().idxmax()[0]}** and more **{df_person.groupby('Time')['How they felt'].value_counts().idxmin()[1]}** in the **{df_person.groupby('Time')['How they felt'].value_counts().idxmin()[0]}**, and that the activity category that made {person} feel the most **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmax()[1]}** was **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmax()[0]}** and the activity category that made {person} feel the most **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmin()[1]}** was **{df_person.groupby('Activity Category')['How they felt'].value_counts().idxmin()[0]}**.
""")
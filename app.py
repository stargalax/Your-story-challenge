import streamlit as st
import pandas as pd
import snowflake.connector
import pydeck as pdk
import matplotlib.pyplot as plt

# Helper function to assign colors to types
def assign_colors(types):
    base_colors = [
        [255, 0, 0],     # red
        [0, 0, 255],     # blue
        [255, 165, 0],   # orange
        [0, 128, 0],     # green
        [128, 0, 128],   # purple
        [255, 192, 203], # pink
        [0, 255, 255],   # cyan
        [128, 128, 0],   # olive
        [0, 100, 0],     # dark green
        [139, 69, 19]    # brown
    ]
    color_map = {}
    for i, t in enumerate(types):
        color_map[t] = base_colors[i % len(base_colors)]
    return color_map

# Function to get row color
def get_row_color(row, color_map, search_name):
    if search_name and search_name in row['HERITAGE_NAME'].lower():
        return [0, 255, 0, 255]  # bright green for search matches
    return color_map.get(row['HERITAGE_TYPE'], [150, 150, 150]) + [160]  # fallback color

# Snowflake data fetch
@st.cache_data(show_spinner=True)
def get_data():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

    query = """
        SELECT HERITAGE_NAME, HERITAGE_TYPE, LAT, LON, CITY_NAME
        FROM HERITAGE_DATA_TN
        WHERE STATE = 'Tamil Nadu'
        AND LAT IS NOT NULL AND LON IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- Main app ---
st.set_page_config(page_title="Tamil Nadu Heritage Map", layout="wide")
st.title("Tamil Nadu Heritage Map")

df = get_data()

# Clean up data
df['HERITAGE_TYPE'] = df['HERITAGE_TYPE'].str.strip().str.title()
df['HERITAGE_NAME'] = df['HERITAGE_NAME'].str.strip()
df['CITY_NAME'] = df['CITY_NAME'].str.strip().str.title()

heritage_types = df['HERITAGE_TYPE'].unique()
cities = df['CITY_NAME'].unique()

# Sidebar menu to switch between views
view_mode = st.sidebar.radio("Choose View", ["Map View", "Analytics"])

if view_mode == "Map View":

    st.sidebar.header("Filters")

    # Reset button
    if st.sidebar.button("🔄 Reset Filters"):
        st.rerun()
    # Filter selection
    #selected_types = st.sidebar.multiselect("Filter by Heritage Type", heritage_types, default=heritage_types.tolist())
    selected_types = st.sidebar.multiselect("Filter by Heritage Type", heritage_types)

    search_name = st.sidebar.text_input("Search Heritage Name").strip().lower()

    # Filter logic
    filtered_df = df.copy()

    if selected_types:
        filtered_df = filtered_df[filtered_df['HERITAGE_TYPE'].isin(selected_types)]

    if search_name:
        filtered_df = filtered_df[
            filtered_df['HERITAGE_NAME'].str.lower().str.contains(search_name, na=False)
        ]

    # Assign colors
    color_map = assign_colors(df['HERITAGE_TYPE'].unique())
    filtered_df['COLOR'] = filtered_df.apply(lambda row: get_row_color(row, color_map, search_name), axis=1)

    # Show search results with map links
    st.sidebar.markdown("### Search Results")
    if filtered_df.empty:
        st.sidebar.write("No matching heritage sites.")
    else:
        for _, row in filtered_df.iterrows():
            name_query = row['HERITAGE_NAME'].replace(' ', '+')
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={name_query}"
            st.sidebar.markdown(f"- [{row['HERITAGE_NAME']}]({gmaps_link})")

    st.write(f"Showing {len(filtered_df)} records on map")

    # Show map
    midpoint = (filtered_df['LAT'].mean(), filtered_df['LON'].mean()) if not filtered_df.empty else (df['LAT'].mean(), df['LON'].mean())

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=7,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filtered_df if not filtered_df.empty else df.assign(COLOR=df.apply(lambda row: get_row_color(row, color_map, ""), axis=1)),
                get_position='[LON, LAT]',
                get_color='COLOR',
                get_radius=5000,
                pickable=True,
            ),
        ],
        tooltip={"text": "{HERITAGE_NAME}\nType: {HERITAGE_TYPE}"}
    ))

elif view_mode == "Analytics":
    st.header("Heritage Analytics")

    # Pie chart: distribution of heritage by city
    city_counts = df['CITY_NAME'].value_counts()
    st.subheader("Heritage Distribution by City")
    
    # Centered pie chart
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(city_counts, labels=city_counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 8})
        ax1.axis('equal')
        st.pyplot(fig1)

    # Bar chart: heritage type distribution in a selected city
    st.subheader("Heritage Type Distribution in Selected City")
    selected_city = st.selectbox("Select City", sorted(cities))

    city_df = df[df['CITY_NAME'] == selected_city]
    type_counts = city_df['HERITAGE_TYPE'].value_counts()

    # Centered bar chart
    col4, col5, col6 = st.columns([1, 2, 1])
    with col5:
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.bar(type_counts.index, type_counts.values, color='skyblue')
        ax2.set_xlabel("Heritage Type", fontsize=9)
        ax2.set_ylabel("Count", fontsize=9)
        ax2.set_title(f"{selected_city}", fontsize=10)
        ax2.tick_params(axis='x', rotation=45, labelsize=8)
        ax2.tick_params(axis='y', labelsize=8)
        st.pyplot(fig2)

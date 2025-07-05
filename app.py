import streamlit as st
import pandas as pd
#import snowflake.connector
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
        return [0, 255, 0, 255]  # bright green
    return color_map.get(row['HERITAGE_TYPE'], [150, 150, 150]) + [160]

# Fetch from Snowflake
@st.cache_data(show_spinner=True)
# def get_data():
#     conn = snowflake.connector.connect(
#         user=st.secrets["snowflake"]["user"],
#         password=st.secrets["snowflake"]["password"],
#         account=st.secrets["snowflake"]["account"],
#         warehouse=st.secrets["snowflake"]["warehouse"],
#         database=st.secrets["snowflake"]["database"],
#         schema=st.secrets["snowflake"]["schema"]
#     )

#     query = """
#         SELECT STATE, CITY_NAME, HERITAGE_NAME, HERITAGE_TYPE, LAT, LON
#         FROM HERITAGE_DATA
#         WHERE LAT IS NOT NULL AND LON IS NOT NULL
#     """
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df
@st.cache_data(show_spinner=True)
def get_data():
    import sqlite3
    conn = sqlite3.connect("heritage.db")
    query = """
        SELECT STATE, CITY_NAME, HERITAGE_NAME, HERITAGE_TYPE, LAT, LON
        FROM HERITAGE_DATA
        WHERE LAT IS NOT NULL AND LON IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Main app
st.set_page_config(page_title="India Heritage Map", layout="wide")
st.title("India Heritage Map")

df = get_data()

# Clean up data
df['STATE'] = df['STATE'].str.strip().str.title()
df['CITY_NAME'] = df['CITY_NAME'].str.strip().str.title()
df['HERITAGE_TYPE'] = df['HERITAGE_TYPE'].str.strip().str.title()
df['HERITAGE_NAME'] = df['HERITAGE_NAME'].str.strip()

heritage_types = df['HERITAGE_TYPE'].unique()
states = sorted(df['STATE'].unique())
cities = df['CITY_NAME'].unique()

view_mode = st.sidebar.radio("Choose View", ["Map View", "Analytics"])
if view_mode == "Map View":
    st.sidebar.header("Filters")

    if st.sidebar.button("🔄 Reset Filters"):
        st.rerun()

    selected_states = st.sidebar.multiselect("Filter by State", states)
    
    # Dynamic heritage type filter based on selected states
    if selected_states:
        filtered_df = df[df['STATE'].isin(selected_states)]
        filtered_types_for_states = filtered_df['HERITAGE_TYPE'].unique()
        selected_types = st.sidebar.multiselect("Filter by Heritage Type", sorted(filtered_types_for_states))
    else:
        filtered_df = df.copy()
        #selected_types = st.sidebar.multiselect("Filter by Heritage Type", sorted(heritage_types))
        heritage_types = df['HERITAGE_TYPE'].dropna().unique()
        heritage_types = [t for t in heritage_types if str(t).strip() != '']
        selected_types = st.sidebar.multiselect("Filter by Heritage Type", sorted(heritage_types))


    # Apply heritage type filter
    if selected_types:
        filtered_df = filtered_df[filtered_df['HERITAGE_TYPE'].isin(selected_types)]

    search_name = st.sidebar.text_input("Search Heritage Name").strip().lower()

    if search_name:
        filtered_df = filtered_df[filtered_df['HERITAGE_NAME'].str.lower().str.contains(search_name, na=False)]


    color_map = assign_colors(df['HERITAGE_TYPE'].unique())
    filtered_df['COLOR'] = filtered_df.apply(lambda row: get_row_color(row, color_map, search_name), axis=1)

    # Show results
    st.sidebar.markdown("### Search Results")
    if filtered_df.empty:
        st.sidebar.write("No matching heritage sites.")
    else:
        for _, row in filtered_df.iterrows():
            name_query = row['HERITAGE_NAME'].replace(' ', '+')
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={name_query}"
            st.sidebar.markdown(f"- [{row['HERITAGE_NAME']}]({gmaps_link})")

    st.write(f"Showing {len(filtered_df)} records on map")

    midpoint = (
        filtered_df['LAT'].mean(),
        filtered_df['LON'].mean()
    ) if not filtered_df.empty else (df['LAT'].mean(), df['LON'].mean())

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=5,
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
        tooltip={"text": "{HERITAGE_NAME}\nType: {HERITAGE_TYPE}\nState: {STATE}"}
    ))
elif view_mode == "Analytics":
    st.header("Heritage Analytics")

    # --- PIE CHART: State distribution with "Other" grouping ---
    st.markdown("### Heritage Distribution by State")

    state_counts = df['STATE'].value_counts()
    total_sites = state_counts.sum()
    major_states = state_counts[state_counts / total_sites > 0.04]
    minor_states = state_counts[state_counts / total_sites <= 0.04]

    # Data for pie chart
    pie_labels = major_states.index.tolist() + ['Other']
    pie_values = major_states.values.tolist() + [minor_states.sum()]

    # Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.markdown("#### 'Other' includes:")
        if not minor_states.empty:
            for state in minor_states.index:
                st.markdown(f"- {state}")
        else:
            st.markdown("No states grouped under 'Other'.")

    # --- BAR CHART: Heritage Type distribution by selected state ---
    st.markdown("### Heritage Type Distribution in Selected State")

    selected_state = st.selectbox("Select State", sorted(df['STATE'].unique()))

    state_df = df[df['STATE'] == selected_state]
    type_counts = state_df['HERITAGE_TYPE'].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(type_counts.index, type_counts.values, color='skyblue')
    ax2.set_xlabel("Heritage Type")
    ax2.set_ylabel("Count")
    ax2.set_title(f"Distribution of Heritage Types in {selected_state}")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

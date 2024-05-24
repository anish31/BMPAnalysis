#%%
## Attempt to create new dasboard
# Check and change directory
import os
current_directory = os.getcwd()
print("Current working directory:", current_directory)
os.chdir(r'C:\Users\hollaa\OneDrive - Jacobs\Python Codes\Python_codes')

# Main code
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

app_title = "BMP Analysis"
sub_title = "Compares the existing and proposed stage hydrographs"

# Function which calculates all the data related to stage hydrographs
def nd_Hydro(exdats, prdats, nd):
    # Analyzing the data
    metric_tit = '**Proposed Node Max with difference to existing node max**'
    ex_nd = exdats[(exdats['Node Name'] == nd) & (exdats['Sim'] == '100yr24hr')]
    pr_nd = prdats[(prdats['Node Name'] == nd) & (prdats['Sim'] == '100yr24hr')]
    ex_Max = ex_nd['Stage [ft]'].max()
    pr_Max = pr_nd['Stage [ft]'].max()
    diff = round(pr_Max - ex_Max,2)
    st.metric(label=metric_tit, value= f'{pr_Max} ft', delta= diff, delta_color= "inverse")
    
def nd_Plot(exdats, prdats, nd):
    # Plotting the data
    ex_nd = exdats[(exdats['Node Name'] == nd) & (exdats['Sim'] == '100yr24hr')]
    pr_nd = prdats[(prdats['Node Name'] == nd) & (prdats['Sim'] == '100yr24hr')]
    plt.plot(ex_nd['Relative Time [hrs]'], ex_nd['Stage [ft]'], label= 'Existing')
    plt.plot(pr_nd['Relative Time [hrs]'], pr_nd['Stage [ft]'], label= 'Proposed')# Customize the plot (add labels, title, legend, etc.)
    plt.xlabel('Time')
    plt.ylabel('Stage')
    plt.title(f'Hydrograph for Node {nd}')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
 
def maps(exFlood, prFlood, basins):
    gdf1 = gpd.read_file(exFlood)
    gdf2 = gpd.read_file(prFlood)
    gdf3 = gpd.read_file(basins)
    gdf1 = gdf1.to_crs("EPSG:4326")
    gdf2 = gdf1.to_crs("EPSG:4326")
    gdf3 = gdf3.to_crs("EPSG:4326")
    maap = folium.Map(location=(27.8232845539, -82.723599915), zoom_start=12)
    folium.GeoJson(data=gdf1.__geo_interface__, name="Test", style_function=lambda x: {
        'fillColor': '#8B008B',  # Dark Magenta fill
        'fillOpacity': 0.5,
        'color':'none', # boundary color
        'weight': 2,
    }).add_to(maap)
    folium.GeoJson(data=gdf2.__geo_interface__, name="Test", style_function=lambda x: {
        'fillColor': '#00FFFF',  # Dark Magenta fill
        'fillOpacity': 0.5,
        'color':'none', # boundary color
        'weight': 2,
    }).add_to(maap)
    folium.GeoJson(data=gdf3.__geo_interface__, name="Test", style_function=lambda x: {
        'fillColor': 'none',  # Dark Magenta fill
        'fillOpacity': 0.5,
        'color':'#000000', # boundary color
        'weight': 2,
    }).add_to(maap).add_child(folium.features.GeoJsonTooltip(['NODENAME']))
    
    st_map = st_folium(maap, width=1000, height=450)

# Use st.cache_data to cache data-related functions
@st.cache_data
def load_data():
    exdats = pd.read_csv(r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Joes_Cr_Existing_Bndry_update_roads.csv')
    prdats = pd.read_csv(r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Joes_Cr_AltB_Final_roads.csv')
    exFlood = r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Exist_BCA_100_plainTemp.shp'
    prFlood = r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\AltB_BCA_100_plainTemp.shp'
    basins = r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Basins.shp'
    return exdats, prdats, exFlood, prFlood, basins
    
def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(sub_title)
    
    # #Loading the data
    # exdats = pd.read_csv(r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Joes_Cr_Existing_Bndry_update_roads.csv')
    # prdats = pd.read_csv(r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Joes_Cr_AltB_Final_roads.csv') 
    # exFlood = (r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Exist_BCA_100_plainTemp.shp')
    # prFlood = r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\AltB_BCA_100_plainTemp.shp'
    # basins = r'C:\Users\hollaa\OneDrive - Jacobs\Joes_Creek\Flood_plains\FP_Dashboard\Basins.shp'
    # Load data using cached function
    exdats, prdats, exFlood, prFlood, basins = load_data()
    nd = 'NL0480'
    # metric_tit = '**Proposed Node Max with difference to existing node max**'
    
    # Analyzing the data
    
    #Display data
    nodLis = list(exdats['Node Name'].unique())
    nodLis = [ x for x in nodLis if not x.startswith('~')]
    nodLis.sort()
    nd = st.sidebar.selectbox('Node Name', nodLis)
    st.subheader('Node Max')
    nd_Hydro(exdats, prdats, nd)
    st.subheader('Hydrogprah')
    nd_Plot(exdats, prdats, nd)
    maps(exFlood,prFlood, basins)
    # ex_nd = exdats[(exdats['Node Name'] == nd) & (exdats['Sim'] == '100yr24hr')]
    # pr_nd = prdats[(prdats['Node Name'] == nd) & (prdats['Sim'] == '100yr24hr')]
    # ex_Max = ex_nd['Stage [ft]'].max()
    # pr_Max = pr_nd['Stage [ft]'].max()
    # diff = round(pr_Max - ex_Max,2)
    # plt.plot(ex_nd['Relative Time [hrs]'], ex_nd['Stage [ft]'], label= 'Existing')
    # plt.plot(pr_nd['Relative Time [hrs]'], pr_nd['Stage [ft]'], label= 'Proposed')# Customize the plot (add labels, title, legend, etc.)
    # plt.xlabel('Time')
    # plt.ylabel('Stage')
    # plt.title(f'Hydrograph for Node {nd}')
    # plt.legend()
    # plt.grid(True)
    
    # Streamlit outputs
    # st.write(ex_nd.shape)
    # st.write(ex_nd.head())
    # st.pyplot(plt)
    # st.metric(label=metric_tit, value= f'{pr_Max} ft', delta= diff, delta_color= "inverse")
    
if __name__=="__main__":
    main()

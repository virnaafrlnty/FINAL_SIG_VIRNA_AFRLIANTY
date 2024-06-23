import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# # mengubah file shp ke dalam geojson
# gdf = gpd.read_file('Banggae\KecamatanBanggae.shp')
# gdf.to_file('KecBanggae.geojson', driver='GeoJSON')
    
    

# memberikan warna berdasarkan jumlah penduduk
def color_function(feature):
    nama_desa = feature['properties']['DESA']
    

    # berdasarkan yang di ambil dari file .geoJson
    if nama_desa == "BAURUNG":
        return '#E6E6'  
    elif nama_desa == "BARUGA DHUA":    
        return '#D8BFD8' 
    elif nama_desa == "TANDE":
        return '#B0C4DE'  
    elif nama_desa == "BARUGA":
        return '#87CEEB'  
    elif nama_desa == "LABUANG":
        return '#6495ED'  
    elif nama_desa == "LEMBANG":
        return '#4169E1'  
    elif nama_desa == "LABUANG UTARA":
        return '#f1c40f'
    elif nama_desa == "TANDE TIMUR":
        return '#e74c3c'
    elif nama_desa == "BUTTU BARUGA":
        return '#8e44ad'
    
    else:
        return '#191970'  
    
def create_map():
    # mengambil file geosjon
    gdf = gpd.read_file('KecBanggae.geojson')

    # mendapatkan koordinat tengah untuk pemetaan
    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    
    # membuat peta folium
    m = folium.Map(location=center, zoom_start=13)
    
    # menambahkan layer GeoJSON 
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': color_function(feature),
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["DESA"],
            aliases=["Nama Desa : "],
            localize=True
        ),
    ).add_to(m)
    
    # menampilkan label berdasarkan desa
    for _, row in gdf.iterrows():
        folium.Marker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            popup=row['DESA'],
            icon=folium.DivIcon(
                html=f"""<div style="font-weight:bold; font-size:10px;">{row['DESA']}</div>""",
                icon_size=(150, 36),
                icon_anchor=(75, 18)
            )
        ).add_to(m)
    



    folium.GeoJson(gdf).add_to(m)
    return m

st.title("Peta Kecamatan Banggae, Kabupaten Majene, Provinsi Sulawesi Barat\nPenerapan peta pada streamlit")
map = create_map()
st_folium(map, width=700, height=500)

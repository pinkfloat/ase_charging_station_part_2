import pandas as pd
import geopandas as gpd


# Load geospatial data for Berlin postal codes
df_geodat_plz = pd.read_csv("../data/geodata_berlin_plz.csv", delimiter=";")

# Load electric charging station data from an Excel file
df_lstat = pd.read_excel("../data/Ladesaeulenregister_SEP.xlsx")


def sort_by_plz_add_geometry(dfr, dfg): 
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    sorted_df               = dframe\
        .sort_values(by='PLZ')\
        .reset_index(drop=True)\
        .sort_index()
        
    sorted_df2              = sorted_df.merge(df_geo, on='PLZ', how ='left')
    sorted_df3              = sorted_df2.dropna(subset=['geometry'])
    
    sorted_df3.loc[:, 'geometry'] = gpd.GeoSeries.from_wkt(sorted_df3['geometry'])
    
    ret = gpd.GeoDataFrame(sorted_df3, geometry='geometry')
    
    return ret


def preprocess_lstat(dfr, dfg):
    """Preprocessing dataframe from Ladesaeulenregister_SEP.xlsx"""
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    dframe2               	= dframe.loc[:,['Betreiber','Anzeigename (Karte)','Postleitzahl', 'Bundesland', 'Breitengrad', 'Längengrad', 'Nennleistung Ladeeinrichtung [kW]']]
    dframe2.rename(columns  = {'Betreiber':'stationOperator','Anzeigename (Karte)':'stationName',"Nennleistung Ladeeinrichtung [kW]":"KW", "Postleitzahl": "PLZ",  'Breitengrad':'Latitude', 'Längengrad':'Longitude', }, inplace = True)

    # Convert to string
    dframe2['Latitude']  = dframe2['Latitude'].astype(str)
    dframe2['Longitude']   = dframe2['Longitude'].astype(str)
    dframe2['stationOperator']   = dframe2['stationOperator'].astype(str)
    dframe2['stationName']   = dframe2['stationName'].astype(str)


    # Now replace the commas with periods
    dframe2['Latitude']  = dframe2['Latitude'].str.replace(',', '.')
    dframe2['Longitude']   = dframe2['Longitude'].str.replace(',', '.')

    dframe3                 = dframe2[(dframe2["Bundesland"] == 'Berlin') & 
                                            (dframe2["PLZ"] > 10115) &  
                                            (dframe2["PLZ"] < 14200)]
    
    ret = sort_by_plz_add_geometry(dframe3, df_geo)

    # Add an ID column with row numbers starting from 1
    ret['stationID'] = range(1, len(ret) + 1)
    
    return ret


df = preprocess_lstat(df_lstat, df_geodat_plz)

df.to_csv("../data/ChargingStationData.csv", index=False)
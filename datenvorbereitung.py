import pandas as pd
import numpy as np
import json

df = pd.read_csv("https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv")
#Origin Delay CSV
dfOriginAirportsDelay =df[["ORIGIN_AIRPORT","ORIGIN_AIRPORT_POS","DEPARTURE_DELAY"]]
dfOriginAirportsDelay["hour"]=df["SCHEDULED_DEPARTURE"].str[11:13]
dfOriginAirportsDelayDay = dfOriginAirportsDelay.groupby(["ORIGIN_AIRPORT"])
dfOriginAirportsDelay = dfOriginAirportsDelay.groupby(["ORIGIN_AIRPORT","hour"])
dfOrigDelaySummary = pd.DataFrame()
for a in dfOriginAirportsDelayDay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["ORIGIN_AIRPORT"].iloc[0],"Hour":"-1","AIRPORT_POS":a[1]["ORIGIN_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DEPARTURE_DELAY"].mean(),"LowDelay":a[1]["DEPARTURE_DELAY"].min(),"HighDelay":a[1]["DEPARTURE_DELAY"].max(),"Count":len(a[1].index)/24}, ignore_index = True)
 
for a in dfOriginAirportsDelay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["ORIGIN_AIRPORT"].iloc[0],"Hour": a[1]["hour"].iloc[0],"AIRPORT_POS":a[1]["ORIGIN_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DEPARTURE_DELAY"].mean(),"LowDelay":a[1]["DEPARTURE_DELAY"].min(),"HighDelay":a[1]["DEPARTURE_DELAY"].max(),"Count":len(a[1].index)}, ignore_index = True)
    
 
dfOrigDelaySummary = dfOrigDelaySummary.sort_values(by="Hour") 
dfOrigDelaySummary.to_csv("OrigDelaySummary.csv")


#Destination Delay CSV
dfDestinationAirportsDelay =df[["DESTINATION_AIRPORT","DESTINATION_AIRPORT_POS","DESTINATION_DELAY"]]
dfDestinationAirportsDelay["hour"]=df["SCHEDULED_DESTINATION"].str[11:13]
dfDestinationAirportsDelayDay = dfDestinationAirportsDelay.groupby(["DESTINATION_AIRPORT"])
dfDestinationAirportsDelay = dfDestinationAirportsDelay.groupby(["DESTINATION_AIRPORT","hour"])

dfOrigDelaySummary = pd.DataFrame()
for a in dfDestinationAirportsDelayDay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour":"-1","AIRPORT_POS":a[1]["DESTINATION_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DESTINATION_DELAY"].mean(),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":len(a[1].index)/(24)}, ignore_index = True)
 
for a in dfDestinationAirportsDelay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour": a[1]["hour"].iloc[0],"AIRPORT_POS":a[1]["DESTINATION_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DESTINATION_DELAY"].mean(),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":len(a[1].index)}, ignore_index = True)
    
 
dfOrigDelaySummary = dfOrigDelaySummary.sort_values(by="Hour") 
dfOrigDelaySummary.to_csv("DestDelaySummary.csv")



#Dataset for names of Airlines 
Airlines = df["AIRLINE"].unique()
df2 = pd.read_csv("https://storage.googleapis.com/kagglesdsdata/datasets/2253/3806/airlines.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230330%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230330T155223Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=4be41636bdf5d8521c92338a74b2ab6e5dd72616f36831f5da23c6b89d6f09dc4f1e5e20df5f2d83b02a4c84f93fd848251ff28c98927a1a0c48ea881af7885cf091d26e71847c383544a98217cc5cdb99300c08dd907642eea3fd848709a03dbac1ad62cea9a233c944f39f4345d448274ef20b2a8160dfc9efcd3c95332e9ae857e8aeb63fc4dd89692faa4acac30c11664bef607f8313f06dd97ca0cc7a5d2f8f0fe9d374d10c4ce585be5a3caf2272fd0eb2de51b3e342b95e598a67f810cbd9f6e02b3aa5dc2bd322db3418d5ad5f2b112c231d4ac766f23fe2b321eeca76c27fcfbcbb101603e49ed150abda503d15523e30ab5c39f5e919357c328d65")
df2= df2[["Name","IATA"]]
df2 = df2[df2["IATA"].isin(Airlines)].sort_values(by="IATA")
dfOrigDelaySummary.to_csv("Airlines.csv")

print(df["DESTINATION_DELAY"].min())
print(df["DEPARTURE_DELAY"].min())

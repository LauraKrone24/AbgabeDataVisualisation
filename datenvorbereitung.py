import pandas as pd
import numpy as np
import json

df = pd.read_csv("https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv")

dfOriginAirportsDelay =df[["ORIGIN_AIRPORT","ORIGIN_AIRPORT_POS","DEPARTURE_DELAY"]]
dfOriginAirportsDelay["hour"]=df["SCHEDULED_DEPARTURE"].str[11:13]
dfOriginAirportsDelay["DEPARTURE_DELAY"] = dfOriginAirportsDelay["DEPARTURE_DELAY"].astype("int32")
dfOriginAirportsDelay = dfOriginAirportsDelay.groupby(["ORIGIN_AIRPORT","hour"])

dfOrigDelaySummary = pd.DataFrame()
for a in dfOriginAirportsDelay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["ORIGIN_AIRPORT"].iloc[0],"Hour": a[1]["hour"].iloc[0],"ORIGIN_AIRPORT_POS":a[1]["ORIGIN_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DEPARTURE_DELAY"].mean(),"Count":len(a[1].index)}, ignore_index = True)
    
 
dfOrigDelaySummary = dfOrigDelaySummary.sort_values(by="Hour") 
dfOrigDelaySummary.to_csv("OrigDelaySummary.csv")
#print(dfOrigDelaySummary)

"""
f = open("dfOriginAirportsDelay.json", "w")
f.write(dfOriginAirportsDelay)
f.close()

dfDestinationAirportsDelay =df[["DESTINATION_AIRPORT","SCHEDULED_DESTINATION","DESTINATION_AIRPORT_POS","DESTINATION_DELAY"]]
dfDestinationAirportsDelay["hour"]=dfDestinationAirportsDelay["SCHEDULED_DESTINATION"].str[11:13]
dfDestinationAirportsDelay = dfDestinationAirportsDelay.groupby(["DESTINATION_AIRPORT","hour"]).apply(lambda x: x.to_json(orient='records')).to_json()

f = open("dfDestinationAirportsDelay.json", "w")
f.write(dfDestinationAirportsDelay)
f.close()
"""
#print(dfDestinationAirportsDelay)
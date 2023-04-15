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

dfDestDelaySummary = pd.DataFrame()
for a in dfDestinationAirportsDelayDay:
    dfDestDelaySummary= dfDestDelaySummary.append({"Airport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour":"-1","AIRPORT_POS":a[1]["DESTINATION_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DESTINATION_DELAY"].mean(),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":len(a[1].index)/(24)}, ignore_index = True)
 
for a in dfDestinationAirportsDelay:
    dfDestDelaySummary= dfDestDelaySummary.append({"Airport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour": a[1]["hour"].iloc[0],"AIRPORT_POS":a[1]["DESTINATION_AIRPORT_POS"].iloc[0],"AvgDelay":a[1]["DESTINATION_DELAY"].mean(),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":len(a[1].index)}, ignore_index = True)
    
 
dfDestDelaySummary = dfDestDelaySummary.sort_values(by="Hour") 
dfDestDelaySummary.to_csv("DestDelaySummary.csv")



#Dataset for names of Airlines 
Airlines = df["AIRLINE"].unique()
df2 = pd.read_csv("OrgAirlineData.csv")
df2= df2[["Name","IATA"]]
df2 = df2[df2["IATA"].isin(Airlines)].sort_values(by="IATA")

df["AirTimeDiff"]  = df["ELAPSED_TIME"]-df["SCHEDULED_TIME"]
dfAirlineGrouped = df.groupby("AIRLINE")
dfAirlineSummary = pd.DataFrame()

for a in dfAirlineGrouped: 
    dfAirlineSummary= dfAirlineSummary.append({"IATA":a[1]["AIRLINE"].iloc[0],"AvgOrgDelay":round(a[1]["DEPARTURE_DELAY"].mean(),2),"MaxOrgDelay":a[1]["DEPARTURE_DELAY"].max(),"MinOrgDelay":a[1]["DEPARTURE_DELAY"].min(),"AvgDestDelay":round(a[1]["DESTINATION_DELAY"].mean(),2),"MaxDestDelay":a[1]["DESTINATION_DELAY"].max(),"MinDestDelay":a[1]["DESTINATION_DELAY"].min(),"AvgAirTimeDiff":round(a[1]["AirTimeDiff"].mean(),2),"MaxAirTimeDiff":a[1]["AirTimeDiff"].max(),"MinAirTimeDiff":a[1]["AirTimeDiff"].min(),"Count":len(a[1].index)},ignore_index = True)



result = pd.merge(df2, dfAirlineSummary, how="outer",on="IATA")
result= result.append({"Name":" All Airlines","IATA":"all","AvgOrgDelay":round(df["DEPARTURE_DELAY"].mean(),2),"MaxOrgDelay":df["DEPARTURE_DELAY"].max(),"MinOrgDelay":df["DEPARTURE_DELAY"].min(),"AvgDestDelay":round(df["DESTINATION_DELAY"].mean(),2),"MaxDestDelay":df["DESTINATION_DELAY"].max(),"MinDestDelay":df["DESTINATION_DELAY"].min(),"AvgAirTimeDiff":round(df["AirTimeDiff"].mean(),2),"MaxAirTimeDiff":df["AirTimeDiff"].max(),"MinAirTimeDiff":df["AirTimeDiff"].min(),"Count":len(df.index)},ignore_index = True)

df2 = result.sort_values(by="Name")
df2.to_csv("Airlines.csv")

df3 = pd.read_csv("airports.csv")
df3 = df3[["IATA","STATE"]]
df3
df = pd.merge(df, df3, left_on='ORIGIN_AIRPORT', right_on='IATA')
df.drop('IATA', axis=1, inplace=True)
df.rename(columns={"STATE": "OrgState"}, inplace=True)
df = pd.merge(df, df3, left_on='DESTINATION_AIRPORT', right_on='IATA')
df.drop('IATA', axis=1, inplace=True)
df.rename(columns={"STATE": "DestState"}, inplace=True)
print(df)

#Connections by State 

dfConnections = df.groupby(["OrgState","DestState"])



dfConnectionsummary ={}
for a in dfConnections: 
    org = a[0][0]
    dest = a[0][1]
    
    dfConnectionsummary[org+","+dest] = {"count":len(a[1].index),"OrgDelay":round(a[1]["DEPARTURE_DELAY"].mean(),2),"DestDelay":round(a[1]["DESTINATION_DELAY"].mean(),2)}

print(dfConnectionsummary)
States = df["OrgState"].dropna().astype("str").append(df["DestState"].dropna()).astype("str").unique()
States = np.sort(States)

csvString = ""
for org in States:
    csvString+=org+";"

csvString.strip(";")
csvString+="\n"

for org in States:
    
    for dest in States: 
        if(org+","+dest in dfConnectionsummary):
            csvString+= str(dfConnectionsummary[org+","+dest])+";"
        else:
            csvString+= "{'count':0,'OrgDelay':0,'DestDelay':0};"
    csvString.strip(";")
    csvString+="\n"


csvString = csvString.replace("\'","\"")
f = open("Connections.csv", "w")
f.write(csvString)
f.close()


        
 



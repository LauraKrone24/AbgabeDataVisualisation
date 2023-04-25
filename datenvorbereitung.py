import pandas as pd
import numpy as np
import json

df = pd.read_csv("https://raw.githubusercontent.com/LauraKrone24/AbgabeDataVisualisation/master/AllFlightsJanuary.csv")
#Origin Delay CSV
dfOriginAirportsDelay =df[["ORIGIN_AIRPORT","ORIGIN_AIRPORT_POS","DEPARTURE_DELAY"]]
dfOriginAirportsDelay["hour"]=df["SCHEDULED_DEPARTURE"]%60
dfOriginAirportsDelayDay = dfOriginAirportsDelay.groupby(["ORIGIN_AIRPORT"])
dfOriginAirportsDelay = dfOriginAirportsDelay.groupby(["ORIGIN_AIRPORT","hour"])
dfOrigDelaySummary = pd.DataFrame()
for a in dfOriginAirportsDelayDay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["ORIGIN_AIRPORT"].iloc[0],"Hour":"-1","AIRPORT_POS":a[1]["ORIGIN_AIRPORT_POS"].iloc[0],"AvgDelay":round(a[1]["DEPARTURE_DELAY"].mean(),2),"LowDelay":a[1]["DEPARTURE_DELAY"].min(),"HighDelay":a[1]["DEPARTURE_DELAY"].max(),"Count":round(len(a[1].index)/24/31,2)}, ignore_index = True)
 
for a in dfOriginAirportsDelay:
    dfOrigDelaySummary= dfOrigDelaySummary.append({"Airport":a[1]["ORIGIN_AIRPORT"].iloc[0],"Hour": a[1]["hour"].iloc[0],"AIRPORT_POS":a[1]["ORIGIN_AIRPORT_POS"].iloc[0],"AvgDelay":round(a[1]["DEPARTURE_DELAY"].mean(),2),"LowDelay":a[1]["DEPARTURE_DELAY"].min(),"HighDelay":a[1]["DEPARTURE_DELAY"].max(),"Count":round(len(a[1].index)/31,2)}, ignore_index = True)
    
 
dfOrigDelaySummary = dfOrigDelaySummary.sort_values(by=["Hour","Count"],ascending=[True, False]) 
dfOrigDelaySummary.to_csv("OrigDelaySummary.csv")


#Destination Delay CSV
dfDestinationAirportsDelay =df[["DESTINATION_AIRPORT","DESTINATION_AIRPORT_POS","DESTINATION_DELAY"]]
dfDestinationAirportsDelay["hour"]=df["SCHEDULED_DESTINATION"]%60
dfDestinationAirportsDelayDay = dfDestinationAirportsDelay.groupby(["DESTINATION_AIRPORT"])
dfDestinationAirportsDelay = dfDestinationAirportsDelay.groupby(["DESTINATION_AIRPORT","hour"])

dfDestDelaySummary = pd.DataFrame()
for a in dfDestinationAirportsDelayDay:
    dfDestDelaySummary= dfDestDelaySummary.append({"Airport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour":"-1","AIRPORT_POS":a[1]["DESTINATION_AIRPORT_POS"].iloc[0],"AvgDelay":round(a[1]["DESTINATION_DELAY"].mean(),2),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":round(len(a[1].index)/(24)/31,2)}, ignore_index = True)
 
for a in dfDestinationAirportsDelay:
    dfDestDelaySummary= dfDestDelaySummary.append({"Airport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour": a[1]["hour"].iloc[0],"AIRPORT_POS":a[1]["DESTINATION_AIRPORT_POS"].iloc[0],"AvgDelay":round(a[1]["DESTINATION_DELAY"].mean(),2),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":round(len(a[1].index)/31,2)}, ignore_index = True)
    
 
dfDestDelaySummary = dfDestDelaySummary.sort_values(by=["Hour","Count"],ascending=[True, False]) 
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
    dfAirlineSummary= dfAirlineSummary.append({"IATA":a[1]["AIRLINE"].iloc[0],"OrgDelayMax":a[1]["DEPARTURE_DELAY"].max(),"OrgDelayMin":a[1]["DEPARTURE_DELAY"].min(),"OrgDelayQ2":round(a[1]["DEPARTURE_DELAY"].quantile(.5),2),"OrgDelayQ3":round(a[1]["DEPARTURE_DELAY"].quantile(.75),2),"OrgDelayQ1":round(a[1]["DEPARTURE_DELAY"].quantile(.25),2),"DestDelayMax":a[1]["DESTINATION_DELAY"].max(),"DestDelayMin":a[1]["DESTINATION_DELAY"].min(),"DestDelayQ2":round(a[1]["DESTINATION_DELAY"].quantile(.5),2),"DestDelayQ3":round(a[1]["DESTINATION_DELAY"].quantile(.75),2),"DestDelayQ1":round(a[1]["DESTINATION_DELAY"].quantile(.25),2),"AirTimeDiffMax":a[1]["AirTimeDiff"].max(),"AirTimeDiffMin":a[1]["AirTimeDiff"].min(),"AirTimeDiffQ2":round(a[1]["AirTimeDiff"].quantile(.5),2),"AirTimeDiffQ3":round(a[1]["AirTimeDiff"].quantile(.75),2),"AirTimeDiffQ1":round(a[1]["AirTimeDiff"].quantile(.25),2),"Count":len(a[1].index)},ignore_index = True)



result = pd.merge(df2, dfAirlineSummary, how="outer",on="IATA")
result= result.append({"Name":" All Airlines","IATA":"all","OrgDelayMax":df["DEPARTURE_DELAY"].max(),"OrgDelayMin":df["DEPARTURE_DELAY"].min(),"OrgDelayQ2":round(df["DEPARTURE_DELAY"].quantile(.5),2),"OrgDelayQ3":round(df["DEPARTURE_DELAY"].quantile(.75),2),"OrgDelayQ1":round(df["DEPARTURE_DELAY"].quantile(.25),2),"DestDelayMax":df["DESTINATION_DELAY"].max(),"DestDelayMin":df["DESTINATION_DELAY"].min(),"DestDelayQ2":round(df["DESTINATION_DELAY"].quantile(.5),2),"DestDelayQ3":round(df["DESTINATION_DELAY"].quantile(.75),2),"DestDelayQ1":round(df["DESTINATION_DELAY"].quantile(.25),2),"AirTimeDiffMax":df["AirTimeDiff"].max(),"AirTimeDiffMin":df["AirTimeDiff"].min(),"AirTimeDiffQ2":round(df["AirTimeDiff"].quantile(.5),2),"AirTimeDiffQ3":round(df["AirTimeDiff"].quantile(.75),2),"AirTimeDiffQ1":round(df["AirTimeDiff"].quantile(.25),2),"Count":len(df.index)},ignore_index = True)

df2 = result.sort_values(by="Name")
df2.to_csv("Airlines.csv")

df3 = pd.read_csv("airports.csv")
df4 = df3


df3 = df3[["IATA","STATE"]]

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


#Airline Delay 

dfAirlineDelay =df[["AIRLINE","DEPARTURE_DELAY","DESTINATION_DELAY"]]
dfAirlineDelay["DestHour"]=df["SCHEDULED_DESTINATION"]%60
dfAirlineDelay["OrgHour"]=df["SCHEDULED_DEPARTURE"]%60
dfAirlineDelayDay = dfAirlineDelay.groupby(["AIRLINE"])
dfAirlineDelayOrg = dfAirlineDelay.groupby(["AIRLINE","OrgHour"])
dfAirlineDelayDest = dfAirlineDelay.groupby(["AIRLINE","DestHour"])

dfAirlineDelaySummaryOrg = pd.DataFrame()
dfAirlineDelaySummaryDest = pd.DataFrame()
for a in dfAirlineDelayDay:
    dfAirlineDelaySummaryOrg= dfAirlineDelaySummaryOrg.append({"Airline":a[1]["AIRLINE"].iloc[0],"Hour":-1,"AvgDelay":  round(a[1]["DEPARTURE_DELAY"].mean(),2),"LowDelay":a[1]["DEPARTURE_DELAY"].min(),"HighDelay":a[1]["DEPARTURE_DELAY"].max(),"Count":round(len(a[1].index)/24/31,2)}, ignore_index = True)
    dfAirlineDelaySummaryDest= dfAirlineDelaySummaryDest.append({"Airline":a[1]["AIRLINE"].iloc[0],"Hour":-1,"AvgDelay":round(a[1]["DESTINATION_DELAY"].mean(),2),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":round(len(a[1].index)/24/31,2)}, ignore_index = True)
 
for a in dfAirlineDelayOrg:
    dfAirlineDelaySummaryOrg= dfAirlineDelaySummaryOrg.append({"Airline":a[1]["AIRLINE"].iloc[0],"Hour": a[1]["OrgHour"].iloc[0],"AvgDelay":round(a[1]["DEPARTURE_DELAY"].mean(),2),"LowDelay":a[1]["DEPARTURE_DELAY"].min(),"HighDelay":a[1]["DEPARTURE_DELAY"].max(),"Count":round(len(a[1].index)/31,2)}, ignore_index = True)
for a in dfAirlineDelayDest:
    dfAirlineDelaySummaryDest= dfAirlineDelaySummaryDest.append({"Airline":a[1]["AIRLINE"].iloc[0],"Hour": a[1]["DestHour"].iloc[0],"AvgDelay":round(a[1]["DESTINATION_DELAY"].mean(),2),"LowDelay":a[1]["DESTINATION_DELAY"].min(),"HighDelay":a[1]["DESTINATION_DELAY"].max(),"Count":round(len(a[1].index)/31,2)}, ignore_index = True)
    
 
dfAirlineDelaySummaryOrg = dfAirlineDelaySummaryOrg.sort_values(by="Hour") 
dfAirlineDelaySummaryOrg.to_csv("AirlineOrgDelaySummary.csv")

dfAirlineDelaySummaryDest = dfAirlineDelaySummaryDest.sort_values(by="Hour") 
dfAirlineDelaySummaryDest.to_csv("AirlineDestDelaySummary.csv")
        
#Datenvorbereitung für Vis 5 - Best Connection 
dfBestConnect = df
dfBestConnect["hour"]=df["SCHEDULED_DEPARTURE"]%60
dfBestConnectDay = dfBestConnect.groupby(["ORIGIN_AIRPORT","DESTINATION_AIRPORT","AIRLINE"])
dfBestConnect = dfBestConnect.groupby(["ORIGIN_AIRPORT","DESTINATION_AIRPORT","hour","AIRLINE"])

dfBestConnectSummary = pd.DataFrame()
for a in dfBestConnectDay: 
    dfBestConnectSummary = dfBestConnectSummary.append({"OrgAirport":a[1]["ORIGIN_AIRPORT"].iloc[0],"DestAirport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour":-1,"Airline":a[1]["AIRLINE"].iloc[0],"MinDelayDest":a[1]["DESTINATION_DELAY"].min(),"AvgDelayDest":a[1]["DESTINATION_DELAY"].mean(),"MaxDelayDest":a[1]["DESTINATION_DELAY"].max(),"MinDelayOrg":a[1]["DEPARTURE_DELAY"].min(),"AvgDelayOrg":a[1]["DEPARTURE_DELAY"].mean(),"MaxDelayOrg":a[1]["DEPARTURE_DELAY"].max(),"Count":len(a[1].index)},ignore_index = True)


for a in dfBestConnect: 
    dfBestConnectSummary = dfBestConnectSummary.append({"OrgAirport":a[1]["ORIGIN_AIRPORT"].iloc[0],"DestAirport":a[1]["DESTINATION_AIRPORT"].iloc[0],"Hour":a[1]["hour"].iloc[0],"Airline":a[1]["AIRLINE"].iloc[0],"MinDelayDest":a[1]["DESTINATION_DELAY"].min(),"AvgDelayDest":a[1]["DESTINATION_DELAY"].mean(),"MaxDelayDest":a[1]["DESTINATION_DELAY"].max(),"MinDelayOrg":a[1]["DEPARTURE_DELAY"].min(),"AvgDelayOrg":a[1]["DEPARTURE_DELAY"].mean(),"MaxDelayOrg":a[1]["DEPARTURE_DELAY"].max(),"Count":len(a[1].index)},ignore_index = True)

dfBestConnectSummary = dfBestConnectSummary.sort_values(by=["OrgAirport","DestAirport","Hour"])
dfBestConnectSummary.to_csv("BestConnectSummary.csv")



# hier noch filter ob Airport überhaupt in Best Connection Summaray
#df4.to_csv("SortedAirports.csv")

import pandas as pd
import numpy as np
import json

df = pd.read_csv("/Users/laura/Desktop/AllCleanedFlights.csv")
df = df[df["MONTH"]==1]

df.to_csv("AllFlightsJanuary.csv")

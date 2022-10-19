import time
start = time.time()
import requests
import csv
import pandas as pd
import json
from datetime import datetime
#from geopy.geocoders import Nominatim
#import pymongo


today = datetime.today()
link = "https://www.eraktkosh.in/BLDAHIMS/bloodbank/nearbyBB.cnt?hmode=GETNEARBYSTOCKDETAILS&stateCode=-1&districtCode=-1&bloodGroup=all&bloodComponent=11&lang=0&_=1662049401609"
f = requests.get(link)
myfile = f.text
a = json.loads(myfile)
b=a.get('data')
header=['number','name','a','b','c','d']
with open('C:/Users/DRK1999/dv_2sem/games.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(b)
df=pd.read_csv("C:/Users/DRK1999/dv_2sem/games.csv",encoding='ISO-8859-1')

index_names = df[ df['b'] == "<p class='text-danger'><b>Whole Blood</b>Not Available Search for another Component" ].index
df.drop(index_names, inplace = True)
index_names = df[ df['b'] == "<p class='text-danger'><b>Stock</b>Not Available Search for another Component" ].index
df.drop(index_names, inplace = True)
df = df.replace('<br/>',',', regex=True)
g=["<p class='text-success'>","</p>"]
df = df.replace(g,'', regex=True)
df=df.replace("<img src='../hisglobal/bbpublic/images/transparent/live_stock.png'>",today.strftime("%Y-%m-%d %H:%M:%S"),regex=True)
df['email']=df['name'].str.split(",").str[-1].str.split(":").str[1]
df['name']=df['name'].str.split(",").str[:-2]
df['name'] = [','.join(map(str, l)) for l in df['name']]
df = df.reset_index()
df['ph']=df['name'].str.split(":").str[-1]
df['name']=df['name'].str.split(":").str[:-1]
df['name'] = [','.join(map(str, l)) for l in df['name']]
df['name']=df['name'].str.split(",").str[:-1]
df['name'] = [','.join(map(str, l)) for l in df['name']]
df['state']=df['name'].str.split(",").str[-1]
df['district']=df['name'].str.split(",").str[-2]
'''geolocator = Nominatim(user_agent="myApp")

df[['location_lat', 'location_long']] = df['name'].apply(geolocator.geocode).apply(lambda x: pd.Series([x.latitude, x.longitude], index=['location_lat', 'location_long']))'''

df['b']=df['b'].str.split(',').str[1:]
#df['b']=[','.join(map(str, l)) for l in df['b']]
#df['b']=df['b'].str.split(':')
#df['b']=[','.join(map(str, l)) for l in df['b']]
df['A+Ve']=0
df['A-Ve']=0
df['B+Ve']=0
df['B-Ve']=0
df['O+Ve']=0
df['O-Ve']=0
df['AB+Ve']=0
df['AB-Ve']=0

df.drop(df.columns[[0,3,6]], axis=1, inplace=True)
df['number']=df.index
df = df[['number','name','state','district','ph','email','b','A+Ve','A-Ve','B+Ve','B-Ve','O+Ve','O-Ve','AB+Ve','AB-Ve','c']]



df['b']=df['b'].to_list()
for index in df.index:
    for i in df['b'][index]:
        b=i.split(":")[0].strip()
        c1=int(i.split(":")[1])
        '''if(b==" A+Ve"):
            df.loc[index,'A+Ve']=c1
        elif(b==" A-Ve"):
            df.loc[index,'A-Ve']=c1
        elif(b==" B+Ve"):
            df.loc[index,'B+Ve']=c1
        elif(b==" B-Ve"):
            df.loc[index,'B-Ve']=c1
        elif(b==" O+Ve"):
            df.loc[index,'O+Ve']=c1
        elif(b==" O-Ve"):
            df.loc[index,'O-Ve']=c1
        elif(b==" AB+Ve"):
            df.loc[index,'AB+Ve']=c1
        elif(b==" AB-Ve"):
            df.loc[index,'AB-Ve']=c1'''
        
        df.loc[index,b]=c1

df.to_csv('C:/Users/DRK1999/dv_2sem/games.csv')

'''myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["LifeStream"]
mycol = mydb["blood_Stock"]

mycol.insert_many(df.to_dict('records'))'''

dff=pd.read_csv('C:/Users/DRK1999/dv_2sem/games1.csv')
out = (df.merge(dff, left_on='name', right_on='name1')
          .reindex(columns=['number','name','state','district','ph','email','b','A+Ve','A-Ve','B+Ve','B-Ve','O+Ve','O-Ve','AB+Ve','AB-Ve','c','lat','long']))
out.to_csv('C:/Users/DRK1999/dv_2sem/final.csv')
out.to_excel('C:/Users/DRK1999/dv_2sem/final.xlsx')

end = time.time()
print("The time of execution of above program is :", end-start)
print(out)

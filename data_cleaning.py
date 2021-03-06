# -*- coding: utf-8 -*-
"""Final_csv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13Pyk1f54C0dmCOseAuEQrf7rfOjy9oif
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

proposals = pd.read_excel("C:/Users/jon.bilbao/Music/TFM/IDOM_Proposals_20210608.xlsx")

#print(proposals.head())
data = proposals[["Proposal Status",'Technical Area Desc.','Functional Area Desc.','Geographic Area Desc.','Project Country','Price(€)','Margin','Pre-backlog generated?','Proposal Created on','Project Start Date',
                  'Project End Date','Project Type Desc.','Service Type Desc.','Product Type Desc.','Origin Proposal','New Customer','Company Desc.',
                  'Source of Funding','Confidential Proposal','Exchange Insurance Required','Bank Guarantee Method']]

data[['Proposal Status']] = data[['Proposal Status']].fillna(value='NO')
data=data.rename(columns={'Proposal Status': 'Status'})
data = data[data.Status.isin(['AW', 'NO'])]

data=data.rename(columns={'Project Start Date': 'Project_Start_Date'})
data=data.rename(columns={'Project End Date': 'Project_End_Date'})
data["Project_Duration"] = (data.Project_End_Date - data.Project_Start_Date)
data=pd.get_dummies(data, columns=['Pre-backlog generated?'])
data=data.rename(columns={'Pre-backlog generated?_Does not apply – Framework Contract': 'Framework Contract'})
data=data.rename(columns={'Pre-backlog generated?_Does not apply – Offer with an existing project': 'Offer with an existing project'})
data=data.rename(columns={'Pre-backlog generated?_SI': 'Pre-backlog generated'})
data=data.drop(columns=['Pre-backlog generated?_NO'])
data=pd.get_dummies(data, columns=['Status'])
data=data.rename(columns={'Status_AW': 'Awarded'})
data=data.drop(columns=['Status_NO'])
data=data.rename(columns={'Proposal Code': 'Proposal_Code'})

#"""**Technical Area**"""
data=data.rename(columns={'Technical Area Desc.': 'Technical_Area_Desc'})

#"""**Functional Area (Business Line)**"""
data=data.rename(columns={'Functional Area Desc.': 'Functional_Area_Desc'})

#"""**Geographic Area**"""
data=data.rename(columns={'Geographic Area Desc.': 'Geographic_Area_Desc'})

#"""**Project Country**"""
data=data.rename(columns={'Project Country': 'Project_Country'})

#"""**Price**"""
data=data.rename(columns={'Price(€)': 'Price_euros'})

#"""Removing outliers"""
left = pd.DataFrame(data.groupby('Technical_Area_Desc').Price_euros.quantile(0.02))
right = pd.DataFrame(data.groupby('Technical_Area_Desc').Price_euros.quantile(0.90))

left.columns = ['left']
right.columns = ['right']

df = data.merge(left, left_on='Technical_Area_Desc', right_index=True)
df = df.merge(right, left_on='Technical_Area_Desc', right_index=True)

df = df[(df['Price_euros'] > df['left']) & (df['Price_euros'] < df['right'])]
df = df.drop(['left', 'right'], axis=1)

data=df

#"""Clustering"""

features = df[df.columns[4:5]]

model = KMeans(n_clusters=4, init='k-means++', n_init=100, max_iter=1000)
km_clusters = model.fit_predict(features)

features=features.to_numpy()
features= features.reshape(-1)

data['Price_cluster'] = km_clusters.tolist()
data['Price_cluster'] = data['Price_cluster'].apply(str)

#"""**Margin**
#Filtro y quito los que tienen Margin muy alto. ¿A partir de cuanto debería quitarlos?
data = data[(data['Margin'] < 95) & (data['Margin'] > 0)]

#"""Hacer rangos"""
data['margin_range']=pd.cut(data['Margin'], bins=3)

#"""**Proposal created on**"""
data=data.rename(columns={'Proposal Created on': 'Proposal_Created_On'})
data['Proposal_Created_On'].isnull().sum()
data["Proposal_Created_On"] = pd.to_datetime(data.Proposal_Created_On, format='%b', errors='coerce').dt.month

#"""**Pre-backlog generated**"""
data=data.rename(columns={'Pre-backlog generated': 'Pre-backlog_generated'})

#"""**Project type**"""
data=data.rename(columns={'Project Type Desc.': 'Project_Type_Desc'})
data = data.dropna(axis=0, subset=['Project_Type_Desc'])

#"""**Service Type**"""
data=data.rename(columns={'Service Type Desc.': 'Service_Type_Desc'})

#"""**Product type**"""
data=data.rename(columns={'Product Type Desc.': 'Product_Type_Desc'})
data = data.dropna(axis=0, subset=['Product_Type_Desc'])

#"""**Origin proposal**"""
data=data.rename(columns={'Origin Proposal': 'Origin_Proposal'})

values = {'Origin_Proposal': 'Not known'}
data=data.fillna(value=values)

#"""**New Customer**"""
data=data.rename(columns={'New Customer': 'New_Customer'})

#"""**Company**"""
data=data.rename(columns={'Company Desc.': 'Company_Desc'})

#"""**Source of funding**"""
data=data.rename(columns={'Source of Funding': 'Source_of_funding'})
data = data.dropna(axis=0, subset=['Source_of_funding'])

#"""**Confidential proposal**"""
data=data.rename(columns={'Confidential Proposal': 'Confidential_proposal'})

#"""**Exchange insurance required**"""
data=data.rename(columns={'Exchange Insurance Required': 'Exchange_Insurance_Required'})

#"""**Bank guarantee method**"""
data=data.rename(columns={'Bank Guarantee Method': 'Bank_Guarantee_Method'})

#"""**Project duration**"""
data['Project_Duration']
data.Project_Duration = (data.Project_Duration / np.timedelta64(1,'D')).astype(int)


left = pd.DataFrame(data.groupby('Technical_Area_Desc').Project_Duration.quantile(0.0))
right = pd.DataFrame(data.groupby('Technical_Area_Desc').Project_Duration.quantile(0.98))

left.columns = ['left']
right.columns = ['right']

df = data.merge(left, left_on='Technical_Area_Desc', right_index=True)
df = df.merge(right, left_on='Technical_Area_Desc', right_index=True)

df = df[(df['Project_Duration'] > df['left']) & (df['Project_Duration'] < df['right'])]
df = df.drop(['left', 'right'], axis=1)


data=df



#"""Clusters"""
features = df[df.columns[19:20]]

model = KMeans(n_clusters=3, init='k-means++', n_init=100, max_iter=1000)
km_clusters = model.fit_predict(features)

features=features.to_numpy()
features= features.reshape(-1)

data['Duration_cluster'] = km_clusters.tolist()

data['Duration_cluster'] = data['Duration_cluster'].apply(str)

#"""**Framework contract**"""
data=data.rename(columns={'Framework Contract': 'Framework_Contract'})

#"""**Offer with an existing project**"""
data=data.rename(columns={'Offer with an existing project': 'Offer_with_existing_project'})

#"""..............................................................................."""
data=data.drop(columns=['Project_Start_Date','Project_End_Date'])
data[['Proposal_Created_On', 'margin_range']] = data[['Proposal_Created_On', 'margin_range']]. astype(str)

#"""Dummies"""
data=pd.get_dummies(data, columns=['Technical_Area_Desc'])
data=pd.get_dummies(data, columns=['Proposal_Created_On'])
data=pd.get_dummies(data, columns=['Project_Type_Desc'])
data=pd.get_dummies(data, columns=['Origin_Proposal'])
data=pd.get_dummies(data, columns=['Company_Desc'])
data=pd.get_dummies(data, columns=['Source_of_funding'])
data=pd.get_dummies(data, columns=['Price_cluster','margin_range','Duration_cluster'])
cols = data.columns.tolist()
cols1 = cols[15:16] + cols[16:60] + cols[12:15] + cols[7:11] + cols[3:5] + cols[11:12] + cols[60:70]
data1=data[cols1]
data1.to_csv('C:/Users/jon.bilbao/Music/TFM/data1.csv')

data=pd.get_dummies(data, columns=['Functional_Area_Desc','Geographic_Area_Desc','Project_Country', 'Service_Type_Desc', 'Product_Type_Desc'])
cols1 = data1.columns.tolist()
cols2=data.columns.tolist()
cols2=cols2[65:]
cols3=cols1+cols2
data2=data[cols3]
data2.head()
data2.to_csv('C:/Users/jon.bilbao/Music/TFM/fulldata.csv')

print("end")
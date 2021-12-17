import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

json_data = json.load(open('kode_negara_lengkap.json'))
raw = pd.read_csv('produksi_minyak_mentah.csv')

#country code dict
list_kode_negara = {}
for data in json_data:
    list_kode_negara.update({data['alpha-3']: data['name']})
    
def get_key(val):
    for key in list_kode_negara.keys():
        if list_kode_negara[key]==val:
            return key
        else: continue

#country list semua
list_not_in = []
for kode in raw['kode_negara']:
    if kode not in list_kode_negara.keys():
        list_not_in.append(kode)
list_not_in = list(set(list_not_in))

df = raw[~raw.kode_negara.isin(list_not_in)]

#country code conversion
def convert_kode_negara(kode):
    try:
        return list_kode_negara[kode]
    except:
        return kode

#country code list
list_kode = []
for i in json_data:
    if i['alpha-3'] not in list_kode:
        list_kode.append(i['alpha-3'])

st.title('Repository Data Produksi Minyak Dunia')
#problem 1
st.header('Production Historical Data by Country')
kode = st.text_input('kode negara', 'kode negara')

negara = convert_kode_negara(kode)

chart_data = df[df['kode_negara']==kode]
chart_data_x = chart_data['tahun']
chart_data_y = chart_data['produksi']
fig_1, ax1 = plt.subplots()
ax1.plot(chart_data_x, chart_data_y)
ax1.set_title(f'Produksi minyak {negara}')
st.pyplot(fig_1)

#problem 2
st.header('Produsen Minyak Terbesar pada Tahun Tertentu')
country_count = st.slider('Banyak negara teratas',1,142,10)
tahun = st.slider('year',1971,2015,2001)

list_negara_maks = df[df['tahun']==tahun].produksi.sort_values(ascending=False)[:country_count].values

fig2, ax2 = plt.subplots()


for data in list_negara_maks:
    #find kode, konversi ke nama negara
    code = df[(df['tahun']==tahun) & (df['produksi']==data)].kode_negara
    nama_negara = convert_kode_negara(code)
    ax2.barh(nama_negara, data)
ax2.set_title(f'{country_count} Negara produksi terbesar pada {tahun}')
st.pyplot(fig2)

#problem 3
st.header('Produsen Minyak Terbesar Kumulatif')
negara_cumm_pair = {}
negara_cumm_pair['Negara'] = []
negara_cumm_pair['Produksi Kumulatif'] = []

#membuat tabel produksi kumulatif
for kode in list_kode:
    negara = convert_kode_negara(kode)
    cumm = df[df['kode_negara']==kode].produksi.sum()
    negara_cumm_pair['Negara'].append(negara)
    negara_cumm_pair['Produksi Kumulatif'].append(cumm)
chart_data = pd.DataFrame(negara_cumm_pair).sort_values('Produksi Kumulatif', ascending=False)

#Membuat Chart
B = st.slider('banyak negara',1,142,15)
fig3, ax3 = plt.subplots()
data_filter = chart_data.head(B)
list_negara = data_filter['Negara'].to_list()
list_prod = data_filter['Produksi Kumulatif'].to_list()

for i in range(B):
    nama_negara = list_negara[i]
    prod = list_prod[i]
    ax3.barh(nama_negara,prod)
ax3.set_title(f'{B} Negara dengan produksi kumulatif terbesar')
st.pyplot(fig3)

#problem 4
st.header('Dimanakah produksi terbesar minyak berada?')
year = st.slider('Tahun',1971,2015,2001)

st.subheader(f'Produksi terbesar tahun {year}')
#Bagian produksi maksimal
#produksi maksimal by tahun
max_in_year = df[df['tahun']==year].sort_values('produksi', ascending=False).produksi.max()
kode_negara_max_year = df[(df['tahun']==year) & (df['produksi']==max_in_year)].kode_negara.values[0]
negara_max_year = convert_kode_negara(kode_negara_max_year)
kata_negara1 = negara_max_year.split()[0]
kata_negara2 = negara_max_year.split()[1]
region = 'test'
subregion = 'test1'
for data in json_data:
    if data['alpha-3'] == kode_negara_max_year:
        region = data['region']
        subregion = data['sub-region']
subregion1=subregion.split()[0]
subregion2=subregion.split()[1]

col1, col5, col2, col3, col4 = st.columns(5)
col1.metric(kata_negara1, kata_negara2)
col5.metric('Produksi', '(bbl)', delta=max_in_year)
col2.metric('Kode Negara', kode_negara_max_year)
col3.metric('Region', region)
col4.metric(subregion1, subregion2)

st.subheader('Negara dengan produksi kumulatif terbesar')          
#produksi maksimal kumulatif
#mendapatkan nilai terbesar
max_cumm = max(negara_cumm_pair['Produksi Kumulatif'])
#index nilai terbesar
index_max = 0
for i in negara_cumm_pair['Produksi Kumulatif']:
    if i == max_cumm:
        index_max = negara_cumm_pair['Produksi Kumulatif'].index(max_cumm)
negara_max_cumm = negara_cumm_pair['Negara'][index_max]
kode_negara2 = get_key(negara_max_cumm)
 
negara1 = negara_max_cumm.split()[0]
negara2 = negara_max_cumm.split()[1]

region2 = 'test'
subregion = 'test1'
for data in json_data:
    if data['alpha-3'] == kode_negara2:
        region2 = data['region']
        subregion = data['sub-region']
subregion1=subregion.split()[0]
subregion2=subregion.split()[1]
col21,col22,col23,col24,col25 = st.columns(5)
col21.metric(negara1,negara2)
col22.metric('Produksi', '(bbl)', delta=max_cumm)
col23.metric('Kode Negara', kode_negara2)
col24.metric('Region', region2)
col25.metric(subregion1, subregion2)

st.header('Dimanakah produksi terkecil minyak berada?')
#Bagian produksi minimal
#produksi minimal by tahun
st.subheader(f'Produksi terkecil tahun {year}')
min_in_year = df[df['tahun']==year].sort_values('produksi', ascending=False).produksi.min()
negara_min_year = convert_kode_negara(df[(df['tahun']==year) & (df['produksi']==min_in_year)].kode_negara.values[0])
kode_negara = get_key(negara_min_year)

col13, col53, col23, col33, col43 = st.columns(5)
negara1 = 'aa'
negara2 = 'bb'
negara_split = negara_min_year.split()
if len(negara_split)>1:
    negara1 = negara_split[0]
    negara2 = negara_split[1]
    col13.metric(negara1, negara2)
else:
    negara1 = negara_split[0]
    col13.metric('Negara', negara1)

col53.metric('Produksi', '(bbl)', delta=min_in_year)
col23.metric('Kode Negara', kode_negara)

region = 'test'
subregion = 'test1'
for data in json_data:
    if data['alpha-3'] == kode_negara:
        region = data['region']
        subregion = data['sub-region']
subregion1=subregion.split()[0]
subregion2=subregion.split()[1]
col33.metric('Region', region)


col43.metric(subregion1, subregion2)

#produksi minimal kumulatif
#mendapatkan nilai terkecil
st.subheader('Negara dengan produksi kumulatif terkecil')
min_cumm = min(negara_cumm_pair['Produksi Kumulatif'])
#index nilai terkecil
index_min = 0
for i in negara_cumm_pair['Produksi Kumulatif']:
    if i == min_cumm:
        index_min = negara_cumm_pair['Produksi Kumulatif'].index(min_cumm)
negara_min_cumm = negara_cumm_pair['Negara'][index_min]
kode_negara = get_key(negara_min_cumm)

col14, col54, col24, col34, col44 = st.columns(5)

negara_split=negara_min_cumm.split()
negara1 = 'aa'
negara2 = 'bb'
if len(negara_split)>1:
    negara1 = negara_split[0]
    negara2 = negara_split[1]
    col14.metric(negara1,negara2)
else:
    negara1 = negara_min_cumm
    col14.metric('Negara',negara1)
col54.metric('Produksi', '(bbl)', delta=min_cumm)

region = 'test'
subregion = 'test1'
for data in json_data:
    if data['alpha-3'] == kode_negara:
        region = data['region']
        subregion = data['sub-region']
subregion1=subregion.split()[0]
subregion2=subregion.split()[1]
col24.metric('Kode Negara', kode_negara)
col34.metric('Region', region)
col44.metric(subregion1, subregion2)

st.header(f'Negara tanpa produksi minyak tahun {year}')
#produksi 0
#by year
negara_0_year = convert_kode_negara(df[(df['tahun']==year) & (df['produksi']==0)].kode_negara.values[0])
kode_negara1 = get_key(negara_0_year)
region = 'test'
subregion = 'test1'
for data in json_data:
    if data['alpha-3'] == kode_negara1:
        region = data['region']
        subregion = data['sub-region']
subregion1=subregion.split()[0]
subregion2=subregion.split()[1]

col411, col422, col433, col444 = st.columns(4)
negara1 = 'aa'
negara2 = 'bb'
negara_split = negara_0_year.split()
if len(negara_split)>1:
    negara1 = negara_split[0]
    negara2 = negara_split[1]
    col411.metric(negara1,negara2)
else:
    negara1 = negara_0_year
    col411.metric('Negara',negara1)
col422.metric('Kode Negara',kode_negara1)
col433.metric('Region', region)
col444.metric(subregion1, subregion2)

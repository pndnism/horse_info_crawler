# -*- coding: utf-8 -*-
# %%
URL = "https://db.netkeiba.com/race/202105030211/"
URL = "https://db.netkeiba.com/race/2021A7a00104/"

# %%
import requests
from bs4 import BeautifulSoup

# %%
response = requests.get(URL)

# %%
soup = BeautifulSoup(response.content, "lxml")

# %%
tables = soup.find_all("table", summary="払い戻し")

# %%
tables

# %%
horse_detail_dict = {}
for table in tables:
    count = 0
    for i in table.find_all("th"):
        horse_detail_dict[i.text] = [i.get_text(',').split(',') for i in table.find_all("tr")[count].find_all("td")]
        count += 1

# %%
"複勝" in horse_detail_dict.keys()

# %%
horse_detail_dict = {}
for i in table.find_all("th"):
    horse_detail_dict[i.text] = []
for i in table.find_all('th'):
    count = 0
    tmp = i.find_all("td")
    for i in tmp:
        horse_detail_dict[list(horse_detail_dict.keys())[count]].append(i)
        count += 1

# %%
table.find_all("tr")[0].find("th").text

# %%
horse_detail_dict = {}
count = 0
for i in table.find_all("th"):
    horse_detail_dict[i.text] = [i.get_text(',').split(',') for i in table.find_all("tr")[count].find_all("td")]
    count += 1

# %%
horse_detail_dict

# %%
[i.text for i in table.find_all("tr")[0].find_all("td")]

# %%
[i.get_text(',').split(',') for i in table.find_all("tr")[1].find_all("td")]

# %%
[i.get_text(',').split(',') for i in table.find_all("tr")[2].find_all("td")]

# %%
[i.get_text(',').split(',') for i in table.find_all("tr")[3].find_all("td")]

# %%
import pandas as pd

# %%
pd.DataFrame().shape

# %%
tansho=[['5'], ['130'], ['1']]
fukusho=[['5', '6'], ['100', '130'], ['1', '2']]
umaren=[['5 - 6'], ['190'], ['1']]
wide=[['5 - 6', '2 - 5', '2 - 6'], ['120', '140', '160'], ['1', '2', '3']]
umatan=[['5 → 6'], ['260'], ['1']]
sanrentan=[['5 → 6 → 2'], ['570'], ['1']]
sanrenpuku=[['2 - 5 - 6'], ['290'], ['1']]

# %%
tansho_prize = tansho[1][0]
fukusho_prize_1st = fukusho[1][0]
fukusho_prize_2nd = fukusho[1][1]
umaren_prize = umaren[1][0]
wide_prize_1st_2nd = wide[1][0] 
wide_prize_1st_3rd = wide[1][1]
wide_prize_2nd_3rd = wide[1][2]
umatan_prize = umatan[1][0]
sanrentan_prize = sanrentan[1][0]
sanrenpuku_prize = sanrenpuku[1][0]

# %%
fukusho_prize_1st

# %%
test_dict = {'tansho_prize': '130',
 'fukusho_prize_1st': '100',
 'fukusho_prize_2nd': '130',
 'umaren_prize': '190',
 'wide_prize_1st_2nd': '120',
 'wide_prize_1st_3rd': '140',
 'wide_prize_2nd_3rd': '160',
 'umatan_prize': '260',
 'sanrentan_prize': '570',
 'sanrenpuku_prize': '290'}

# %%
pd.DataFrame(test_dict,index=[0])

# %%

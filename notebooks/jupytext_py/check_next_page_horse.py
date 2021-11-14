# -*- coding: utf-8 -*-
# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# %%
normal_url = "https://db.netkeiba.com/?sort_key=prize&sort_type=desc&pid=horse_list&serial=a%3A20%3A%7Bs%3A3%3A%22pid%22%3Bs%3A10%3A%22horse_list%22%3Bs%3A4%3A%22word%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sire%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22keito%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22mare%22%3Bs%3A0%3A%22%22%3Bs%3A3%3A%22bms%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22trainer%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22owner%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22breeder%22%3Bs%3A0%3A%22%22%3Bs%3A3%3A%22sex%22%3Ba%3A3%3A%7Bi%3A0%3Bs%3A1%3A%221%22%3Bi%3A1%3Bs%3A1%3A%222%22%3Bi%3A2%3Bs%3A1%3A%223%22%3B%7Ds%3A9%3A%22under_age%22%3Bs%3A1%3A%222%22%3Bs%3A8%3A%22over_age%22%3Bs%3A4%3A%22none%22%3Bs%3A9%3A%22prize_min%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22prize_max%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sort%22%3Bs%3A5%3A%22prize%22%3Bs%3A4%3A%22list%22%3Bs%3A2%3A%2220%22%3Bs%3A9%3A%22style_dir%22%3Bs%3A17%3A%22style%2Fnetkeiba.ja%22%3Bs%3A13%3A%22template_file%22%3Bs%3A15%3A%22horse_list.html%22%3Bs%3A9%3A%22style_url%22%3Bs%3A18%3A%22%2Fstyle%2Fnetkeiba.ja%22%3Bs%3A6%3A%22search%22%3Bs%3A35%3A%22%C0%AD%CA%CC%5B%B2%B4%A1%A2%CC%C6%A1%A2%A5%BB%5D%A1%A2%C7%AF%CE%F0%5B2%BA%D0%A1%C1%CC%B5%BB%D8%C4%EA%5D%22%3B%7D&page=960"
check_url = "https://db.netkeiba.com/?sort_key=prize&sort_type=desc&pid=horse_list&serial=a%3A20%3A%7Bs%3A3%3A%22pid%22%3Bs%3A10%3A%22horse_list%22%3Bs%3A4%3A%22word%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sire%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22keito%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22mare%22%3Bs%3A0%3A%22%22%3Bs%3A3%3A%22bms%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22trainer%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22owner%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22breeder%22%3Bs%3A0%3A%22%22%3Bs%3A3%3A%22sex%22%3Ba%3A3%3A%7Bi%3A0%3Bs%3A1%3A%221%22%3Bi%3A1%3Bs%3A1%3A%222%22%3Bi%3A2%3Bs%3A1%3A%223%22%3B%7Ds%3A9%3A%22under_age%22%3Bs%3A1%3A%222%22%3Bs%3A8%3A%22over_age%22%3Bs%3A4%3A%22none%22%3Bs%3A9%3A%22prize_min%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22prize_max%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sort%22%3Bs%3A5%3A%22prize%22%3Bs%3A4%3A%22list%22%3Bs%3A2%3A%2220%22%3Bs%3A9%3A%22style_dir%22%3Bs%3A17%3A%22style%2Fnetkeiba.ja%22%3Bs%3A13%3A%22template_file%22%3Bs%3A15%3A%22horse_list.html%22%3Bs%3A9%3A%22style_url%22%3Bs%3A18%3A%22%2Fstyle%2Fnetkeiba.ja%22%3Bs%3A6%3A%22search%22%3Bs%3A35%3A%22%C0%AD%CA%CC%5B%B2%B4%A1%A2%CC%C6%A1%A2%A5%BB%5D%A1%A2%C7%AF%CE%F0%5B2%BA%D0%A1%C1%CC%B5%BB%D8%C4%EA%5D%22%3B%7D&page=961"

# %%
response = requests.get(normal_url)

# %%
soup = BeautifulSoup(response.content, 'lxml')

# %%
next_page_post_parameter = None
next_page_element = soup.select_one("div.pager a:contains('次')")


# %%
next_page_element

# %%
normal_url = "https://db.netkeiba.com/?sort_key=date&sort_type=desc&pid=race_list&serial=a%3A15%3A%7Bs%3A3%3A%22pid%22%3Bs%3A9%3A%22race_list%22%3Bs%3A4%3A%22word%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22track%22%3Ba%3A2%3A%7Bi%3A0%3Bs%3A1%3A%221%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7Ds%3A10%3A%22start_year%22%3Bs%3A4%3A%22none%22%3Bs%3A9%3A%22start_mon%22%3Bs%3A4%3A%22none%22%3Bs%3A8%3A%22end_year%22%3Bs%3A4%3A%22none%22%3Bs%3A7%3A%22end_mon%22%3Bs%3A4%3A%22none%22%3Bs%3A9%3A%22kyori_min%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22kyori_max%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sort%22%3Bs%3A4%3A%22date%22%3Bs%3A4%3A%22list%22%3Bs%3A2%3A%2220%22%3Bs%3A9%3A%22style_dir%22%3Bs%3A17%3A%22style%2Fnetkeiba.ja%22%3Bs%3A13%3A%22template_file%22%3Bs%3A14%3A%22race_list.html%22%3Bs%3A9%3A%22style_url%22%3Bs%3A18%3A%22%2Fstyle%2Fnetkeiba.ja%22%3Bs%3A6%3A%22search%22%3Bs%3A42%3A%22%B6%A5%C1%F6%BC%EF%CA%CC%5B%BC%C7%A1%A2%A5%C0%A1%BC%A5%C8%5D%A1%A2%B4%FC%B4%D6%5B%CC%B5%BB%D8%C4%EA%A1%C1%CC%B5%BB%D8%C4%EA%5D%22%3B%7D&page=7562"
check_url = "https://db.netkeiba.com/?sort_key=date&sort_type=desc&pid=race_list&serial=a%3A15%3A%7Bs%3A3%3A%22pid%22%3Bs%3A9%3A%22race_list%22%3Bs%3A4%3A%22word%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22track%22%3Ba%3A2%3A%7Bi%3A0%3Bs%3A1%3A%221%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7Ds%3A10%3A%22start_year%22%3Bs%3A4%3A%22none%22%3Bs%3A9%3A%22start_mon%22%3Bs%3A4%3A%22none%22%3Bs%3A8%3A%22end_year%22%3Bs%3A4%3A%22none%22%3Bs%3A7%3A%22end_mon%22%3Bs%3A4%3A%22none%22%3Bs%3A9%3A%22kyori_min%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22kyori_max%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sort%22%3Bs%3A4%3A%22date%22%3Bs%3A4%3A%22list%22%3Bs%3A2%3A%2220%22%3Bs%3A9%3A%22style_dir%22%3Bs%3A17%3A%22style%2Fnetkeiba.ja%22%3Bs%3A13%3A%22template_file%22%3Bs%3A14%3A%22race_list.html%22%3Bs%3A9%3A%22style_url%22%3Bs%3A18%3A%22%2Fstyle%2Fnetkeiba.ja%22%3Bs%3A6%3A%22search%22%3Bs%3A42%3A%22%B6%A5%C1%F6%BC%EF%CA%CC%5B%BC%C7%A1%A2%A5%C0%A1%BC%A5%C8%5D%A1%A2%B4%FC%B4%D6%5B%CC%B5%BB%D8%C4%EA%A1%C1%CC%B5%BB%D8%C4%EA%5D%22%3B%7D&page=7563"

# %%
response = requests.get(normal_url)

# %%
soup = BeautifulSoup(response.content, 'html.parser')

# %%
next_page_post_parameter = None
next_page_element = soup.select_one("div.pager a:contains('次')")


# %%
next_page_element

# %%
response = requests.get(check_url)

# %%
soup = BeautifulSoup(response.content, 'html.parser')

# %%
next_page_post_parameter = None
next_page_element = soup.select_one("div.pager a:contains('次')")


# %%
next_page_element

# %%
soup

# %%

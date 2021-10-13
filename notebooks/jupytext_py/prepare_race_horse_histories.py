# %%
import glob
import pandas as pd

# %%
# horse
check_csvs = glob.glob("/Users/daikimiyazaki/workspace/pndnism/horse_race_prediction/horse_info_crawler/horse_info_crawler/pedigree/data/horse_info/**/*.csv",recursive=True)
concat_list = []
# if len(check_csvs) == 0:
#     return []
for i in check_csvs:
    concat_list.append(pd.read_csv(i))
concat_df = pd.concat(concat_list, axis=0)

# %%
concat_df.shape

# %%
concat_df.drop_duplicates().to_csv("shaped_horse_info_000000.csv", index=False)

# %%
# race
check_csvs = glob.glob("/Users/daikimiyazaki/workspace/pndnism/horse_race_prediction/horse_info_crawler/horse_info_crawler/race/data/race_histories/**/*.csv",recursive=True)
concat_list = []
# if len(check_csvs) == 0:
#     return []
for i in check_csvs:
    concat_list.append(pd.read_csv(i))
concat_df = pd.concat(concat_list, axis=0)
        

# %%
concat_df.shape

# %%
concat_df.drop_duplicates().shape

# %%
concat_df.drop_duplicates().to_csv("shaped_race_history_000000.csv", index=False)

# %%

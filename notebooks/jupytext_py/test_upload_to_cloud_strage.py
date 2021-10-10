# %%
from google.cloud import storage
import os
import pandas as pd



# %%
# Only need this if you're running this code locally.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/daikimiyazaki/.config/pndnism-project-fc40cb799b41.json'

df = pd.DataFrame(data=[{1,2,3},{4,5,6}],columns=['a','b','c'])

client = storage.Client()
bucket = client.get_bucket('pndnism_horse_data')
    
bucket.blob('upload_test/test.csv').upload_from_string(df.to_csv(), 'text/csv')

# %%

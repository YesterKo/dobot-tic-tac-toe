import pandas as pd

SHEET_ID = '1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA'
SHEET_NAME = 'Sheet1'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url).values.tolist()
df = [j for sub in df for j in sub if type(j)!=float]

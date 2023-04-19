import pandas as pd
import pygsheets
# https://docs.google.com/spreadsheets/d/1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA/gviz/tq?tqx=out:csv&sheet=Sheet1
SHEET_ID = '1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA'
SHEET_NAME = 'Sheet1'
def get_data_from_sheet(sheet_id, sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url).values.tolist()
    return df

naide_seis = [['b', 'r', 'l'], ['o', 't', 'o'], ['o', 'o', 'o']]

# df = get_data_from_sheet(SHEET_ID, SHEET_NAME)
def push_data_to_sheet(seis, sheet_id, sheet_name):
    df = pd.DataFrame(seis)
    df.dropna()
    gc = pygsheets.authorize(service_file='dobotnageminetripstrapstrull-bf6a690980de.json')
    sh = gc.open_by_url(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}')
    wks = sh.sheet1
    wks.set_dataframe(df,(1,1))
    return True

df = push_data_to_sheet(naide_seis, SHEET_ID, SHEET_NAME)

# df = pd.read_csv(url).values.tolist()
# df = [j for sub in df for j in sub if type(j)!=float]
print(df)


import pandas as pd
import pygsheets
# https://docs.google.com/spreadsheets/d/1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA/
SHEET_ID = '1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA'
SHEET_NAME = 'Sheet1'

# naide_seis = [['b', 'r', 'l'], ['o', 't', 'o'], ['o', 'o', 'o']]

class Sheet():

    def __init__(self, sheet_id, sheet_name) -> None:
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name

    def get_data_from_sheet(self):
        url = f'https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet={self.sheet_name}'
        # test = pd.read_csv(url, dtype=str, keep_default_na=False)
        #DO NOT add NUMBERS into the CSV thing or it will only get the numbers for you and not alphabetical characters
        df = pd.read_csv(url).astype(str) #! KOGU KURJA JUUR!!!
        print(df)
        data = df.drop(df.columns[0],axis=1).values.tolist() #saab actual board data kätte
        return data

    # df = get_data_from_sheet(SHEET_ID, SHEET_NAME)
    def push_data_to_sheet(self, seis):
        df = pd.DataFrame(seis)
        df.dropna()
        gc = pygsheets.authorize(service_file='dobotnageminetripstrapstrull-bf6a690980de.json')
        sh = gc.open_by_url(f'https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet={self.sheet_name}')
        wks = sh.sheet1
        wks.set_dataframe(df,(1,1))
        return True
    
leht = Sheet(SHEET_ID, SHEET_NAME)
print(leht.get_data_from_sheet())
# df = leht.push_data_to_sheet(naide_seis)
# # df = pd.read_csv(url).values.tolist()
# # df = [j for sub in df for j in sub if type(j)!=float]
# print(df)


import requests
from bs4 import BeautifulSoup
import pandas as pd


if __name__ == '__main__':

    #URL Requests
    website_url = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population').text

    #Souping
    soup = BeautifulSoup(website_url,'lxml')
    Top_Cities_Table = soup.find('table', {'class': 'wikitable sortable'})
    dataFrame_0 = pd.read_html(str(Top_Cities_Table))[0]

    #Data Cleaning
    dataFrame_0['City'] = dataFrame_0['City'].apply(lambda x: str(x)[0:str(x).find('[')] if '[' in str(x) else str(x))

    dataFrame_0.drop('Change', axis=1, inplace=True)
    dataFrame_0.drop('2016 land area.1',  axis=1, inplace=True)
    dataFrame_0.drop('2016 population density',  axis=1, inplace=True)
    dataFrame_0.drop('Location', axis=1, inplace=True)
    dataFrame_0.drop('2016 population density.1',  axis=1, inplace=True)
    dataFrame_0.drop('2018estimate', axis=1, inplace=True)
    dataFrame_0.drop('2016 land area', axis=1, inplace=True)


    cities = dataFrame_0['City'].values

    links = Top_Cities_Table.findAll('a')

    White = []
    white_bool = False
    Non_Hispanic_White = []
    non_hisp_bool = False
    Black = []
    black_bool = False
    Asian = []
    asian_bool = False
    Hispanic = []
    hisp_bool = False
    Other = []
    other_bool = False

    for link in links:

        if link.text in cities:
            web_string = 'https://en.wikipedia.org' + link.get('href')
            website_url_1 = requests.get(web_string).text
            soup_1 = BeautifulSoup(website_url_1, 'lxml')
            Racial_Composition_Table = soup_1.findAll('table', {'class':'wikitable sortable collapsible'})

            try:
                dataFrame_1 = pd.read_html(str(Racial_Composition_Table))[0]
                df_1 = dataFrame_1.iloc[:,0]

                df_2 = dataFrame_1.filter(regex='2010')

                final_dataFrame = pd.concat([df_1,df_2], axis=1)
                # print(final_dataFrame)

                for i, j in final_dataFrame.iterrows():

                    if 'White' == str(j[0]):
                        White.append(str(j[1]).replace('%',''))
                        white_bool = True
                        continue
                    if 'African' in str(j[0]):
                        Black.append(str(j[1]).replace('%',''))
                        black_bool = True
                        continue
                    if 'Latino' in str(j[0]) and 'Hispanic' in str(j[0]):
                        Hispanic.append(str(j[1]).replace('%',''))
                        hisp_bool = True
                        continue
                    if 'Asian' in str(j[0]):
                        Asian.append(str(j[1]).replace('%',''))
                        asian_bool = True
                        continue
                    if 'Other' in str(j[0]):
                        Other.append(str(j[1]).replace('%',''))
                        other_bool = True
                        continue
                    if 'Non-Hispanic' in str(j[0]):
                        Non_Hispanic_White.append(str(j[1]).replace('%',''))
                        non_hisp_bool = True
                        continue

            except ValueError:
                pass

            except IndexError:
                pass

            if non_hisp_bool:
                 non_hisp_bool = False
            else:
                Non_Hispanic_White.append("NA")

            if black_bool:
                black_bool = False
            else:
                Black.append("NA")

            if asian_bool:
                asian_bool = False
            else:
                Asian.append("NA")

            if hisp_bool:
                hisp_bool = False
            else:
                Hispanic.append("NA")

            if white_bool:
                white_bool = False
            else:
                White.append("NA")

            if other_bool:
                other_bool = False
            else:
                Other.append("NA")


    dataFrame_0["White"] = White
    dataFrame_0["Non_Hispanic_White"] = Non_Hispanic_White
    dataFrame_0["African_American"] = Black
    dataFrame_0["Asian"] = Asian
    dataFrame_0["Other"] = Other


    dataFrame_0.to_csv('data.csv', header=1, index=False)

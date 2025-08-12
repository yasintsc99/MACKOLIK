import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, url):
        self.url = url
        self.HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}
        self.session = requests.Session()

    def fetch_page(self):
        response = self.session.get(self.url,headers=self.HEADER)
        return response.text

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_data(self):
        html = self.fetch_page()
        soup = self.parse_html(html)
        return soup

    def fetch_data(self,season):
        data = self.get_data()
        statistics = data.find("div",attrs={"class":"page-competition-stats-index__container-widget widget-content-switch__content--left"}).find_all("section",attrs={"class":"p0c-competition-bet-stats__bet-stat p0c-competition-bet-stats__bet-stat--match-score"})
        index = 1
        all_data = []
        for statistic in statistics:
            if index == 1:
                index += 1
                continue
            else:
                header = statistic.find("div",attrs={"class":"widget-section-title-bar"}).text.strip()
                teams = statistic.find_all("div",attrs={"class":"p0c-competition-bet-stats__row"})
                for team in teams:
                    teamName = team.find("span",attrs={"class":"p0c-competition-bet-stats__row-header-title"}).text.strip()
                    statValue = team.find("span",attrs={"class":"p0c-competition-bet-stats__row-header-value"}).text.strip()
                    all_data.append({"Takım": teamName, header: statValue})
        # Create a Dataframe
        df = pd.DataFrame(all_data)
        # If exist for same team more than 1 statistics concat them
        df = df.groupby("Takım").first().reset_index()
        # Write to excel
        df.to_excel(f"{season} Sezonu Türkiye Süper Ligi Takım Bazında İstatistikler.xlsx", index=False)
        print(f"Excel dosyası oluşturuldu: {season} Sezonu Türkiye Süper Ligi Takım Bazında İstatistikler.xlsx")

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}
    rq = requests.get("https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-trendyol-s%C3%BCper-lig/2024-2025/istatistik/482ofyysbdbeoxauk19yg7tdt",headers=headers)
    soup = BeautifulSoup(rq.text,"html.parser")
    seasons = soup.find("select",attrs={"class":"component-dropdown__native"}).find_all("option")

    for season in seasons:
        seasonValue = season.text.strip()
        if "/" in seasonValue:
            seasonValue = seasonValue.replace("/","-")
            URL = f"https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-trendyol-s%C3%BCper-lig/{seasonValue}/istatistik/482ofyysbdbeoxauk19yg7tdt"
            Scraper(URL).fetch_data(seasonValue)
        else:
            URL = f"https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-trendyol-s%C3%BCper-lig/{seasonValue}/istatistik/482ofyysbdbeoxauk19yg7tdt"
            Scraper(URL).fetch_data(seasonValue)
if __name__ == "__main__":
    main()
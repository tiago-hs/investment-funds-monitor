import os

import requests
from parsel import Selector


class FIDailyInfCollector:
    URL = "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/"

    def __init__(self, path):
        self.path = path

    def __fetch(self):
        response = requests.get(self.URL)
        html = Selector(text=response.text)
        return html

    def collect(self):
        html = self.__fetch()
        files_list = html.xpath('//pre/a[re:test(@href, "inf_diario")]/@href').getall()

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        for file in files_list:
            zip_url = os.path.join(self.URL, file)
            filename = os.path.join(self.path, file)

            with open(filename, "wb") as f:
                zip_response = requests.get(zip_url)
                f.write(zip_response.content)
            print(f"--> File: {file} downloaded.")

        downloads_total = len(os.listdir(self.path))
        print(f"Total: {downloads_total}")


# ----


def main():
    path = "download"
    collector = FIDailyInfCollector(path)
    collector.collect()


if __name__ == "__main__":
    main()

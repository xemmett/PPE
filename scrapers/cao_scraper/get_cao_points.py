import urllib.request as urq
import tabula
import pandas as pd

def download_file(url, filename):
    response = urq.urlopen(url)
    resobj = response.read()
    print(response.url)
    with open(filename, mode='wb') as outfile:
        outfile.write(resobj)

def create_dataset():
    # 25 years worth of points
    url_base = "http://www2.cao.ie/app_scoring/points_stats/lc{}pts.pdf"
    filename_base = "2_pages_test/lc{}pts.csv"
    for i in range(1995, 2022):
        try:
            year_str = str(i)[2:]
            url = url_base.format(year_str)
            filename = filename_base.format(year_str)
            download_file(url, filename)
            df = tabula.read_pdf(filename, pages=2)[0]
            year_column = [i for x in range(0, len(df))]
            df.to_csv(filename, index=False)
        except:
            print(i)

create_dataset()

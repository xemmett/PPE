import urllib.request as urq
import tabula
import pandas as pd

def download_file(url, filename):
    request = urq.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36')
    response = urq.urlopen(url)
    resobj = response.read()
    print(response.headers)
    with open(filename, mode='wb') as outfile:
        outfile.write(resobj)

def create_dataset():
    # 25 years worth of points
    for lvl in range(8, 6, -1):
        url_base = "http://www2.cao.ie/points/lvl{}_{}.pdf"
        filename_base = "coursepts/lvl{}_{}course_pts.csv"
        for i in range(2018, 1997, -1):
            # try:
            year_str = str(i)[2:]
            url = url_base.format(lvl, year_str)
            filename = filename_base.format(lvl, year_str)
            download_file(url, filename)
            df = tabula.read_pdf(filename, pages=2)
            masterdf = pd.DataFrame([], columns=['course_code', 'institution_and_course', 'lowest_accepted', 'median_accepted'])
            for d in df:
                masterdf+=d
            masterdf.to_csv(filename, index=False)
            # except:
                # print(i)
            break

create_dataset()

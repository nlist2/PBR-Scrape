import time
from bs4 import BeautifulSoup
import pandas as pd


def get_comments_new(url, sess):

    r = sess.get(url, headers=dict(Referer=url))
    if r.status_code == 404:
        return None
    if r.status_code == 500:
        time.sleep(600)
        raise ConnectionError

    soup = BeautifulSoup(r.text, 'html.parser')
    soup_tester = soup.select_one('#college-profile')

    college = 0
    if soup_tester is not None:
        print("has college")
        college = 1
    else:
        print("no college")

    reports = []

    # get hs reports
    comments = soup.select('.player-comment')
    for rep in comments:
        print('hsrepor')
        try:
            date = rep.select_one('.comment-date').text.strip()
        except:
            date = None
        if date is None:
            try:
                date = rep.select_one('.comment strong').text.strip()
                rep.select_one('.comment strong').decompose()
            except:
                date = None
            if date is None:
                try:
                    report = rep.select_one('.comment span').text.strip()
                    rep.select_one('.comment span').decompose()
                    date = rep.select_one('.comment').text.strip()
                except:
                    date = None
                    report = rep.select_one('.comment').text.strip()
            else:
                report = rep.select_one('.comment').text.strip()
        else:
            report = rep.select_one('.comment').text.strip()
        try:
            reports.append({'report': report, 'date': date, 'type': 'hs'})
        except Exception as e:
            print(date, rep.select_one('.comment').text.strip())
            print(str(e))
            print(rep.prettify())
            raise e

    # get college reports
    if college == 1:
        comments = soup.select('#college_tab2 p')
        for rep in comments:
            try:
                date = rep.select_one('strong').text.strip()
                rep.select_one('strong').decompose()
            except:
                date = None
            report = rep.text.strip()
            reports.append({'report': report, 'date': date, 'type': 'college'})
    print(reports)
    if reports == []:
        reports.append({'report': 'no_reports', 'date': '', 'type': ''})
    return pd.DataFrame(reports)
from seleniumbase import SB
import pandas as pd
import sys

print('==== Scopus H-index Scraper V1.0.0 ====')

if len(sys.argv) != 2:
    print('    Error: bad argument\n'
          '\n'
          '    Usage: ScopusHindexFinder [path to Excel]\n'
          '\n'
          '    Excel should look like:\n'
          '    Lastname  |  Firstname  |  Affiliation\n'
          '    Jansen    |     Jan     |')
    exit()


def verify_success(sb):
    sb.assert_element('img[alt="Elsevier"]', timeout=4)
    sb.sleep(3)


with SB(uc=True) as sb:
    sb.uc_open_with_reconnect("http://www.scopus.com/freelookup/form/author.uri", 3)
    try:
        verify_success(sb)
    except Exception:
        if sb.is_element_visible('input[value*="Verify"]'):
            sb.uc_click('input[value*="Verify"]')
        else:
            sb.uc_gui_click_captcha()
        try:
            verify_success(sb)
        except Exception:
            raise Exception("Detected!")

    df = pd.read_excel(sys.argv[1])
    df.fillna('', inplace=True)

    for index, row in df.iterrows():
        row = row.copy()

        sb.type('#lastname', row[0])
        sb.type('#firstname', row[1])
        sb.type('#institute', row[2])

        sb.click('#authorSubmitBtn')

        try:
            sb.assert_element_absent('#resultDataRow2', timeout=4)
        except Exception:
            df.loc[index, 'Num Pub'] = 'Multiple Authors found'
            sb.go_back()
            continue

        try:
            sb.click('#resultDataRow1 > td.authorResultsNamesCol.col20 > a')
        except Exception:
            df.loc[index, 'Num Pub'] = 'Scopus has no info on Author'
            sb.go_back()
            continue

        df.loc[index, 'Num Pub'] = int(sb.get_text('#scopus-author-profile-page-control-microui__general-information'
                                                   '-content > div:nth-child(3) > section > div > div:nth-child(1) > '
                                                   'div > div > div > div:nth-child(1) > span').replace(',', ''))
        df.loc[index, 'Citations'] = int(sb.get_text('#scopus-author-profile-page-control-microui__general-information'
                                                     '-content > div:nth-child(3) > section > div > div:nth-child(2) > '
                                                     'div > div > div > div:nth-child(1) > span').replace(',', ''))
        df.loc[index, 'h-index'] = int(sb.get_text('#scopus-author-profile-page-control-microui__general-information'
                                                   '-content > div:nth-child(3) > section > div > div:nth-child(3) > '
                                                   'div > div > div > div:nth-child(1) > span').replace(',', ''))

        sb.go_back()
        sb.go_back()

    # output
    df.to_excel("output.xlsx")

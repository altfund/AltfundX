import requests
import bs4
import re
import csv


def clean_symbol(value):
    symbol = '*$%,'
    exclude = set(symbol)
    value = ''.join(ch for ch in value if ch not in exclude)
    value = value.replace("?", "NA")
    return value

base_url = "https://coinmarketcap.com"
r = requests.get(r'https://coinmarketcap.com/historical/')

soup = bs4.BeautifulSoup(r.text)
years = soup('h2')
for year in years:
    print(year)
blocks = []
valid_url_list = []

fields = [
    "Name",
    "Symbol",
    "Market Cap",
    "Price",
    "Circulating Supply",
    "1h",
    "24h",
    "7d",
    "Is Mined",
    "Date",
]

out_file = open('data.csv',"w", newline="")
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
csvwriter.writerow(dict((fn,fn) for fn in fields))

for year in years:
    blocks.append(year.find_parent('div'))

    for block in blocks:
        year = block('h2')[0].text
        months = block('div', class_= re.compile('col'))
        for month in months:
            cur_month_str = month('h3')[0].text
            day = month.select('a')[0].text
            cur_hyperlink = month.select('a')

            for link in cur_hyperlink:
                hyperlink = link['href']
                valid_url = base_url + hyperlink

                if valid_url not in valid_url_list:
                    valid_url_list.append(valid_url)
                    response = requests.get(valid_url)
                    table_soup = bs4.BeautifulSoup(response.text)
                    table = table_soup.find('table')
                    x = (len(table.findAll('tr')) - 1)
                    for row in table.findAll('tr')[1:x]:
                        col = row.findAll('td')
                        sample_dict = {}
                        sample_dict['Name'] = col[1].findAll('a')[1].text
                        sample_dict['Symbol'] = col[2].getText()
                        sample_dict['Market Cap'] = clean_symbol(col[3].text.strip())
                        sample_dict['Price'] = clean_symbol(col[4].find('a').getText())
                        circulating_supply = col[5].find('a')
                        if not circulating_supply:
                            circulating_supply = col[5].find('span')
                        sample_dict['Circulating Supply'] = clean_symbol(circulating_supply.text.strip())

                        sample_dict['1h'] = clean_symbol(col[7].getText())
                        sample_dict['24h'] = clean_symbol(col[8].getText())
                        sample_dict['7d'] = clean_symbol(col[9].getText())

                        if "*" in col[5].text:
                            sample_dict['Is Mined'] = False
                        else:
                            sample_dict['Is Mined'] = True

                        date = valid_url.split("/")[-2]
                        date = "{}-{}-{}".format(date[:4], date[4:6], date[6:8])

                        sample_dict['Date'] = date
                        csvwriter.writerow(sample_dict)

                        print ("Processed Date:{}".format(date))

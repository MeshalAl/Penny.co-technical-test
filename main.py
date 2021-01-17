from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
import pandas as pd
import copy
from openpyxl import load_workbook

__author__ = "Meshal Alanazi <MeshalAlanaziNSA@gmail.com>"

def excel_sheet(items, data_dir, source=None, idx=None, **kwargs):

    excel_df = pd.ExcelFile(data_dir)
    sheets = excel_df.parse("Astro")
    itemdict = {'url' : '', 'data': {'img':[],'spec': {'column': [],'columninfo':[]}}}
    cols = {'image_source': []}
    itemlist = [copy.deepcopy(itemdict) for i in items]


    for index, i in enumerate(items):
        itemlist[index]['url'] = i.get('url')

        for j in i.get('images'):
            path = j.get('path')
            itemlist[index]['data']['img'].append(path)

        for counter, x in enumerate(i['spec']):
            if counter > 0:
                columnanditemlist = x.split(':')
                if columnanditemlist[0] and columnanditemlist[1]:
                    itemlist[index]['data']['spec']['column'].append(columnanditemlist[0])
                    itemlist[index]['data']['spec']['columninfo'].append(columnanditemlist[1])

    for i in itemlist:
        x = i.get('data').get('spec').get('column')
        for colname in x:
            if colname not in cols:
                if colname:
                    cols[str(colname)] = list()

    dataitems = []
    for i in itemlist:
        x = {'image_source': i.get('data').get('img')}
        for j, column in enumerate(i.get('data').get('spec').get('column')):
            x[column] = i.get('data').get('spec').get('columninfo')[j]
        dataitems.append(x)
    data = pd.DataFrame(dataitems, columns=cols)
    data.drop(data.columns[data.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    sheets.drop(sheets.columns[sheets.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    final = [sheets, data]
    finaldf = pd.concat(final, axis=1)
    finaldf.to_excel(kwargs.get('resdir')+'/result.xlsx', sheet_name='Astro')




def start_crawler(data, **kwargs):  # todo base spider logic, modularity (time-consuming)

    idx = kwargs.get('idx')
    process = CrawlerProcess(get_project_settings())

    items = []

    def item_scraped(item, response, spider):
        items.append(item)

    if 'source' in kwargs:  # checks if crawler needs a source site and keyword to search with
        crawler = process.create_crawler()
        source = kwargs.get('source')
        process.crawl('Knipex', url=data[source].tolist(), idx=data[idx].tolist())
    else:
        crawler = process.create_crawler('Astro')
        crawler.signals.connect(item_scraped, signal=signals.item_passed)
        process.crawl(crawler, url=data[idx].tolist())  # hits the page directly without searching

    process.start()

    return items

def data_source(loc, **kwargs):

    excel_df = pd.ExcelFile(loc)
    source = kwargs.get('source')
    idx = kwargs.get('idx')
    sheets = list()

    for i in excel_df.sheet_names:  # split into individual sheets
        df = pd.read_excel(loc, sheet_name=i)
        sheets.append(df)

    for i, sheet in enumerate(sheets):
        j = sheet[idx].iloc[0]
        if j.startswith('http'):  # check if identifier is needs a source website.
            sheets[i] = sheet[[idx]].dropna()  # strips all NaN rows, saves memory.
        else:  # idx is not a direct site, and needs a source site along with its id.
            sheets[i] = sheet[[source, idx]].dropna()

    return sheets

# suggested improvements:  1- a general purpose spider that can work without much modification.
#                          2- agreed upon identifier/source scheme that follows through on all sheets.
#                          3- multi-file support and extra functionality that are modular.
#                          4- error management and url restructuring when facing a 404 page.


def main(data_dir, save_dir='Data/Scrapped', resdir='Data/Source',idx="Identifier", source="Source"):

    astroDF, knipexDF = data_source(data_dir, idx=idx, source=source)

    astroitems = start_crawler(astroDF, idx=idx, savedir=save_dir)

    excel_sheet(data_dir=data_dir, items=astroitems, idx=idx, resdir=resdir)



if __name__ == "__main__":
    main('Data/Source/Dataset - Penny test.xlsx')

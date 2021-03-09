import requests
from requests import RequestException
from contextlib import closing

from lxml import html as LH
from prettytable import PrettyTable



def request_bestbuy(model):
    headers = {
        'authority': 'www.bestbuy.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'referer': f'https://www.bestbuy.com/site/searchpage.jsp?st={model}&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys',
        'accept-language': 'en-US,en;q=0.9'
    }

    params = (
        ('st', f'{model}'),
        ('_dyncharset', 'UTF-8'),
        ('_dynSessConf', ''),
        ('id', 'pcat17071'),
        ('type', 'page'),
        ('sc', 'Global'),
        ('cp', '1'),
        ('nrp', ''),
        ('sp', ''),
        ('qp', ''),
        ('list', 'n'),
        ('af', 'true'),
        ('iht', 'y'),
        ('usc', 'All Categories'),
        ('ks', '960'),
        ('keys', 'keys'),
        ('intl', 'nosplash'),
    )

    BASE_URL = 'https://www.bestbuy.com/site/searchpage.jsp'

    resp_content = None
    try:
        with closing(requests.get(BASE_URL,headers=headers, params=params)) as resp:
            resp_content = LH.fromstring(resp.content.decode(resp.encoding))
            return resp_content
    except RequestException as e:
        print(f"Error during requests to {BASE_URL} : {str(e)}")

def request_walmart(model):
    headers = {
        'authority': 'www.walmart.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-gpc': '1',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('query', f'{model}'),
    )
    BASE_URL = 'https://www.walmart.com/search/'

    resp_content = None
    try:
        with closing(requests.get(BASE_URL,headers=headers, params=params)) as resp:
            resp_content = LH.fromstring(resp.content.decode(resp.encoding))
            return resp_content
    except RequestException as e:
        print(f"Error during requests to {BASE_URL} : {str(e)}")

def request_bjs(model):

    headers = {
        'authority': 'bjswholesale-cors.groupbycloud.com',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'skip-caching': 'false',
        'sec-gpc': '1',
        'origin': 'https://www.bjs.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bjs.com/',
        'accept-language': 'en-US,en;q=0.9',
    }


    data = '{"pageSize":4,"area":"BCProduction","fields":["*"],"query":"'+model+'","collection":"productionB2CProducts","skip":0,"biasing":{"biases":[]},"pruneRefinements":false,"refinements":[{"navigationName":"visualVariant.nonvisualVariant.gbi_program_availability.clubID","type":"Value","value":"online"},{"navigationName":"visualVariant.nonvisualVariant.gbi_program_availability.clubID","type":"Value","value":"Club0109"},{"type":"Value","navigationName":"visualVariant.nonvisualVariant.gbi_program_availability.gbi_search_sdd","value":"online_Y"},{"type":"Value","navigationName":"visualVariant.nonvisualVariant.gbi_program_availability.gbi_search_sdd","value":"online_N"},{"type":"Value","navigationName":"visualVariant.nonvisualVariant.gbi_program_availability.gbi_search_sdd","value":"Club0109_Y"},{"type":"Value","navigationName":"visualVariant.nonvisualVariant.gbi_program_availability.gbi_search_sdd","value":"Club0109_N"}]}'

    BASE_URL = 'https://bjswholesale-cors.groupbycloud.com/api/v1/search'
    resp_content = None
    try:
        with closing(requests.post(BASE_URL,headers=headers, data=data)) as resp:
            resp_content = resp.json()
            return resp_content
    except RequestException as e:
        print(f"Error during requests to {BASE_URL} : {str(e)}")


def getPrice_bestbuy(queryModel):
    html_content = request_bestbuy(queryModel)
    item_list = html_content.xpath('//li[@class="sku-item"]')

    for item in item_list:
        model = item.findtext('.//span[@class="sku-value"]')
        price = item.findtext('.//div[@class="priceView-hero-price priceView-customer-price"]/span')
        if price and model:
            model = model.lower()
            if model.strip().startswith(queryModel.strip().lower()):
                return price

    return "N/A"

def getPrice_walmart(queryModel):
    html_content = request_walmart(queryModel)
    search_results = html_content.xpath('//div[@data-automation-id="search-result-listview-item"]')
    if len(search_results)>0:
        for item in search_results:
            title = item.xpath('.//a[@data-type="itemTitles"]')
            price = item.xpath('.//span[@class="price-group"]')
            if title and price:
                title_txt = title[0].text_content()
                price_txt = price[0].text_content()
                if queryModel.lower() in title_txt.lower() and 'refurbished' not in title_txt.lower():
                    try:
                        price = price_txt.strip('$')
                        print(price)
                        if float(price) < 70:
                            continue
                    except:
                        continue
                    return f"{price_txt}"
    return "N/A"

def getPrice_bjs(queryModel):
    resp_json = request_bjs(queryModel)
    records = resp_json.get('records')
    for record in records:
        allMeta = record.get('allMeta')
        if allMeta:
            title = allMeta.get('title')
            price = allMeta.get('visualVariant')[0].get('nonvisualVariant')[0].get('product_price')
            price = f"${price}"
            return price
            if queryModel.lower() in title.lower():
                return price
    return "N/A"


def request_amazon(model):
    headers = {
    'authority': 'www.amazon.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-gpc': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'referer': f'https://www.amazon.com/s?i=aps&k={model}&ref=nb_sb_noss_2&url=search-alias%3Daps',
    'accept-language': 'en-US,en;q=0.9'
    }

    params = (
        ('k', f'{model}'),
        ('ref', 'nb_sb_noss_2'),
    )
    BASE_URL = "https://www.amazon.com/s"

    resp_content = None
    try:
        with closing(requests.get(BASE_URL,headers=headers, params=params)) as resp:
            resp_content = LH.fromstring(resp.content.decode(resp.encoding))
            return resp_content
    except RequestException as e:
        print(f"Error during requests to {BASE_URL} : {str(e)}")

def getPrice_amazon(queryModel):
    html_content = request_amazon(queryModel)
    first_item_el = html_content.xpath('//div[@data-index="1"]')
    if len(first_item_el) > 0:
        first_item = first_item_el[0]
        title = first_item.find('.//span[@class="a-size-medium a-color-base a-text-normal"]')
        title = title.text_content() if len(title) > 0 else None
        price_elem = first_item.xpath('.//span[@class="a-price-whole"]/text()')
        if price_elem:
            price = price_elem[0]
            if queryModel.lower() in title.lower():
                if price:
                    return f"${price}"

    return "N/A"


def get_modelPrices(model):
    print(f"\nFetching Model: {model}.\n")
    dataObj = dict.fromkeys(["Model","bestbuy","bjs","walmart"])
    dataObj["Model"] = model.strip()
    model = model.strip()

    try:
        dataObj['bestbuy'] = getPrice_bestbuy(model)
    except:
        dataObj['bestbuy'] = "N/A"
    try:
        dataObj['bjs'] = getPrice_bjs(model)
    except:
        dataObj['bjs'] = "N/A"
    try:
        dataObj['walmart'] = getPrice_walmart(model)
    except:
        dataObj['walmart'] = "N/A"
    return dataObj


if __name__ == '__main__':

    models_input = input("Enter model string ( separated by , ) \n Example: 55UN7300, 65S423, UN43N5300, D40F-G9, 24LH4830\n: ")
    models= models_input.split(",")

    my_table = PrettyTable()
    my_table.field_names = ["Model#", "BestBuy", "Bjs", "Walmart"]
    for model in models:
        dataObj = get_modelPrices(model)
        my_table.add_row(dataObj.values())
        print(my_table.get_string())

    with open('output.csv', 'w') as f:
        f.write(my_table.get_csv_string())
    input(f"\nFinished,Press Enter to exit.\n")

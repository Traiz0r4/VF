import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import openpyxl as ox



iherb_url = 'https://ru.iherb.com/'
start_time = time.time()
cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}

globalchoice = []

top_twelve = []


def main(inquiry):  # основная функция
    # inquiry= input("Введите ваш запрос:\n") #ввод запроса
    inquiry = inquiry.replace(" ", "%20")
    href = 'https://ru.iherb.com/' + f'search?kw={inquiry}&cids=1855'  # переход по ссылке поиска

    url = href
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_product_links = soup.find_all('a', class_='absolute-link product-link')
    print(f'Количество товаров: {len(all_product_links)}')
    if len(soup.find_all(class_='no-results')) != 0:  # проверка на существование такого товара
        print(f'Не удается найти элементы, соответствующие запросу: " {inquiry} "\n ')
        print('The end!')
    else:
        print("Бестселлеры")
        made_url(url + f'&sr=4')

        print("Цена по возрастанию")
        made_url(url + f'&sr=2')
        finish_time = time.time()
        save(inquiry, start_time, finish_time)
    # --------------------------------------------


def made_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_product_links = soup.find_all('a', class_='absolute-link product-link')
    parsing(all_product_links)


def parsing(all_product_links):
    counter = 0
    for href in range(len(all_product_links)):
        if counter < 6:
            dict = {}
            url = all_product_links[href]['href']
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                availability = soup.find("div", class_="text-danger stock-status-text").text
            except:
                comments = soup.find("a", class_="rating-count").find("span").text
                # if availability.find("Нет в наличии")!=-1 and int(comments)>400:
                if int(comments) > 400:
                    print(f'Обрабатываем товар {counter}')
                    print(f"href: {all_product_links[href]['href']}")
                    name_of_product = soup.find(id='name').text  # имя продукта
                    dict["Название продукта"] = name_of_product
                    dict["Ссылка"] = all_product_links[href]['href']
                    try:
                        new_price = soup.find('b', class_='s24').text
                        old_price = soup.find(id='price').text
                        dict["Цена со скидкой"] = new_price
                        dict["Цена"] = old_price
                    except:
                        old_price = soup.find(id='price', class_='col-xs-15 col-md-15 price our-price').text
                        dict["Цена"] = old_price
                        dict["Цена со скидкой"] = "-"
                    company = soup.find("span", itemprop="name").find("bdi").text
                    dict["Производитель"] = company
                    try:
                        amount_of_capsulse = soup.find("div",
                                                       class_="attribute-group-количество-в-упаковке attribute-tile-group").find_all(
                            "div", class_="attribute-name")
                        capsulse = ''
                        for amount in amount_of_capsulse:
                            capsulse += str(amount["data-val"]) + " \ "
                    except:
                        try:
                            capsulse = soup.find("div", class_="item combo-shaded stock-onsale").find("div",
                                                                                                      class_="attribute-name").text
                        except:
                            capsulse = name_of_product.split(",")[-1]
                    mark = (soup.find('a', class_='stars'))['title'][0:5]

                    dict["Рейтинг"] = mark
                    dict["Капсулы"] = capsulse
                    dict["Отзывы"] = comments
                    solution = filter_name(name_of_product, top_twelve)
                    if solution == False:
                        print("Добавляем товар в словарь бестселлеров")
                        print("--------------------------")
                        top_twelve.append(dict)
                        counter += 1
        else:

            break


def filter_name(name, product_list):
    print("Проверяем на наличие в словаре")
    if len(product_list) != 0:
        for elem in range(len(product_list)):
            if name == product_list[elem]["Название продукта"]:
                return (True)
            else:
                return (False)
    else:
        return (False)


def save(inquiry, start_time, finish_time):
    # ----------
    inquiry = inquiry.replace("%20", " ")
    df = pd.DataFrame(top_twelve)
    print("Сохраняем все в отчет.")
    # ---------------------------------------------------------
    #update_spreadsheet('././Files/otchet.xlsx', df, sheet_name='1')
    writer = pd.ExcelWriter('././Files/report.xlsx')  # здесь путь настроить
    # ---------------------------------------------------------
    df.to_excel(writer, sheet_name='inquiry', index=False, na_rep='NaN')

    # column_width = max(df['Название продукта'].astype(str).map(len).max(), len('Название продукта'))
    # col_idx = df.columns.get_loc('Название продукта')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, column_width-5)

    # col_idx = df.columns.get_loc('Ссылка')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, 10)

    # col_idx = df.columns.get_loc('Цена со скидкой')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, 10)

    # col_idx = df.columns.get_loc('Цена')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, 12)

    # col_idx = df.columns.get_loc('Производитель')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, 8)

    # col_idx = df.columns.get_loc('Рейтинг')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, 8)

    # column_width = max(df['Капсулы'].astype(str).map(len).max(), len('Капсулы'))
    # col_idx = df.columns.get_loc('Капсулы')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, column_width)

    # col_idx = df.columns.get_loc('Отзывы')
    # writer.sheets[inquiry].set_column(col_idx, col_idx, 8)

    print("Сохраняем все в отчет.")
    writer.save()

    print("Время парсинга данных:", round(finish_time - start_time))

# Чтобы отдельно проверить роботоспособность расскоментируй:
# if __name__=='__main__':
#     main()


def update_spreadsheet(path: str, _df, starcol: int = 1, startrow: int = 1, sheet_name: str = "ToUpdate"):
    '''

    :param path: Путь до файла Excel
    :param _df: Датафрейм Pandas для записи
    :param starcol: Стартовая колонка в таблице листа Excel, куда буду писать данные
    :param startrow: Стартовая строка в таблице листа Excel, куда буду писать данные
    :param sheet_name: Имя листа в таблице Excel, куда буду писать данные
    :return:
    '''
    wb = ox.load_workbook(path)
    for ir in range(0, len(_df)):
        for ic in range(0, len(_df.iloc[ir])):
            wb[sheet_name].cell(startrow + ir, starcol + ic).value = _df.iloc[ir][ic]
    wb.save(path)
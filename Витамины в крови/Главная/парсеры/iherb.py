import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd


iherb_url = 'https://ru.iherb.com/'
start_time = time.time()
cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
product_data = []
globalchoice = []

top_twelve = []# СЮДА ВСЕ СОХАРНЯЕТСЯ, В СПИСОК СЛОВАРЕЙ


def main(searchzapros):  # основная функция
    inquiry = searchzapros # ввод запроса
    inquiry = inquiry.replace(" ", "%20")
    href = 'https://ru.iherb.com/' + f'search?kw={inquiry}&cids=1855'+'&ranges=2'  # переход по ссылке поиска

    sol = input('\nВы хотите использовать фильтры? д/н\n')
    if sol.lower() == 'д' or sol.lower() == 'l':
        url = filtration(
            href)  # (*) Функция вызова функций фильтрации, сюда же вернеться значение с которым мы и дальше будем работать
        # url=href
    else:
        print('Результат без использования фильтрации')
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
        report()
        save(inquiry, start_time)
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
                    dict["name_of_product"] = name_of_product
                    dict["href"] = all_product_links[href]['href']
                    try:
                        new_price = soup.find('b', class_='s24').text
                        old_price = soup.find(id='price').text
                        dict["new_price"] = new_price
                        dict["old_price"] = old_price
                    except:
                        old_price = soup.find(id='price', class_='col-xs-15 col-md-15 price our-price').text
                        dict["old_price"] = old_price
                    company = soup.find("span", itemprop="name").find("bdi").text
                    dict["company"] = company
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

                    dict["mark"] = mark
                    dict["amount_of_capsulse"] = capsulse
                    dict["amount_of_comments"] = comments
                    solution = filter_name(name_of_product, top_twelve)
                    print(f'solution={solution}')
                    if solution == False:
                        print("Добавляем товар в словарь бестселлеров")
                        top_twelve.append(dict)
                        counter += 1
        else:
            break


def filter_name(name, product_list):
    print("Проверяем на наличие в словаре")
    print(f'len: {len(product_list)}')
    if len(product_list) != 0:
        for elem in range(len(product_list)):
            if name == product_list[elem]["name_of_product"]:
                return (True)
            else:
                return (False)
    else:
        return (False)


def save(inquiry, start_time):# ФУНКЦИЯ СОХРАНЕНИЯ
    # -----------
    # inquiry=inquiry
    search_info = {'Дата и Время запроса:': [time.ctime()],
                   'Запрос пользователя:': [inquiry],
                   "Фильтры:": [globalchoice]}

    sheet2 = pd.DataFrame(search_info)
    sheet1 = pd.DataFrame(top_twelve)  # сохраням на третий лист данные из топ 5 бесцеллеров и цены по возрастанию
    # ---------------------------------------------------------------------
    print("Сохраняем все в отчет.")
    # пишем в наш файл данные----------------------------------------------
    sheets_name = {'top_ten_products': sheet1, 'info': sheet2}
    writer = pd.ExcelWriter(f'./report.xlsx', engine='xlsxwriter')
    for sheet_name in sheets_name.keys():
        sheets_name[sheet_name].to_excel(writer, sheet_name=sheet_name)
    writer.save()
    # -----------
    print("Время выполнения:", round(time.time() - start_time))

# Функция фильтрации итогово отчета
def report():
    report = {
        1: "name_of_product",
        2: "mark",
        3: "href",
        4: "old_price",
        5: "new_price",
        6: "company",
        7: "amount_of_capsulse",
        8: "amount_of_comments",
    }

    h = input(
        "Выберите параметры НЕ вносимые в отчет:\n 1)Наименование товара\n 2)Рейтинг\n 3)Cсылка\n 4)Цена\n 5)Цена со скидкой\n 6)Компания производитель\n 7)Количество штук в упаковке\n 8)Количество положительных комментариев\nДля окончания ввода, просто нажмите Enter...\n")

    while h != '':
        for k, v in report.items():
            if int(h) == k:
                sort_and_del(v)
        h = input("Хорошо, выберите еще (для прекращения просто нажмите Enter)")


# функция удаления данных из итогово отчета
def sort_and_del(v):
    for elem in range(len(product_data)):
        try:
            del product_data[elem][v]
        except:
            pass


if __name__ == '__main__':
    main()

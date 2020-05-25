from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from product import Product
# indian rupee char = ₹
# the targeted URL to get the specified information, in this case 'Amazon.in'
URL = 'https://www.amazon.in/'

# taking input product from the user
search_query = input("\nWhat product are you looking for?\n: ")

# Giving web driver options for chrome like opening in incognito etc.
chr_option = webdriver.ChromeOptions()
chr_option.add_argument('--ignore-certificate-errors')
# chrOption.add_argument('--headless')    #this will not open the browser, when the scraper is run
chr_option.add_argument('--incognito')
# assigning the webdriver to get a particular website
driver = webdriver.Chrome(
    executable_path="C:/Users/Maanki jewel/Desktop/chromedriver", chrome_options=chr_option)
driver.get(URL)

# searching automatically on the website
element = driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
element.send_keys(search_query, Keys.ENTER)
print("Done!")

# From the extracted price removce the ₹ Symbol, and the (comma) punctuation


def convert_to_price(price):
    try:
        upd_price = price.split('₹')[1]
        try:
            array = upd_price.split(',')
            for ele in array:
                newPrice += ele
        except:
            Exception()
    except:
        Exception()
    finally:
        return float(newPrice)


pageNo = 1
counter = 0
products = []

# Sample 1: traversing through the pages by changing the URL
'''
while(True):
    if(pageNo != 1):
         try:
             change the URL again for different page
             driver.get(driver.current_url + "&page=" + str(pageNo))
         except:
             break;
'''

# Sample 2 : traversing through th pages by clicking the next button on website
while True:
    if pageNo != 1:
        try:
            # traverse to the next page if possible when scraping for pageNo 1 is done.
            nextPage = driver.find_element_by_xpath('//li[@class="a-last"]/a')
            nextPage.click()
        except:
            break

    print('Page No. : ' + str(pageNo) + '\n')

    # Gives us all the product boxes of the page
    for box in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div'):
        canAddProduct = True  # defines; Is there a item for scraping or not
        title = ''
        curr_price = ''
        prev_price = ''
        link = ''

        try:
            #print(str(counter) + ':\n')

            # scrape the product's title
            title = box.find_element_by_tag_name('h2').text
            #print('\ttitle : ' + title + '\n')

            # scrape the product's current price
            curr_price = convert_to_price(
                box.find_element_by_class_name('a-price-whole').text)
            #print('\tcurrent price : ' + str(curr_price) + '\n')

            # scrape the product's link
            link = box.find_elements_by_xpath(
                '//h2/a[@class="a-link-normal a-text-normal"]')[counter].get_attribute('href')
            #print('\tlink : ' + link + '\n')

            try:
                # scrape the product's previous price
                prev_price = convert_to_price(
                    box.find_element_by_class_name('a-text-price').text)
                #print('\tprevious price : ' + str(prev_price) + '\n')
            except:
                Exception()
        except:
            Exception(
                '\n---There is no product in this element of the productArray---\n')
            canAddProduct = False

        if(canAddProduct):
            # if there is a product then add it to the list of products
            products.append(Product(title, curr_price, prev_price, link))
            print(products)
        counter += 1
    pageNo += 1

    if pageNo == 10:
        break

for p in products:
    p.expelliarmus()

max_discount = 0.0  # variable for storing the maximum discount price
min_price = 0.0  # variable for storing the lowest price of a product
# creating an object of Product for the cheapest product
cheapest_product = Product('', 0.0, 0.0, '')
# creating an object of Product for the best deal
best_deal = Product('', 0.0, 0.0, '')
# splitting each word of the search_query to check it is valid or not
search_terms = search_query.split(' ')
not_intialise = True  # to initialise the above variables with their default products

for product in products:
    # showing whether the searched product is relevant or not
    valid_product = True
    for words in search_terms:
        if words.lower() not in product.title.lower():
            not_valid_product = False

    if valid_product:  # if it is a valid product then find the best deal and the cheapest product
        if not_intialise:
            min_price = product.curr_price
            cheapest_product = product
            not_intialise = True

        # to find the cheapest product
        elif product.curr_price < min_price:
            min_price = product.curr_price
            cheapest_product = product

        # try to get a discount value if a product has a previous value
        try:
            discount = product.prev_price - product.curr_price
        except:
            Exception()
            discount = 0.0

        # to find product with the best deal (sorted by discount)
        if discount > max_discount:
            max_discount = discount
            best_deal = product

# print the best deal
print('Best Deal\n:')
best_deal.expelliarmus()

# print the cheapest product
print('Cheapest Product\n:')
cheapest_product.expelliarmus()

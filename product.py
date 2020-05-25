#each product must have these charactersitics as follows:
class Product:
    def __init__(self, title, curr_price, prev_price, link):
        self.title = title
        self.curr_price = curr_price
        self.prev_price = prev_price
        self.link = link

    def expelliarmus(self):
        print('\ttitle : ' + self.title + '\n')
        print('\tcurrent price : ' +str(self.curr_price) + '\n')
        print('\tprevious price : ' + str(self.prev_price) + '\n')
        print('\tlink : ' + self.link + '\n')

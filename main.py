from ebooklib import epub
import scraper
import re

book = epub.read_epub('C:\\Users\\supernauth\\py_project\\molyolo\\120-haiku.epub')

class HalfBook:
    """
    It is assumed, that the book doesn't have all
    the metadatas.
    """
    def __init__(self):
        pass
    
    def book_input(self):
        # The absolute path must be given
        book_loc = input('Add meg a könyv helyzetét a gépen: ')
        book_loc_fixed = re.sub('\\', '\\\\', book_loc)
        book = epub.read_epub(book_loc_fixed)
        return book
        

    def checker(book):
        # to check the current or new metadatas, if needed
        metadatas = ['title', 'creator', 'publisher', 'description']

        initial_data = []
        
        for datas in metadatas:
            try:
                attribute = (book.get_metadata('DC', datas))[0][0]
                if attribute == None:
                    initial_data.append((f"\t{datas} is None"))
                else:
                    initial_data.append(attribute)
            except IndexError:
                initial_data.append(f"\t{datas} is empty")
        
        return initial_data
            

if __name__ == '__main__':
    new_book = HalfBook()
    new_book.book_input()
    moly_link = input('Add meg a könyv molyos linkjét: ')
    scraped_book = scraper.Reader(moly_link)
    title = scraped_book.get_title()
    author = scraped_book.get_author()
    publisher = scraped_book.get_publisher()
    blurb = scraped_book.get_blurb()
    
    # print(title + "\n" + author + "\n" + publisher + "\n" + blurb)
    
    book.set_title(title)
    book.add_author(author)
    book.add_metadata('DC', 'publisher', publisher)
    book.add_metadata('DC', 'description', blurb)
    
    new_filename = input('Add meg az új könyv fájlnevét: ')
    epub.write_epub(new_filename, book)
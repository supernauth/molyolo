from bs4 import BeautifulSoup
import requests as req
import re


class Reader:
    def __init__(self, url):
        self.url = url
        self.resp = req.get(self.url)
        self.soup = BeautifulSoup(self.resp.text, 'html.parser')

    def get_title(self):
        title = self.soup.find_all('span', class_='item')
        title_str = ''
        for element in title:
            title_str += str(element)

        title_final = re.sub(r'<.*?>', '', title_str)
        return title_final
    
    def get_author(self):
        author = self.soup.find_all('div', class_='authors')
        author_str = ''
        for element in author:
            author_str += str(element)

        # the referred div part is too long to use re
        author_a_tag = (author_str)[46:]
        author_final = re.sub(r'<.*?>', '', author_a_tag)
        return author_final
    
    def get_publisher(self):
        publisher = self.soup.find_all('a')

        # the publisher's a tag does not have class/id, found with the href text
        links = []
        for link in publisher:
            if (link.get('href')).startswith('/kiadok/'):
                links.append(link)
            else:
                pass

        # more publishing date, but using the last one, deleting the HTML-part
        last_publisher = str(links[0])
        start = last_publisher.find('>')
        ending = last_publisher.find('</')

        publisher_final = last_publisher[start + 1:ending]
        return publisher_final
    
    def get_blurb(self):
        # finding the blurb, making it string without HTML tags using re
        blurb = self.soup.find_all('div', class_='text')

        blurb_str = ''
        for element in blurb:
            blurb_str += str(element)
        blurb_final = re.sub(r'<.*?>', '', blurb_str)
        return blurb_final

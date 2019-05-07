from bs4 import BeautifulSoup as bs
import newspaper
import re
import requests
from urllib.parse import urlparse
from urllib.parse import urlsplit


class PageAnalyser():   #coded by haks
    data_structure = []

    def __init__(self, url):
        # requests.get only works with urls with http or https
        # so the url needs to have http or https in it
        if re.match(r"(https://|http://).+", url):
            self.url = url
        else:
            self.url = "http://{}".format(url)

    def get_page_content(self, url=None): #downloads the content of a url passed into it . Coded by @Edeediong
        if url is None:
            url = self.url 
        try:
            # Some sites do not allow requests without headers
            # The headers dictionary deals with this
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}            
            page_object = requests.get(url, headers=headers)
            page_content = page_object.content
            parsed_page_content = bs(page_content, "html.parser",from_encoding="iso-8859-1")
            return parsed_page_content
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
            print("Error: Something is wrong with the url")


    def get_all_links_and_anchor_texts(self, page_content): #fetches both external and internal links  as well as the anchor . Coded by @Munirat
        anchor_tags = page_content.find_all("a")
        links = []
        anchor_text = []
        for anchor_tag in anchor_tags:
            # Some anchor tags do not have href attributes
            # Use an empty string as the href value of such tags
            try:
                links.append(anchor_tag["href"])
            except KeyError:
                links.append("")
            anchor_text.append(anchor_tag.text.strip())
        links_and_anchor_texts = list(zip(links, anchor_text))
        return links_and_anchor_texts

    def get_link_one_level_down(self, link): #get's 1st level links eg hotels.ng/about  . Coded by @Munirat
        scheme = urlsplit(link).scheme
        netloc = urlsplit(link).netloc
        if((scheme == '') | (netloc == '')):
            return link
        base_url='://'.join([urlsplit(link).scheme,urlsplit(link).netloc])
        path=urlsplit(link).path
        path=path.split('/')
        one_level = [base_url, path[1]]
        return '/'.join(one_level)

    def get_internal_links_and_anchor_texts(self, links_and_anchor_texts): #gets the internal links and the anchor texts . Coded by @Jesse Amamgbu
        link_text_mapping = {}
        domain_name = urlparse(self.url).netloc

        for link, anchor_text in links_and_anchor_texts:
            link_domain_name = urlparse(link).netloc

            try:
                if (link_domain_name == domain_name):
                    link_one_level_deep = self.get_link_one_level_down(link)
                    link_text_mapping.setdefault(link_one_level_deep,[]).append(anchor_text)
                
                elif re.match(r"^(/.*)", link):
                    full_link = "{}{}".format(domain_name, link)                                       
                    link_one_level_deep = self.get_link_one_level_down(full_link)
                    link_text_mapping.setdefault(link_one_level_deep,[]).append(anchor_text)

            except IndexError:
                continue
        return link_text_mapping

    def get_meta_data(self, link_text_mapping): #loops through each internal link to return the h1, keyword, sumarry and short url. Coded by @Nnamdi
        meta_data = []
        for link, anchor_text in link_text_mapping.items():
            # requests.get only works with urls with http or https
            # so the url needs to have http or https in it
            if not re.match(r"(https://|http://).+", link):
                link = "http://{}".format(link)
            try:
                article = newspaper.Article("")
                page_content = self.get_page_content(link)
                article.set_html(str(page_content))
                article.parse()
                article.nlp()
                keywords = article.keywords
                summary = article.summary
                h1=[h1_tag.get_text() for h1_tag in page_content.find_all("h1")]
                short_url = link.split("/")[-1]
                meta_data.append((link, h1, keywords, short_url, anchor_text, summary))
            except newspaper.article.ArticleException:
                continue

        return meta_data

    def get_data_structure(self, meta_data): #gets the output to  display in a nested dictionary that will be easily transformed to Json. Coded by @Haks
        domain_name = urlparse(self.url).netloc
        data_structure = {domain_name:{}}
        for page_data in meta_data:
            url = page_data[0]
            h1 = page_data[1]
            keywords = page_data[2]
            short_url = page_data[3] if len(page_data[3]) > 0 else "home"
            anchor_tags = page_data[4]
            summary = page_data[5]
            page_structure = {
            "url": url,
            "h1": h1,
            "keywords": keywords,
            "short_url": short_url,
            "anchor_tags": anchor_tags,
            "summary": summary
            }
            data_structure[domain_name].setdefault(short_url,[]).append(page_structure)
        PageAnalyser.data_structure.append(data_structure)
        return data_structure
        
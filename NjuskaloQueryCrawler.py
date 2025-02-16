from bs4 import BeautifulSoup
import json
import time
import os
import random
import re

class NjuskaloQueryCrawler():
    #The blacklisted links which should be skipped
    blacklistedLinks = {'/luksuzne-nekretnine'}
    #Gets a list of all possible entities on the page. An entity is an entry to the njuskalo website.
    def _getPossibleEntities(self, soup):
        regularEntityList = soup.find('div', class_='EntityList--ListItemRegularAd')
        vauVauEntityList = soup.find('div', class_='EntityList--VauVau')
        entities = []
        if (regularEntityList != None):
            entities = regularEntityList.find_all('li', class_='EntityList-item')
        if (vauVauEntityList != None):
            entities.extend(vauVauEntityList.find_all('li', class_='EntityList-item'))
        return entities
    

    #Inserts a possible entity into parsed items which will be exported to the json
    def _crawlEntity(self, parsed_items, entity):
        if (entity.find('article', class_='entity-body') == None):
            return
        
        #Prep of entity description for easier parsing
        description_str_raw = entity.find('div', class_='entity-description-main').text
        living_area_str = re.search(r'(\d+(\.\d+)?)\s* m2', description_str_raw)
        location_str = re.search(r'Lokacija:\s*(.*)', description_str_raw)

        name_data = entity.find('a')

        name_str = name_data.text
        link_str = name_data['href']
        # location_str = entity.find('div', class_='entity-description-main').text
        published_str = entity.find('time').text
        price_str = entity.find('strong', class_='price--hrk').text

        print("Scraped " + name_str)

        parsed_items.append({
                            'name' : name_str.strip(),
                            'location' : location_str.group(1),
                            'Living Area': living_area_str.group(0),
                            'published' : published_str,
                            'price' : price_str.strip(),
                            'link' : link_str
                    })
    #Write a category into a file on disk
    def _crawlCategoryLink(self, category_href, page, out_folder, page_limit):
        page.goto('https://www.njuskalo.hr' + category_href)

        currentPage = 1
        parsed_items_from_category = []
        charsToRemoveFromFilename='/?'
        charsToRemoveFromFilenameRegex = f'[{re.escape(charsToRemoveFromFilename)}]'
        while (True):
            html_from_page = page.content()
            soup = BeautifulSoup(html_from_page, 'html.parser')
            entities = self._getPossibleEntities(soup)

            file = open(os.path.join(out_folder, re.sub(charsToRemoveFromFilenameRegex, '', category_href) + '.json'), 'w', encoding='utf-8')
                
            for entity in entities:
                self._crawlEntity(parsed_items_from_category, entity)

            parsed_items_string_json = json.dumps(parsed_items_from_category, ensure_ascii=False, indent=2)
            file.write(parsed_items_string_json)

            print('Parsed page: '+ str(currentPage))


            currentPage = currentPage + 1
            nextPageLink = self._getNextPageLink(soup)
            shouldConsiderPageLimit = page_limit != None
            if ((nextPageLink == None) or (shouldConsiderPageLimit and (page_limit == (currentPage - 1)))):
                file.close()
                break
            else:
                #sleep to give it a bit of human behavior
                time.sleep(random.uniform(0.05, 0.25))

                page.goto(nextPageLink)

    #The crawling mechanism for user picked categories:
    def crawlSelectedCategory(self, page, options):
        page.goto('https://www.njuskalo.hr')

        time.sleep(random.uniform(3,4.5))

        self._crawlCategoryLink(options.categoryHref, page, options.outFolder, options.pageLimit)

    #The crawling mechanism
    def crawlSelectedTab(self, page, options):
        # Navigate to the URL.
        page.goto(options.tab)

        time.sleep(random.uniform(3,4.5))

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        categories = soup.find_all('li', class_='Category')

        categories.extend(soup.find_all('div', class_='Category'))

        links_to_crawl = []
        for category in categories:
            category_links = category.find_all('a')
            links_to_crawl.extend(category_links)

        for link in links_to_crawl:
            category_href = link['href']
            if (category_href in self.blacklistedLinks):
                print('Skipping: ' + category_href +'. Blacklisted.')
                continue
            print(category_href)

            self._crawlCategoryLink(category_href, page, options.outFolder, options.pageLimit)

    #If there is no page after this, returns None
    def _getNextPageLink(self, soup):
        try:
            pagination_html = soup.find('ul', class_='Pagination-items')
            nextButtonSpan = pagination_html.find('span', text='»')
            if (nextButtonSpan == None):
                return None
            else:
                try:
                    return nextButtonSpan.parent['data-href']
                except:
                    return nextButtonSpan.parent['href']
        except:
            return None
        

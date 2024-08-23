
from NjuskaloCrawler import NjuskaloCrawler
from CrawlingOptions import CustomCategoryCrawlingOptions, TabCrawlingOptions
from NjuskaloTab import NjuskaloTab
from enum import Enum

splash_message = """
****************************************************
*                                                  *
*           Welcome to Njuškalo Crawler!           *
*                                                  *
* This tool allows you to scrape and analyze data  *
* from the popular Croatian classifieds website    *
* Njuškalo. Whether you're looking for the best    *
* real estate deals, the latest tech gadgets, or   *
* just curious about market trends, this crawler   *
* has you covered.                                 *
*                                                  *
* Please ensure you have the necessary permissions *
* to scrape data and respect the website's         *
* terms of service.                                *
*                                                  *
* Happy Crawling!                                  *
*                                                  *
***************************************************


"""

class TerminalEngine:
    def _runWholeTab(self):
        print("Pick a tab to crawl: 1 = Marketplace, 2 = AutoMoto, Anything else = Nekretnine")
        choice = input()
        tab_option = None
        if (choice == '1'):
            tab_option = NjuskaloTab.Marketplace
        elif (choice == '2'):
            tab_option = NjuskaloTab.AutoMoto
        else:
            tab_option = NjuskaloTab.Nekretnine

        print("Do you want a limit on the pages scraped? If you do enter the amount of pages, if not enter 0 or something which isn't a digit")

        choice = input()

        page_num_option = None
        if (choice != '0' and choice.isdigit()):
            page_num_option = choice
        
        print("Enter the directory to save, like: C:\\Folder\\Where\\You\\Want\\Data")

        data_folder = input()

        options = TabCrawlingOptions(tab_option, data_folder, int(page_num_option))
        crawler = NjuskaloCrawler()
        crawler.crawlTab(options = options)
    def _runCustomCategory(self):
        print("Pick a category link to crawl: '/prodaja-kuca', '/prodaja-kuca/istra', etc...")
        print("This is basically everyhing after www.njuskalo.hr in the link in chrome")

        category_href = input()

        print("Do you want a limit on the pages scraped? If you do enter the amount of pages, if not enter 0 or something which isn't a digit")

        choice = input()

        page_num_option = None
        if (choice != '0' and choice.isdigit()):
            page_num_option = int(choice)
        
        print("Enter the directory to save, like: C:\\Folder\\Where\\You\\Want\\Data")

        data_folder = input()

        options = CustomCategoryCrawlingOptions(category_href, data_folder, page_num_option)
        crawler = NjuskaloCrawler()
        crawler.crawlCustomCategory(options = options)

    def runCoreLoop(self):
        print(splash_message)
        while True:
            print("Would you like to scrape one of the main tabs in njuskalo (Nekretnine, Auto-Moto or Marketplace) or a custom category?")
            print("\nCustom category = 1 | Whole Tab = 2 | Quit = Anything Else")

            choice = input()
            if (choice == '1'):
                self._runCustomCategory()
            elif (choice == '2'):
                self._runWholeTab()
            else:
                break

            print ("Crawling complete!")
        print('Hope you like this tool! Please leave a star on github if you did :)!')
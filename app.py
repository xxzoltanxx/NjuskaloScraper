from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import TabCrawler
from NjuskaloTab import NjuskaloTab
from enum import Enum
import os

class NjuskaloCrawler():

    def _get_hyperlink_for_tab(self, tab):
        if (tab == NjuskaloTab.Marketplace):
            return 'https://www.njuskalo.hr/marketplace'
        elif (tab == NjuskaloTab.AutoMoto):
            return 'https://www.njuskalo.hr/auto-moto'
        elif (tab == NjuskaloTab.Nekretnine):
            return 'https://www.njuskalo.hr/nekretnine'
        else:
            return ''

    def crawlTab(self, tab, output_directory):
        with sync_playwright() as playwright_launcher:
            self._browser = playwright_launcher.chromium.launch_persistent_context(user_data_dir='', channel='chrome', headless=False, args=['--start-maximized'], no_viewport=True)
            self._page = self._browser.new_page()

            #Apply playwright stealth masking to page
            stealth_sync(self._page)
            tab_crawler = TabCrawler.TabCrawler()
            tab_crawler.crawlSelectedTab(self._page, output_directory, self._get_hyperlink_for_tab(tab))


    def crawlCustomCategory(self, categoryHref, output_directory):
        with sync_playwright() as playwright_launcher:
            self._browser = playwright_launcher.chromium.launch_persistent_context(user_data_dir='', channel='chrome', headless=False, args=['--start-maximized'], no_viewport=True)
            self._page = self._browser.new_page()

            #Apply playwright stealth masking to page
            stealth_sync(self._page)
            tab_crawler = TabCrawler.TabCrawler()
            tab_crawler.crawlSelectedCategory(self._page, output_directory, categoryHref)


if __name__ == "__main__":
    njuskalo_crawler = NjuskaloCrawler()
    #njuskalo_crawler.crawlTab(NjuskaloTab.Marketplace, os.getcwd())
    njuskalo_crawler.crawlCustomCategory('/prodaja-stanova/zagrebacka', os.getcwd())

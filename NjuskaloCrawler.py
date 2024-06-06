from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import NjuskaloQueryCrawler
from NjuskaloTab import NjuskaloTab
from enum import Enum
from CrawlingOptions import *
import os
import time
import random
    
"""
Scraper for https://www.njuskalo.hr/.
Can crawl one of the tabs and store everything inside a directory, or crawl a custom category url(http:)
"""

class NjuskaloCrawler():

    #Clicks on all popups which occur in a browser with an empty history
    #visiting njuskalo.hr
    def _initializeStartClicks(self, page):
        page.goto('https://www.njuskalo.hr')
        time.sleep(random.uniform(1.5,2.5))
        try:
            page.click("#didomi-notice-agree-button", timeout = random.uniform(0.5,1.5) * 1000)
        except:
            print("Cookie policy accept button not found")
        time.sleep(random.uniform(1.5,2.5))
        try:
            page.locator('.button-standard .button-standard--alpha .bp-radix__button-standard--full .PrivacyPolicyNotice-close .PrivacyPolicyNotice-close--asButton').click(timeout = random.uniform(0.5,1.5) * 1000)
        except:
            print("Privacy notice button not found.")

    #crawls whole tabs (Nekretnice, Marketplace, Auto Moto Nautika)
    #options are TabCrawlingOptions
    def crawlTab(self, options):
        with sync_playwright() as playwright_launcher:
            self._browser = playwright_launcher.chromium.launch_persistent_context(user_data_dir='', channel='chrome', headless=False, args=['--start-maximized'], no_viewport=True)
            self._page = self._browser.new_page()

            #Apply playwright stealth masking to page
            stealth_sync(self._page)
            tab_crawler = NjuskaloQueryCrawler.NjuskaloQueryCrawler()
            self._initializeStartClicks(self._page)
            tab_crawler.crawlSelectedTab(self._page, options)

    #crawls a customHref (like '/od-glave-do-pete')
    #options are CustomCategoryCrawlingOptions
    def crawlCustomCategory(self, options):
        with sync_playwright() as playwright_launcher:
            self._browser = playwright_launcher.chromium.launch_persistent_context(user_data_dir='', channel='chrome', headless=False, args=['--start-maximized'], no_viewport=True)
            self._page = self._browser.new_page()

            #Apply playwright stealth masking to page
            stealth_sync(self._page)
            tab_crawler = NjuskaloQueryCrawler.NjuskaloQueryCrawler()
            self._initializeStartClicks(self._page)
            tab_crawler.crawlSelectedCategory(self._page, options)

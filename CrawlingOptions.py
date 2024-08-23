from enum import Enum;
from NjuskaloTab import NjuskaloTab
import os

class CustomCategoryCrawlingOptions:
    #categoryHref example: '/prodaja-kuca'
    #pageLimit - the limit on the pages that are crawled
    #outFolder - the directory where you want the data saved
    def __init__(self, categoryHref, outFolder, pageLimit = None):
        self.categoryHref = categoryHref
        self.pageLimit = pageLimit
        self.outFolder = outFolder

class TabCrawlingOptions:
    #tab: NjuskaloTab.AutoMoto, NjuskaloTab.Nekretnine, NjuskaloTab.Marketplace 
    #pageLimit - the limit on the pages that are crawled
    #outFolder - the directory where you want the data saved
    def __init__(self, tab, outFolder, pageLimit = None):
        self.tab = get_hyperlink_for_tab(tab)
        self.pageLimit = pageLimit
        self.outFolder = outFolder + "\\\\"

def get_hyperlink_for_tab(tab):
    if (tab == NjuskaloTab.Marketplace):
        return 'https://www.njuskalo.hr/marketplace'
    elif (tab == NjuskaloTab.AutoMoto):
        return 'https://www.njuskalo.hr/auto-moto'
    elif (tab == NjuskaloTab.Nekretnine):
        return 'https://www.njuskalo.hr/nekretnine'
    else:
        return ''
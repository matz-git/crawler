from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SpreadShirtBot():


    def __init__(self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)


    def closeBrowser(self):
        self.browser.close()


    def __exit__(self):
        self.closeBrowser()


    def getSite(self, url, keywords):
        self.browser.get('https://www.' + url + '/' + keywords)


    def get_tags(self):
        
        time.sleep(4)
        
        # get all article links on first page
        links = self.browser.find_elements_by_xpath("//a[@class='article thumb-font']")

        arr = []

        print(len(links))
        # print(type(links))

        for x in range(len(links)):
            arr.append(links[x].get_attribute("href"))
        else:
            print("Finally finished!")
       
        print(arr)

        tag_list = []

        iteration = 1
        sleepTimeSeconds = 2

        for element in arr:
            
            time.sleep(sleepTimeSeconds)
            self.browser.get(element)

            tags = self.browser.find_element_by_xpath("//div[@class='designer-info__tags small-font']/descendant::span[2]").get_attribute("innerHTML")
            tag_list = tag_list + [x.strip() for x in tags.split(',')]

            print(f"durchgang nr: {iteration}/{len(links)}")

            time.sleep(sleepTimeSeconds)

            iteration += 1

        print(tag_list)

        d = {}
        for item in tag_list:
            if item in d:
                d[item] = d.get(item)+1
            else:
                d[item] = 1

        final_arr = (sorted(d.items(), key =  lambda kv:(kv[1], kv[0])))     

        for key in final_arr:
            print(key)


bot = SpreadShirtBot()
bot.getSite('spreadshirt.de', 'search+term+etc')
bot.get_tags()
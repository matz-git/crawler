import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
import time, urllib.request


class InstagramBot():

    
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.email = email
        self.password = password


    def getSite(self, username):

        self.browser.get('https://www.instagram.com/' + username)

        time.sleep(8)

        posts = self.browser.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(1) > span > span").text
        print('Posts: ' + str(posts))
      
        followers = self.browser.find_elements_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span")[0].text
        print('Followers: ' + str(followers))

        followings = self.browser.find_elements_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > span")[0].text
        print('Followings: ' + str(followings))


    def get_images(self):
        scrolldown = self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        match=False
        while(match==False):
            last_count = scrolldown
            time.sleep(3)
            scrolldown = self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
            if last_count==scrolldown:
                match=True

        posts = []
        links = self.browser.find_elements_by_tag_name('a')
        for link in links:
            post = link.get_attribute('href')
            if '/p/' in post:
                posts.append(post)

        with open('posts.json', 'w') as outfile:
            json.dump(posts, outfile)

        print(posts)

        download_url = ''
        for post in posts:	
            self.browser.get(post)
            shortcode = self.browser.current_url.split("/")[-2]
            time.sleep(7)

            # carussel
            if self.browser.find_element_by_css_selector("img[style='object-fit: cover;']") is not None:
                
                def check_exists_by_class_name(name):
                    try:
                        self.browser.find_element_by_class_name(name)
                    except NoSuchElementException:
                        return False
                    return True

                def check_exists_by_tag_name(name):
                    try:
                        self.browser.find_element_by_tag_name(name)
                    except NoSuchElementException:
                        return False
                    return True

                if check_exists_by_class_name('coreSpriteRightChevron  '):
                    i = 0
                    j = 0

                    while(check_exists_by_class_name('coreSpriteRightChevron  ')):
                        time.sleep(3)

                        download_url = ''
                        shortcode = ''
                        shortcode = self.browser.current_url.split("/")[-2] + str(j)
                        img_url = self.browser.find_elements_by_class_name('KL4Bh')[i].find_element_by_tag_name('img').get_attribute('src')
                        
                        print("____________")
                        print(len(self.browser.find_elements_by_class_name('KL4Bh')))
                        
                        print("____________")
                        download_url_arr = self.browser.find_elements_by_css_selector("img[style='object-fit: cover;']")
                        download_url = download_url_arr[i].get_attribute('src')
                        
                        urllib.request.urlretrieve( img_url, '{}.jpg'.format(shortcode))
                        if i == 1:
                            i = 1
                        else:
                            i = i + 1
                        time.sleep(2)
                        next_button = self.browser.find_element_by_class_name('coreSpriteRightChevron  ')
                        next_button.click()
                        j = j + 1

                        time.sleep(2)

                    # the Last element (has no coreSpriteRightChevron):
                    download_url = ''

                    shortcode = shortcode + str(j)

                    download_url = self.browser.find_elements_by_class_name('KL4Bh')[1].find_element_by_tag_name('img').get_attribute('src')

                    urllib.request.urlretrieve( download_url, '{}.jpg'.format(shortcode))

                else:
                    if check_exists_by_tag_name('video'):
                        download_url = self.browser.find_element_by_css_selector("video[type='video/mp4']").get_attribute('src')
                        urllib.request.urlretrieve( download_url, '{}.mp4'.format(shortcode))
                    else:
                        download_url = self.browser.find_element_by_css_selector("img[style='object-fit: cover;']").get_attribute('src')
                        urllib.request.urlretrieve( download_url, '{}.jpg'.format(shortcode))

            else:
                download_url = self.browser.find_element_by_css_selector("video[type='video/mp4']").get_attribute('src')
                urllib.request.urlretrieve( download_url, '{}.mp4'.format(shortcode))
            
            time.sleep(5)


    def signIn(self):
        self.browser.get('https://www.instagram.com')

        time.sleep(2)

        emailInput = self.browser.find_element_by_css_selector('input[name="username"]')
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(2)
        
        notificationButton = self.browser.find_element_by_class_name('HoLwm')
        notificationButton.click()

        time.sleep(4)


    def closeBrowser(self):
        self.browser.close()


    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


bot = InstagramBot('name', 'password')
bot.signIn
bot.getSite('username')
bot.get_images()
bot.closeBrowser()
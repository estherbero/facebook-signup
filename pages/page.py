from selenium import webdriver
import random
import string

class Page:
    
    ## open browser
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        self.browser = webdriver.Chrome(chrome_options=chrome_options)  
    
    def open (self, url):
        self.browser.get(url)

    def close(self):
        self.browser.close()
    
    # def wait_for_page_title(self, title, timeout):
    #   WebDriverWait(self.driver, timeout).until(EC.title_is(title))

    def find_id(self, selector):
      return self.browser.find_element_by_id(selector)

    def find_xpath(self, selector):
      return self.browser.find_element_by_xpath(selector)

    def insert_data_in(self, selector, text):
      self.find_id(selector).send_keys(text)

    def click(self, selector):
      self.find_id(selector).click()
    
    def select_gender(self):
      attempt = 1
      while(attempt < 4):
        try:
          self.click('u_0_9')
          break
        except:
          print('Attempt select gender: ' + attempt + ' failed. Trying again...')
          attempt += 1
      if (attempt > 3):
        raise 'Failed to select gender.'

    def generate_name(self, length):
        VOWELS = "aeiou"
        CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
        word = ""
        for i in range(length):
            if i % 2 == 0:
                word += random.choice(CONSONANTS)
            else:
                word += random.choice(VOWELS)
        return word
import unittest
import random
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page import Page


class Registration(unittest.TestCase):

    ## start an instance of Chrome with selenium-webdriver
    ## open the Url
    @classmethod
    def setUpClass(self):
        self.page = Page()
        print ('---SCENARIO: HAPPY PATH-REGISTRATION---')    
        self.page.open('https://www.facebook.com/')

    ## close browser when finished
    @classmethod
    def tearDownClass(self):
        self.page.close()

    def test_register(self):
        ## Generate Random names/surnames/DoB
        print ('RANDOM DATA GENERATION')
        name_str = self.page.generate_name(random.randint(6,8))
        print ('name=' + name_str)
        surname_str = self.page.generate_name(random.randint(4,8))
        print ('surname=' + surname_str)
        email_data = name_str + str(random.randint(1,9))
        print ('email=' + email_data)
        password_data = surname_str + str(random.randint(1,9))
        print ('password=' + password_data)
        day_num = random.randint(1,28)
        print ('DoB=' + str(day_num))
        year_num = random.randint(1970,1995)
        print ('YoB=' + str(year_num))

        ## Create an account--fill the fields
        print ('---REGISTER FORM---')
        print ('START FILLING')

        ## Name
        name = self.page.insert_data_in('u_0_j', name_str)
        ## Surname
        surname = self.page.insert_data_in('u_0_l',surname_str)
        ## Mail address or Mobile number
        email = self.page.insert_data_in('u_0_o', email_data + '@hotmail.com')
        ## Re-enter mail address
        reemail = self.page.insert_data_in('u_0_r', email_data + '@hotmail.com')
        ## Password
        password = self.page.insert_data_in('u_0_v', password_data)
        ## DoB
        day = self.page.insert_data_in('day',day_num)
        year = self.page.insert_data_in('year',year_num)
        ## Select Gender RadioButton/checkbox

        attempt = 1
        while(attempt < 4):
            try:
                self.page.click('u_0_9')
                break
            except:
                print('Attempt select gender: ' + attempt + ' failed. Trying again...')
            attempt += 1
        if (attempt > 3):
            raise 'Failed to select gender.'

        ## Sign Up button
        signup = self.page.click('u_0_11')
        print ('END FILLING')

        WebDriverWait(self.page.browser, 5).until(EC.title_is('Facebook'))
        # assert: next page loaded, name identified
        print ('---END TEST---')
        print ('---TEST CASE RESOLUTION---')
        # Force to "Failed" first changing the 'name_str' to another string for instance
        # Ideally we should use ID selector or custom ID's for testing attribute in order to make our test suite steady and robust
        #assert self.browser.find_element_by_xpath('//*[@id="bluebar_profile_and_home"]/div[1]/div/a/span/span').text.lower() == name_str, "KO, not correctly registered"
        assert self.page.browser.find_element_by_class_name('_1vp5').text.lower() == name_str, "KO, not correctly registered"

if __name__ == "__main__":
    unittest.main()


import unittest
import random
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.page import Page


class FBRegistration(unittest.TestCase):

    ## start an instance of Chrome with selenium-webdriver
    ## open the Url
    # We could use a setUpClass and a tearDownClass for instancing Page and open and close driver
    # but we do want to have a fresh browser instance per test to make sure registration has a clean start
    def setUp(self):
        self.page = Page()   
        self.page.open('https://www.facebook.com/')

    ## close browser when finished
    def tearDown(self):
      self.page.close()

    def test_register(self):
        print ('---SCENARIO: HAPPY PATH-REGISTRATION---') 
        ## Generate Random names/surnames/DoB
        print ('RANDOM DATA GENERATION')
        name_str = self.page.generate_name(random.randint(6,8))
        surname_str = self.page.generate_name(random.randint(4,8))
        email_data = name_str + str(random.randint(1,9))
        password_data = surname_str + str(random.randint(1,9))
        day_num = random.randint(1,28)
        year_num = random.randint(1970,1995)

        ## Create an account--fill the fields
        print ('---REGISTER FORM---')
        print ('START FILLING')

        ## Name
        self.page.insert_data_in('u_0_j', name_str)
        ## Surname
        self.page.insert_data_in('u_0_l',surname_str)
        ## Mail address or Mobile number
        self.page.insert_data_in('u_0_o', email_data + '@hotmail.com')
        ## Re-enter mail address
        self.page.insert_data_in('u_0_r', email_data + '@hotmail.com')
        ## Password
        self.page.insert_data_in('u_0_v', password_data)
        ## DoB
        self.page.insert_data_in('day',day_num)
        self.page.insert_data_in('year',year_num)

        ## Select Gender RadioButton/checkbox
        self.page.select_gender()

        ## Sign Up button
        signup = self.page.click('u_0_11')
        print ('END FILLING')

        WebDriverWait(self.page.browser, 5).until(EC.title_is('Facebook'))
        # assert: next page loaded, name identified
        print ('---END TEST---')
        print ('---TEST CASE RESOLUTION---')
        assert self.page.browser.find_element_by_class_name('_1vp5').text.lower() == name_str, "KO, not correctly registered"
        # For a full sign up, we would need to verify email. This is doable by checking inbox and validating the code with different approachs like, 
        # e.g. https://medium.com/appgambit/email-verification-with-selenium-a5117cb1a9c1 
        # Since Facebook has some protection agaisnt fake accounts, we cannot use a generic email like "testing+HereRandomData@gmail.com" because 
        # it is detected as same as "testing@gmail.com", so we will need a dynamic email generator, which will be much out of the scope of this test.

    def test_under_age(self):
        print ('---SCENARIO: NO HAPPY PATH EXAMPLE---') 
        ## Generate Random names/surnames/DoB
        # We can module this part as long as it can be the same for a test suite, we keep this way to make it more flexible to add "bad" data at any point
        print ('RANDOM DATA GENERATION')
        name_str = self.page.generate_name(random.randint(6,8))
        surname_str = self.page.generate_name(random.randint(4,8))
        email_data = name_str + str(random.randint(1,9))
        password_data = surname_str + str(random.randint(1,9))
        day_num = random.randint(1,28)
        year_num = random.randint(2009,2018)

        ## Create an account--fill the fields
        print ('---REGISTER FORM---')
        print ('START FILLING')

        # We can make move this to a function as well, but we are also interested not filling all the gaps to check we get the proper error message
        ## Name
        self.page.insert_data_in('u_0_j', name_str)
        ## Surname
        self.page.insert_data_in('u_0_l',surname_str)
        ## Mail address or Mobile number
        self.page.insert_data_in('u_0_o', email_data + '@hotmail.com')
        ## Re-enter mail address
        self.page.insert_data_in('u_0_r', email_data + '@hotmail.com')
        ## Password
        self.page.insert_data_in('u_0_v', password_data)
        ## DoB
        self.page.insert_data_in('day',day_num)
        self.page.insert_data_in('year',year_num)

        ## Select Gender RadioButton/checkbox
        self.page.select_gender()

        ## Sign Up button
        signup = self.page.click('u_0_11')
        print ('END FILLING')

        # Ideally we should use ID like we are using in all other selectors or custom QA id to make our test suite robust and steady
        # This is an example of Xpath use, which is not recommended. We just want an example here.
        error_msg_selector = '/html/body/div[1]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/form/div/div'
        error_msg = "Sorry, we are not able to process your registration."
        
        WebDriverWait(self.page.browser, 10).until(EC.text_to_be_present_in_element((By.XPATH, error_msg_selector), error_msg))

if __name__ == "__main__":
    unittest.main()
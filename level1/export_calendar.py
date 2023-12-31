# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestDefaultSuite():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_getcalendarURL(self):
    self.driver.get("https://sandbox.moodledemo.net/my//my/")
    self.driver.set_window_size(826, 824)
    self.driver.execute_script("window.scrollTo(0,663.2000122070312)")
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[4]/div/div[2]/div/section/div/aside/section[2]/div/div/div[2]/div/span[2]/a").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form/button").click()
    self.driver.find_element(By.ID, "id_events_exportevents_all").click()
    self.driver.find_element(By.ID, "id_generateurl").click()
    self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
    self.driver.find_element(By.ID, "id_generateurl").click()
    self.driver.find_element(By.ID, "copyexporturl").click()
  
  def test_export(self):
    self.driver.get("https://sandbox.moodledemo.net/my/")
    self.driver.set_window_size(831, 824)
    self.driver.find_element(By.LINK_TEXT, "Import or export calendars").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form/button").click()
    self.driver.find_element(By.ID, "id_events_exportevents_all").click()
    self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
    self.driver.find_element(By.ID, "id_export").click()
  
  def test_exportnotchooseevent(self):
    self.driver.get("https://sandbox.moodledemo.net/my/")
    self.driver.set_window_size(826, 824)
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[4]/div/div[2]/div/section/div/aside/section[2]/div/div/div[2]/div/span[2]/a").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form/button").click()
    self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
    self.driver.find_element(By.ID, "id_export").click()
  
  def test_exportnotchoosetimeperiod(self):
    self.driver.get("https://sandbox.moodledemo.net/my/")
    self.driver.set_window_size(831, 824)
    self.driver.find_element(By.CSS_SELECTOR, "#inst42 > .card-body").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[4]/div/div[2]/div/section/div/aside/section[2]/div/div/div[2]/div/span[2]/a").click()
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form/button").click()
    self.driver.find_element(By.ID, "id_events_exportevents_all").click()
    self.driver.find_element(By.ID, "id_export").click()
  
  def test_getcalendarURLnotchooseevent(self):
    self.driver.get("https://sandbox.moodledemo.net/my/")
    self.driver.set_window_size(828, 824)
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div/div[2]/div/section/div/aside/section[2]/div/div/div[2]/div/span[2]/a").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form/button").click()
    self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
    self.driver.find_element(By.ID, "id_generateurl").click()
  
  def test_getcalendarURLnotchoosetimeperiod(self):
    self.driver.get("https://sandbox.moodledemo.net/my//")
    self.driver.set_window_size(828, 824)
    self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[4]/div/div[2]/div/section/div/aside/section[2]/div/div/div[2]/div/span[2]/a").click()
    self.driver.find_element(By.XPATH, "//html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form/button").click()
    self.driver.find_element(By.ID, "id_events_exportevents_all").click()
    self.driver.find_element(By.ID, "id_generateurl").click()

    def run(self):
        result = []
        fail_test_name = []

        for test_file in self.test_list:
            self.setup_method()
            self.login_student_account()
            self.navigate_to_assignment_place()
            test = self.test_submit_assignment(self.test_list[test_file])
            result.append(test)
            if not test:
                fail_test_name.append(test_file)
            self.teardown_method(None)

        fail_test_name_str = 'Fail testcase:\n\t' + '\n\t'.join(name for name in fail_test_name) if len(fail_test_name) != 0 else 'Fail testcase: None'
        print(f"""
        \n---------- Test submit assignment result -----------\nCorrect test: {result.count(True)}/{len(result)}\n{fail_test_name_str}\n------------------------------------
        """)
        return fail_test_name_str

    # ... other existing methods ...

# Usage example
if __name__ == "__main__":
    test_list = ["test1", "test2", "test3"]  # Replace with your actual test cases
    test_instance = TestDefaultSuite()
    test_instance.test_list = test_list  # Set the test_list attribute
    result = test_instance.run()
    print(result)

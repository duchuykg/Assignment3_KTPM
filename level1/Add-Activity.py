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
  
  def test_addActivitySuccess(self):
    self.driver.get("https://sandbox.moodledemo.net/my/courses.php/my/courses.php")
    self.driver.set_window_size(520, 816)
    self.driver.find_element(By.CSS_SELECTOR, "#course-info-container-2-4 .multiline").click()
    self.driver.find_element(By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text").click()
    self.driver.execute_script("window.scrollTo(0,300)")
    self.driver.find_element(By.CSS_SELECTOR, "#all-7 .option:nth-child(3) .optionicon").click()
    element = self.driver.find_element(By.LINK_TEXT, "Participants")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.ID, "id_name").click()
    self.driver.find_element(By.ID, "id_name").send_keys("Hellos")
    self.driver.find_element(By.ID, "id_submitbutton2").click()
  
  def test_addActitvityStop(self):
    self.driver.get("https://sandbox.moodledemo.net/my/courses.php")
    self.driver.set_window_size(520, 816)
    self.driver.find_element(By.CSS_SELECTOR, "#course-info-container-2-4 .multiline").click()
    self.driver.find_element(By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text").click()
    self.driver.find_element(By.CSS_SELECTOR, "#all-7 .option:nth-child(10) .optionicon > .icon").click()
    self.driver.execute_script("window.scrollTo(0,200)")
    self.driver.find_element(By.ID, "id_name").click()
    self.driver.find_element(By.ID, "id_name").send_keys("235234254")
    self.driver.find_element(By.ID, "id_mainglossary").click()
    dropdown = self.driver.find_element(By.ID, "id_mainglossary")
    dropdown.find_element(By.XPATH, "//option[. = 'Main glossary']").click()
    self.driver.find_element(By.ID, "collapseElement-1").click()
    self.driver.find_element(By.ID, "id_defaultapproval").click()
    dropdown = self.driver.find_element(By.ID, "id_defaultapproval")
    dropdown.find_element(By.XPATH, "//option[. = 'No']").click()
    self.driver.find_element(By.ID, "id_editalways").click()
    dropdown = self.driver.find_element(By.ID, "id_editalways")
    dropdown.find_element(By.XPATH, "//option[. = 'Yes']").click()
    self.driver.find_element(By.ID, "id_cancel").click()
  
  def test_addActitvityFailName(self):
    self.driver.get("https://sandbox.moodledemo.net/my/courses.php")
    self.driver.set_window_size(520, 816)
    self.driver.find_element(By.CSS_SELECTOR, "#course-info-container-2-4 .multiline").click()
    self.driver.find_element(By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text").click()
    self.driver.find_element(By.CSS_SELECTOR, "#all-7 .option:nth-child(1) .optionicon > .icon").click()
    self.driver.execute_script("window.scrollTo(0,26.399999618530273)")
    self.driver.find_element(By.ID, "id_assignsubmission_file_maxsizebytes").click()
    dropdown = self.driver.find_element(By.ID, "id_assignsubmission_file_maxsizebytes")
    dropdown.find_element(By.XPATH, "//option[. = 'regexp:500\\sKB']").click()
    self.driver.find_element(By.ID, "id_submitbutton2").click()
    self.driver.find_element(By.ID, "id_name").click()
    self.driver.find_element(By.ID, "id_error_name").click()
  def run(self):
        result = []
        fail_test_name = []

        for test_method in dir(self):
            if test_method.startswith("test_"):
                self.setup_method(None)
                getattr(self, test_method)()
                self.teardown_method(None)

                test_result = bool(self.driver.find_elements(By.CSS_SELECTOR, '.toast-message'))
                result.append(test_result)

                if not test_result:
                    fail_test_name.append(test_method)

        fail_test_name_str = 'Fail test cases:\n\t' + \
            '\n\t'.join(name for name in fail_test_name) if len(
                fail_test_name) != 0 else 'Fail test cases: None'
        return f"""
        \n---------- Test result -----------\nCorrect tests: {result.count(True)}/{len(result)}\n{fail_test_name_str}\n------------------------------------
        """
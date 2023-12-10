import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import selenium.common.exceptions as ex


class test_submit_quiz:
    def __init__(self, test_list):
        self.test_list = test_list

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.driver.get("https://sandbox.moodledemo.net/")
        self.driver.set_window_size(974, 1039)

    def teardown_method(self, method):
        self.driver.quit()
    
    def login_student_account(self):
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys("student")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("sandbox")
        self.driver.find_element(By.ID, "loginbtn").click()

    def logout(self):
        self.driver.find_element(By.ID, "user-menu-toggle").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()

    def navigate_to_quiz_place(self):
        wait = WebDriverWait(self.driver, 50)
        wait.until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "My courses"))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div/div/div/div/a/div"))).click()

    def test_submit_quiz(self, test_file):
        wait = WebDriverWait(self.driver, 50)
        status = test_file['status']
        expected = test_file['expected']
        Alternative = test_file['Alternative']
        try:
            if status == 'Normal':
                result = True 
                self.driver.find_element(By.LINK_TEXT, "Quiz 2").click()
                if Alternative == "Cancel":
                    try:
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//form/button"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.ID, "id_cancel"))).click()
                        return True
                    except Exception:
                        return False
                elif Alternative == "Re-do":
                    try:
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//form/button"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.ID, "id_submitbutton"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".r0 > .ml-1"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//form/div/div[2]/input"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[contains(.,\'Return to attempt\')]"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[2]/input"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//form/div/div[2]/input"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[5]/div/div/form/button"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".modal-footer > .btn-primary"))).click()
                        return True
                    except Exception:
                        return False
                
                else:  
                    try:
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//form/button"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.ID, "id_submitbutton"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".r0 > .ml-1"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//form/div/div[2]/input"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[5]/div/div/form/button"))).click()
                        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".modal-footer > .btn-primary"))).click()
                        return True
                    except Exception:
                        return False
            
            elif status == 'Deadline':
                self.driver.find_element(By.LINK_TEXT, "Question 1 (Deadline is over)").click()
                
                try:
                    self.driver.find_element(By.XPATH, "//form/button").click()
                    return False
                except ex.NoSuchElementException:
                    return True

            elif status == 'Exhausted':
                self.driver.find_element(By.LINK_TEXT, "Question 3 (Exhausted Attempts Allowed)").click()
                
                try:
                    self.driver.find_element(By.XPATH, "//form/button").click()
                    return False
                except ex.NoSuchElementException:
                    return True

        except Exception as e:
            print(e)
            if status == 'Exhausted' or status == 'Deadline':
                return True
            return False

    def run(self):
        result = []
        fail_test_name = []

        for test_file in self.test_list:
            self.setup_method()
            self.login_student_account()
            self.navigate_to_quiz_place()
            test = self.test_submit_quiz(self.test_list[test_file])
            result.append(test)
            if not test:
                fail_test_name.append(test_file)
            self.teardown_method(None)

        fail_test_name_str = 'Fail testcase:\n\t' + '\n\t'.join(name for name in fail_test_name) if len(fail_test_name) != 0 else 'Fail testcase: None'
        return f"""
        \n---------- Test submit quiz result -----------\nCorrect test: {result.count(True)}/{len(result)}\n{fail_test_name_str}\n------------------------------------
        """
        return fail_test_name_str

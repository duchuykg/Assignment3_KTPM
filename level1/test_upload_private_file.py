import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

JS_DROP_FILES = "var k=arguments,d=k[0],g=k[1],c=k[2],m=d.ownerDocument||document;for(var e=0;;){var f=d.getBoundingClientRect(),b=f.left+(g||(f.width/2)),a=f.top+(c||(f.height/2)),h=m.elementFromPoint(b,a);if(h&&d.contains(h)){break}if(++e>1){var j=new Error('Element not interactable');j.code=15;throw j}d.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var l=m.createElement('INPUT');l.setAttribute('type','file');l.setAttribute('multiple','');l.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');l.onchange=function(q){l.parentElement.removeChild(l);q.stopPropagation();var r={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:l.files,setData:function u(){},getData:function o(){},clearData:function s(){},setDragImage:function i(){}};if(window.DataTransferItemList){r.items=Object.setPrototypeOf(Array.prototype.map.call(l.files,function(x){return{constructor:DataTransferItem,kind:'file',type:x.type,getAsFile:function v(){return x},getAsString:function y(A){var z=new FileReader();z.onload=function(B){A(B.target.result)};z.readAsText(x)},webkitGetAsEntry:function w(){return{constructor:FileSystemFileEntry,name:x.name,fullPath:'/'+x.name,isFile:true,isDirectory:false,file:function z(A){A(x)}}}}}),{constructor:DataTransferItemList,add:function t(){},clear:function p(){},remove:function n(){}})}['dragenter','dragover','drop'].forEach(function(v){var w=m.createEvent('DragEvent');w.initMouseEvent(v,true,true,m.defaultView,0,0,0,b,a,false,false,false,false,0,null);Object.setPrototypeOf(w,null);w.dataTransfer=r;Object.setPrototypeOf(w,DragEvent.prototype);h.dispatchEvent(w)})};m.documentElement.appendChild(l);l.getBoundingClientRect();return l"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []
    
    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, list) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))
    
    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})

WebElement.drop_files = drop_files


class test_upload_private_file:
    def __init__(self, test_list):
        self.test_list = test_list

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.driver.get("https://sandbox401.moodledemo.net")
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


    def navigate_to_upload_place(self):
        self.driver.find_element(By.ID, "user-menu-toggle").click()
        self.driver.find_element(By.LINK_TEXT, "Private files").click()

    def test_upload_file(self, test_file):
        wait = WebDriverWait(self.driver, 50)
        file_path = os.path.abspath('../test files/' + test_file['filename'])
        upload_type = test_file['upload type']
        expected = test_file['expected']
        create_folder = test_file['create folder']
        folder_name = test_file['folder name']

        try:
            if create_folder:
                # automation for creating folder
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-btn-mkdir"))).click()
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input")))

                if folder_name != '':
                    self.driver.find_element(By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input").send_keys(folder_name)
                    self.driver.find_element(By.CSS_SELECTOR, ".fp-dlg-butcreate").click()
                    wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-file.fp-folder'))).click()
                else:
                    self.driver.find_element(By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input").clear()
                    create_btn = self.driver.find_element(By.CSS_SELECTOR, ".fp-dlg-butcreate")
                    result = "Cannot create folder" if create_btn.value_of_css_property('opacity') == '0.65' else 'Create folder successful'
                    return result == expected
            
            if upload_type == "select":
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-btn-add"))).click()
                wait.until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Upload a file"))).click()
                wait.until(expected_conditions.visibility_of_element_located((By.NAME, "repo_upload_file")))

                self.driver.find_element(By.NAME, "repo_upload_file").send_keys(file_path)
                self.driver.find_element(By.XPATH, "//button[contains(.,'Upload this file')]").click()
                wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, '.fp-file')))
                self.driver.find_element(By.NAME, 'submitbutton').click()
                toast_message = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.toast-message')))

                result = toast_message.text == expected

            elif upload_type == "drag and drop":
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager-container')))
                drop_target = self.driver.find_element(By.CSS_SELECTOR, '.filemanager-container')
                drop_target.drop_files(file_path)

                if "The maximum size you can upload is 100MB." in expected:
                    toast_message = wait.until(expected_conditions.visibility_of_element_located((By.ID, "fp-msg-labelledby"))).text
                    self.driver.find_element(By.CSS_SELECTOR, '.file-picker.fp-msg.fp-msg-error > button').click()

                    return toast_message == expected
                else:
                    wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, '.fp-file')))

                    self.driver.find_element(By.NAME, 'submitbutton').click()
                    toast_message = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.toast-message')))

                    result = toast_message.text == expected

            if create_folder:
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-contextmenu'))).click()
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager.fp-select.fp-folder > form > div:nth-child(1) > button:nth-child(2)'))).click()
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-dlg-butconfirm'))).click()
                self.driver.find_element(By.NAME, 'submitbutton').click()
            else:
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-file'))).click()
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager.fp-select.fp-file > form > div:nth-child(1) > button:nth-child(2)')))
                self.driver.find_element(By.CSS_SELECTOR, '.filemanager.fp-select.fp-file > form > div:nth-child(1) > button:nth-child(2)').click()
                wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-dlg-butconfirm'))).click()
                self.driver.find_element(By.NAME, 'submitbutton').click()

            return result
        except Exception as e:
            print(e)
            return False

    def run(self):
        result = []
        fail_test_name = []

        for test_file in self.test_list:
            self.setup_method()
            self.login_student_account()
            self.navigate_to_upload_place()
            test = self.test_upload_file(self.test_list[test_file])
            result.append(test)
            if not test:
                fail_test_name.append(test_file)
            self.teardown_method(None)

        fail_test_name_str = 'Fail testcase:\n\t' + '\n\t'.join(name for name in fail_test_name) if len(fail_test_name) != 0 else 'Fail testcase: None'
        return f"""
        \n---------- Test upload private file result -----------\nCorrect test: {result.count(True)}/{len(result)}\n{fail_test_name_str}\n------------------------------------
        """
        return fail_test_name_str

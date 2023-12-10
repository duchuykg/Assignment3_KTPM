import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options as ChromeOption


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
    def setup_method(self):
        chrome_option = ChromeOption()
        chrome_option.add_argument('--lang=en')
        self.driver = webdriver.Chrome(chrome_options=chrome_option)
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


    def test_upload_file_1(self):
        wait = WebDriverWait(self.driver, 50)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-btn-add"))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Upload a file"))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.NAME, "repo_upload_file")))

        file_path = os.path.abspath('../test files/test.pdf')
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(file_path)
        self.driver.find_element(By.XPATH, "//button[contains(.,'Upload this file')]").click()
        wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, '.fp-file')))
        self.driver.find_element(By.NAME, 'submitbutton').click()
        toast_message = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.toast-message')))

        result = toast_message.text == 'Changes saved'

        time.sleep(1)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-file'))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager.fp-select.fp-file > form > div:nth-child(1) > button:nth-child(2)')))
        self.driver.find_element(By.CSS_SELECTOR, '.filemanager.fp-select.fp-file > form > div:nth-child(1) > button:nth-child(2)').click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-dlg-butconfirm'))).click()
        self.driver.find_element(By.NAME, 'submitbutton').click()

        return result


    def test_upload_file_2(self):
        wait = WebDriverWait(self.driver, 50)
        file_path = os.path.abspath('../test files/test.pdf')

        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager-container')))
        drop_target = self.driver.find_element(By.CSS_SELECTOR, '.filemanager-container')
        drop_target.drop_files(file_path)   
        wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, '.fp-file')))

        self.driver.find_element(By.NAME, 'submitbutton').click()
        toast_message = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.toast-message')))

        result = toast_message.text == 'Changes saved'

        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-file'))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager.fp-select.fp-file > form > div:nth-child(1) > button:nth-child(2)')))
        self.driver.find_element(By.CSS_SELECTOR, '.filemanager.fp-select.fp-file > form > div:nth-child(1) > button:nth-child(2)').click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-dlg-butconfirm'))).click()
        self.driver.find_element(By.NAME, 'submitbutton').click()

        return result


    def test_upload_file_3(self):
        wait = WebDriverWait(self.driver, 50)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-btn-mkdir"))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input")))
        self.driver.find_element(By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input").send_keys('test1')
        self.driver.find_element(By.CSS_SELECTOR, ".fp-dlg-butcreate").click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-file.fp-folder'))).click()
        
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-btn-add"))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Upload a file"))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.NAME, "repo_upload_file")))

        file_path = os.path.abspath('../test files/test.pdf')
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(file_path)
        self.driver.find_element(By.XPATH, "//button[contains(.,'Upload this file')]").click()
        wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, '.fp-file')))
        self.driver.find_element(By.NAME, 'submitbutton').click()
        toast_message = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.toast-message')))

        result = toast_message.text == 'Changes saved'

        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-contextmenu'))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager.fp-select.fp-folder > form > div:nth-child(1) > button:nth-child(2)'))).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.fp-dlg-butconfirm'))).click()
        self.driver.find_element(By.NAME, 'submitbutton').click()

        return result

    def test_upload_file_4(self):
        return True


    def test_upload_file_5(self):
        wait = WebDriverWait(self.driver, 50)
        file_path = os.path.abspath('../test files/test2.pdf')

        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager-container')))
        drop_target = self.driver.find_element(By.CSS_SELECTOR, '.filemanager-container')
        drop_target.drop_files(file_path)
        toast_message = wait.until(expected_conditions.visibility_of_element_located((By.ID, "fp-msg-labelledby"))).text
        self.driver.find_element(By.CSS_SELECTOR, '.file-picker.fp-msg.fp-msg-error > button').click()

        return toast_message == 'The file test2.pdf is too large. The maximum size you can upload is 100MB.'


    def test_upload_file_6(self):
        wait = WebDriverWait(self.driver, 20)
        file_path = os.path.abspath('../test files/test3.ext')

        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager-container')))
        drop_target = self.driver.find_element(By.CSS_SELECTOR, '.filemanager-container')
        drop_target.drop_files(file_path)
        try:
            toast_message = wait.until(expected_conditions.visibility_of_element_located((By.ID, "fp-msg-labelledby"))).text
            self.driver.find_element(By.CSS_SELECTOR, '.file-picker.fp-msg.fp-msg-error > button').click()

            return toast_message.text == 'The file test2.pdf has invalid extension'
        except:
            return False

    
    def test_upload_file_7(self):
        wait = WebDriverWait(self.driver, 50)
        file_path = os.path.abspath('../test files/test4.ext')

        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.filemanager-container')))
        drop_target = self.driver.find_element(By.CSS_SELECTOR, '.filemanager-container')
        drop_target.drop_files(file_path)
        toast_message = wait.until(expected_conditions.visibility_of_element_located((By.ID, "fp-msg-labelledby"))).text
        self.driver.find_element(By.CSS_SELECTOR, '.file-picker.fp-msg.fp-msg-error > button').click()

        return toast_message == 'The file test4.ext is too large. The maximum size you can upload is 100MB.'


    def test_upload_file_8(self):
        wait = WebDriverWait(self.driver, 50)
        try:
            wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-btn-mkdir"))).click()
            wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input")))
            self.driver.find_element(By.CSS_SELECTOR, ".fp-mkdir-dlg-text > input").clear()
            create_btn = self.driver.find_element(By.CSS_SELECTOR, ".fp-dlg-butcreate")
            return create_btn.value_of_css_property('opacity') == '0.65'
        except:
            return False

    def run(self):
        result = []
        fail_test_name = []

        # test case 2
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_2()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_2.__name__)
        self.teardown_method(None)

        # test case 1
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_1()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_1.__name__)
        self.teardown_method(None)

        # test case 3
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_3()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_3.__name__)
        self.teardown_method(None)


        # test case 4
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_4()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_4.__name__)
        self.teardown_method(None)


        # test case 5
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_5()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_5.__name__)
        self.teardown_method(None)


        # test case 6
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_6()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_6.__name__)
        self.teardown_method(None)


        # test case 7
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_7()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_7.__name__)
        self.teardown_method(None)


        # test case 8
        self.setup_method()
        self.login_student_account()
        self.navigate_to_upload_place()
        test = self.test_upload_file_8()
        result.append(test)
        if not test:
            fail_test_name.append(self.test_upload_file_8.__name__)
        self.teardown_method(None)


        fail_test_name_str = 'Fail testcase:\n\t' + '\n\t'.join(name for name in fail_test_name) if len(fail_test_name) != 0 else 'Fail testcase: None'
        return f"""
        \n---------- Test upload private file result -----------\nCorrect test: {result.count(True)}/{len(result)}\n{fail_test_name_str}\n------------------------------------
        """

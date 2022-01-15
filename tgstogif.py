import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import listdir, path, getcwd, system

file_extension = "tgs"
options = webdriver.ChromeOptions() 

# chromedriver needs to be updated according to your Chrome Browser version
chrome_sel_path = 'D:\C\Program Files\Selenium\Chrome\Chrome ver 97\chromedriver.exe' # set your chromedriver path

def openBrowser():
    driver.get("https://www.emojibest.com/tgs-to-gif")
    # waiting for webpage to load
    driver.implicitly_wait(30)

def sendfiles(tgs_file):
    # driver.implicitly_wait(10)
    upload_file = driver.find_element_by_class_name("el-upload__input")
    
    print("Uploading place caught")
    
    upload_file.send_keys(tgs_file) # uploading file

def downloadfiles():
    driver.implicitly_wait(10)
    
    download_file = driver.find_element_by_class_name("el-button")
    print("Downloading place caught")
    download_file.click()
    # wait for file to be converted
    driver.implicitly_wait(60)

    download_start = driver.find_element_by_class_name("el-button--success") # selecting download button
    download_start.click() # clicking download button
    

if __name__ == "__main__":
    directory = getcwd() # current directory where the python file is placed

    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": directory+"\\", # IMPORTANT - ENDING SLASH V IMPORTANT,
        "directory_upgrade": True
        }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=chrome_sel_path, options=options)

    ar = [i for i in listdir() if i.endswith(file_extension)] # selecting only the files ending with .tgs extension
    time.sleep(5)

    input("Ready ? \nPress Enter to continue")
    system("cls")
    # print("Converting : ", ar)
    
    print("Opening Browser") # opening webpage
    openBrowser()

    count = 0
    for t in ar:
        # initialise
        tries = 0
        uploaded = False
        dowloaded = False
        print("Converting :", t)
        f = path.abspath(t) # finding absolute path so to pass it to webpage

        while ((tries < 3) and (not uploaded)): # will try for 3 times if upload encounters some error
            try:
                sendfiles(f)
                tries = 0
                uploaded = True
            except:
                tries+=1
            
        # driver.implicitly_wait(30)
        
        while ((tries < 3) and (not dowloaded)): # if not uploaded, tries becomes >3 and it will try for 3 times if download encounters some error 
            try:
                downloadfiles()
                tries = 0
                dowloaded = True
            except:
                tries+=1
                
        # time.sleep(5)
        count+=1
        if count == 3: # done so to reload the page, continous conversion takes a lot of memory
            openBrowser() # reopening
            # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
            count = 0
            # if input("Turn it off ? (y/n) : ").lower() == 'y':    #if you want to close the program/Chrome, you can make use of this statement
            #     driver.quit()
            #     break
    time.sleep(30) # time alloted to download the last file
    driver.quit()

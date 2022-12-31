import time
from os import listdir, path, getcwd, system, rename
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

# chromedriver needs to be updated according to your Chrome Browser version
chrome_sel_path = "path\\to\\chromedriver.exe" # set your chromedriver path

def rename_webp_to_mp4():
    file_extension = "webp"
    new_extension = "mp4"

    to_be_renamed = [i for i in listdir() if i.endswith(file_extension)] #  PYTHON FILE IS IN THE SAME FOLDER WHERE webp FILES ARE
    for f in to_be_renamed:
        rename(f, str(f.split(".")[0])+"."+new_extension)

def openBrowser(link):
    driver.get(link)
    time.sleep(10)

    # waiting for webpage to load
    # driver.implicitly_wait(30)

    

    # pass

def uploadFile(mp4file):
    # driver.implicitly_wait(10)
    # upload_file = driver.find_element_by_class_name("up-input")
    upload_file = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/form/fieldset/p[1]/input")

    
    print(">>> Uploading place caught")
    
    upload_file.send_keys(mp4file) # uploading file

    # up_button = driver.find_element_by_class_name("button primary")

    # up_button = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/form/fieldset/p[4]/input")     # <<< THIS WAS OLDER VERSION OF SELINIUM
    up_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/form/fieldset/p[4]/input")
    

    up_button.click()
    print(">>> Uploaded")
    time.sleep(2)

def downloadFile():
    # driver.implicitly_wait(10)

    # convert_button = driver.find_element_by_class_name("button primary")

    # convert_button = driver.find_element_by_xpath("/html/body/div/div[4]/div[1]/form/p[3]/input")            # <<< THIS WAS IN OLDER VERSION ON SELINIUM
    convert_button = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[1]/form/p[3]/input")

    print("Converting place caught")
    convert_button.click()

    # time.sleep(10)

    # driver.implicitly_wait(10)
    # save_button = driver.find_element_by_class_name("save") 

    # save_button = driver.find_element_by_xpath("/html/body/div/div[4]/div[1]/div[3]/table/tbody/tr[2]/td[7]/a") # <<< THIS WAS IN OLDER VERSION ON SELINIUM
    save_button = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[1]/div[3]/table/tbody/tr[2]/td[7]/a")
    

    print(">>> Downloading place caught")
    save_button.click()
    print(">>> Downloaded")

    time.sleep(2)

    
    # pass

if __name__ == "__main__":
    link = "https://ezgif.com/video-to-gif"
    rename_webp_to_mp4()

    directory = getcwd()

    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": directory+"\\", # IMPORTANT - ENDING SLASH V IMPORTANT,
        "directory_upgrade": True
        }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=chrome_sel_path, options=options)
    driver.implicitly_wait(20)

    input("Ready ? \nPress Enter to continue")
    system("cls")

    print("Opening Browser") # opening webpage
    openBrowser(link)

    count = 0

    to_process = [i for i in listdir() if i.endswith("mp4")]
    done_process = []
    log_f = open("log.txt", "w")

    try:
        for t in to_process:
        # for t in range(2):
            # initialise
            tries = 0
            uploaded = False
            dowloaded = False
            print("CONVERTING :", t)
            f = path.abspath(t) # finding absolute path so to pass it to webpage

            while ((tries < 3) and (not uploaded)): # will try for 3 times if upload encounters some error
                try:
                    print(">>> TRYING TO UPLOAD FILE !!!")
                    uploadFile(f)
                    log_f.write(f"\n>>> UPLOADED {t}")
                    tries = 0
                    uploaded = True
                except:
                    print(">>> SOME ERROR IN UPLOADING FILE !!!")
                    openBrowser(link)
                    tries+=1
                
            # driver.implicitly_wait(30)
            
            while ((tries < 3) and (not dowloaded)): # if not uploaded, tries becomes >3 and it will try for 3 times if download encounters some error 
                try:
                    print(">>> TRYING TO DOWNLOAD FILE !!!")
                    downloadFile()
                    tries = 0
                    dowloaded = True
                    done_process.append(t)
                    print(f"\n\n>>> {t} CONVERTION DONE !!!\n\n")
                    log_f.write(f"\n\t>>> {t} CONVERTED.\n")
                    time.sleep(2)
                except:
                    print(">>> SOME ERROR IN DOWNLOADING FILE !!!")
                    tries+=1
                    
            # time.sleep(5)
            count+=1
            # if count == 3: # done so to reload the page, continous conversion takes a lot of memory
            if dowloaded:
                openBrowser(link) # reopening
                # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
                count = 0
                # if input("Turn it off ? (y/n) : ").lower() == 'y':    #if you want to close the program/Chrome, you can make use of this statement
                #     driver.quit()
                #     break
    except:
        print("SOME ERROR !!!")
        log_f.write("\n\nSOME ERROR !!!\n\n")
    
    time.sleep(30) # time alloted to download the last file
    print(">>> DONE")
    # log_f
    print(sorted(to_process))
    print(sorted(done_process))
    
    not_done = set(to_process)-set(done_process)
    print(not_done)

    log_f.write("- "*10+f"\nTO PROCESS : {sorted(to_process)}\nPROCESSED : {done_process}\nNOT DONE : {not_done}\n"+"- *10")
    log_f.close()

    input("\n\n\tENTER ANY KEY TO EXIT.")
    driver.quit()

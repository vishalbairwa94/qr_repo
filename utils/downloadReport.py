import time
from selenium.webdriver.support.ui import WebDriverWait
import os
import shutil

def wait_for_download_and_rename(newFilename, driver, download_dir):
    # function to wait for all chrome downloads to finish
    def chrome_downloads(drv):
        if not "chrome://downloads" in drv.current_url: # if 'chrome downloads' is not current tab
            drv.execute_script("window.open('');") # open a new tab
            drv.switch_to.window(driver.window_handles[1]) # switch to the new tab
            drv.get("chrome://downloads/") # navigate to chrome downloads
        return drv.execute_script("""
            return document.querySelector('downloads-manager')
            .shadowRoot.querySelector('#downloadsList')
            .items.filter(e => e.state === 'COMPLETE')
            .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
            """)
    # wait for all the downloads to be completed
    dld_file_paths = WebDriverWait(driver, 120, 1).until(chrome_downloads) # returns list of downloaded file paths
    # Close the current tab (chrome downloads)
    if "chrome://downloads" in driver.current_url:
        driver.close()
    # Switch back to original tab
    driver.switch_to.window(driver.window_handles[0])
    # get latest downloaded file name and path
    dlFilename = dld_file_paths[0] # latest downloaded file from the list
    # wait till downloaded file appears in download directory
    time_to_wait = 20 # adjust timeout as per your needs
    time_counter = 0
    while not os.path.isfile(dlFilename):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            break
    # rename the downloaded file
    shutil.move(dlFilename, os.path.join(download_dir,newFilename))
    return
from selenium import webdriver
from utils import downloadReport


def initiate_download(url):
    new_file_name = 'my_file.pdf'
    output = "outfile.jpg"

    download_dir = r'/Users/vishalbairwa'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir, # Set own Download path
        "download.prompt_for_download": False, # Do not ask for download at runtime
        "download.directory_upgrade": True, # Also needed to suppress download prompt
        "plugins.plugins_disabled": ["Chrome PDF Viewer"], # Disable this plugin
        "plugins.always_open_pdf_externally": True, # Enable this plugin
    })
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(url)
    downloadReport.wait_for_download_and_rename(new_file_name, driver, download_dir)
    driver.quit()
    return new_file_name
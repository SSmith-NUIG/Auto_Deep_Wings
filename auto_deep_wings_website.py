from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode

# initiate firefox webdriver.
# This needs to be specific to your OS.
# see relevant tutorial https://www.tutorialspoint.com/how-to-get-firefox-working-with-selenium-webdriver-on-mac-osx
# When this driver is downloaded, change the path here to your path:
driver = webdriver.Firefox(executable_path=r'/home/stephen/Downloads/geckodriver-v0.31.0-linux64/geckodriver')

# get deepwings URL
url = "https://deepwings.ddns.net/"
driver.get(url)
driver.implicitly_wait(10)

# find the upload button using CSS
upload_file = driver.find_element_by_css_selector('.dz-hidden-input')

# ALL OF THIS WILL BE PUT INSIDE A FOR LOOP
# TO LOOP OVER ALL DIRECTORIES OF SAMPLES


# initiate an empty list to store our images in
list_of_images = []
# grab its basename
sample_name = os.path.basename("M343G22")
# loop over all images in this directory
for images in os.listdir("/home/stephen/Documents/deep_wings/test_images/M343G22/"):
    # account for MAC OS .DS_Store file
    if not images.startswith('.'):
        # Only grab the cropped images, not the main original
        if "_" in images:
            # grab full image path, REPLACE THIS WITH ARGPARSE
            image_path = "/home/stephen/Documents/deep_wings/test_images/M343G22/" + images
            # append this to our list
            list_of_images.append(image_path)

# dropzone CSS accepts a list of file paths separated by a newline character
string_of_paths = "\n".join(list_of_images)

# hit the upload file button on the dropzone and send it our list of samples
upload_file.send_keys(string_of_paths)
# wait 20 seconds for the analysis to run (decrease or increase this based on your experiences with the script
driver.implicitly_wait(20)

# Wait another 40 seconds, again decrease or increase as you see fit.
# Then click the download xlsx button by its XPATH
WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="download-xlsx"]'))).click()

# Move and rename the downloaded file.
# NOTE: there can be no other data.xlsx file in your downloads when you run this script or else this will fail
# Subsequent downloads will be named data(1).xlsx etc.
# REPLACE OUTPUT FOLDER WITH ARGPARSE?
os.rename("/home/stephen/Downloads/data.xlsx", "/home/stephen/Documents/deep_wings/outputs/{}.xlsx".format(sample_name))
# close the driver
driver. close()



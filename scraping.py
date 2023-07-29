import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import random
import string
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"Image downloaded successfully: {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {url}\n", e)


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()))
    google_images = "https://www.google.com/imghp?hl=EN"
    driver.get(google_images)

    n_img = input("Enter number of images you want:\n")
    search = input("What images do you want?:\n")
    text_area = driver.find_element(By.XPATH, '//textarea[@class="gLFyf"]')
    text_area.send_keys(search)
    root = Path("images")
    save_folder = Path(search)
    save_folder = root / save_folder
    save_folder.mkdir(parents=True, exist_ok=True)
    button = driver.find_element(By.XPATH, '//button[@class="Tg7LZd"]')
    driver.execute_script("arguments[0].click();", button)
    a = input("Waiting for the user input to start..")

    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, "html.parser")
    containers = pageSoup.findAll("div", {"class": "isv-r PNCib MSM1fd BUooTd"})

    len_containers = len(containers)
    print(f"Found {len_containers} images to download")

    img_urls = []

    def wait_for_elements_visibility(xpath):
        wait = WebDriverWait(driver, 20)
        elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        return elements

    # Define the XPath to locate all the images
    images_xpath = '//*[@class="wXeWr islib nfEiy"]'
    # Get all the image elements
    image_elements = wait_for_elements_visibility(images_xpath)

    # Loop through each image element and perform actions (click, extract information, etc.)
    try:
        for i, image_element in enumerate(image_elements):
            if i >= int(n_img):
                break
            # For demonstration purposes, let's click on each image
            image_element.click()
            # You can perform any other action you want on each image element.
            # Add your logic here...
            opened_img_xpath = """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]"""
            max_wait = 0
            while (
                driver.find_element(By.XPATH, opened_img_xpath).get_attribute("src").startswith("data:")
                or driver.find_element(By.XPATH, opened_img_xpath).get_attribute("src").startswith("https://encrypted-tbn0")
            ):
                max_wait += 1
                time.sleep(2)
                if max_wait == 15:
                    break
            opened_img_element = driver.find_element(By.XPATH, opened_img_xpath)
            image_src_link = opened_img_element.get_attribute('src')
            print(image_src_link)
            img_urls.append(image_src_link)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

    # Create a folder to save the downloaded images
    if not os.path.exists('images'):
        os.makedirs('images')

    # Check if the urls.txt file exists for the given search keyword
    urls_file_path = os.path.join('images', f"{search}/urls.txt")
    if os.path.exists(urls_file_path):
        # Read the URLs from the file and store them in a list
        with open(urls_file_path, 'r') as urls_file:
            urls_open = urls_file.readlines()
        urls_open = [i.strip() for i in urls_open]

        # Filter out the URLs that are already downloaded
        img_urls = [url for url in img_urls if url not in urls_open]

    # Loop through the list of image URLs and download each image
    for idx, url in enumerate(img_urls, start=1):
        # Generate a unique filename for the image using timestamp and random string
        timestamp = int(time.time())
        random_string = generate_random_string(6)
        filename = f"{timestamp}_{random_string}.jpg"

        save_path = os.path.join(save_folder, filename)
        download_image(url, save_path)

        # Append the downloaded URL to the urls.txt file
        with open(urls_file_path, 'a+') as urls_file:
            urls_file.write(url + '\n')


if __name__ == "__main__":
    main()
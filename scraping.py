from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import io
from PIL import Image
import time


options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
options.binary_location = "D:\Workspace\Python\YOLO Vehicle detection\web_scraping\chromedriver.exe"  
driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()))


image_url = "https://5.imimg.com/data5/ANDROID/Default/2022/6/DJ/CQ/QT/43079619/screenshot-2022-06-03-15-27-49-15-jpg-500x500.jpg"

def get_google_images(wd, delay, max_images, url):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    wd.get(url)
    image_urls = set()
    while len(image_urls) < max_images:
        scroll_down(driver)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) : max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            images = wd.find_elements(By.CLASS_NAME, "r48jcc pT0Scc iPVvYb")
            for image in images:
                if image.get_attribute("src") and "http" in image.get_attribute("src"):
                    image_urls.add(image.get_attribute("src"))
            print(f"Found {len(image_urls)} images.")
    return image_urls

            



def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        print(image_content)
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        print("Success")
    except Exception as e:
        print(f"Failed - {e}")

# download_image("", image_url, "test.jpg")
urls = get_google_images(wd=driver, delay=1, max_images=5, url="https://www.google.com/search?q=lorry+india+road&tbm=isch&ved=2ahUKEwjRyKfk6uP_AhUB4qACHbo_ARMQ2-cCegQIABAA&oq=lorry+india+road&gs_lcp=CgNpbWcQAzoECCMQJzoFCAAQgAQ6CwgAEIAEELEDEIMBOgcIABCKBRBDOgYIABAFEB46BAgAEB46BggAEAgQHlCXBVjMH2D-IGgAcAB4AIABqwGIAfENkgEEMC4xMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=bAmbZNHiFoHEg8UPuv-EmAE&bih=680&biw=1177")
print(urls)
driver.quit()
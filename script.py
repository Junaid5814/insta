import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Render Environment Variables se credentials uthana (Security ke liye best practice hy)
INSTAGRAM_USERNAME = os.environ.get("IG_USERNAME", "j_tech_pk")
INSTAGRAM_PASSWORD = os.environ.get("IG_PASSWORD", "Junaid.5814")

TARGET_HASHTAGS = ["techinvestor", "uktech", "londonstartups", "sauditech", "riyadhstartups", "siliconvalley"]
LIKE_LIMIT_PER_HOUR = 10

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def human_scroll(driver):
    scroll_amount = random.randint(200, 500)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(random.randint(2, 5))

def login_to_instagram(driver, username, password):
    driver.get("https://instagram.com")
    time.sleep(random.randint(5, 8))
    
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")
    
    for letter in username:
        user_input.send_keys(letter)
        time.sleep(random.uniform(0.1, 0.3))
        
    for letter in password:
        pass_input.send_keys(letter)
        time.sleep(random.uniform(0.1, 0.3))
        
    pass_input.send_keys(Keys.ENTER)
    time.sleep(random.randint(8, 12))

def like_posts_by_hashtag(driver, hashtag, max_likes):
    url = f"https://instagram.com{hashtag}/"
    driver.get(url)
    time.sleep(random.randint(6, 10))
    
    try:
        first_post = driver.find_element(By.XPATH, '//article//a')
        first_post.click()
        time.sleep(random.randint(4, 6))
    except Exception:
        print(f"Hashtag #{hashtag} par posts load nahi ho sakeen.")
        return 0

    likes_done = 0
    while likes_done < max_likes:
        try:
            human_scroll(driver)
            
            like_button = driver.find_element(By.XPATH, '//article//section/span/button')
            svg_element = like_button.find_element(By.TAG_NAME, 'svg')
            current_label = svg_element.get_attribute("aria-label")
            
            if current_label == "Like":
                actions = ActionChains(driver)
                actions.move_to_element(like_button).perform()
                time.sleep(random.randint(1, 3))
                
                like_button.click()
                likes_done += 1
                print(f"[+] Liked post {likes_done}/{max_likes} under #{hashtag}")
                time.sleep(random.randint(30, 60)) 
            else:
                print("[-] Already liked, skipping...")

            next_button = driver.find_element(By.XPATH, '//svg[@aria-label="Next"]/ancestor::button')
            next_button.click()
            time.sleep(random.randint(6, 12))
            
        except Exception:
            print("[!] Loop main error ya posts khatam.")
            break
            
    return likes_done

def main():
    print("Script started on Render cloud container...")
    driver = init_driver()
    try:
        login_to_instagram(driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        
        while True:
            print("\n--- Starting New Hourly Cycle ---")
            selected_hashtag = random.choice(TARGET_HASHTAGS)
            
            total_liked = like_posts_by_hashtag(driver, selected_hashtag, LIKE_LIMIT_PER_HOUR)
            print(f"Cycle finished. Total likes: {total_liked}")
            
            sleep_window = 3600 + random.randint(100, 400)
            print(f"Sleeping for {sleep_window // 60} minutes...")
            time.sleep(sleep_window)
            
    except KeyboardInterrupt:
        print("Script stopped.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

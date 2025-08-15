import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')


class InternetSpeedTwitterBot:
    def __init__(self):
        self.options = webdriver.ChromeOptions()

        # Make browser look more human and less automated
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # Selenium 4.6+ will automatically manage the driver
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.up = 0
        self.down = 0
        self.wait = WebDriverWait(self.driver, 20)

    def human_delay(self, min_seconds=1, max_seconds=3):
        """Random delay to mimic human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def human_type(self, element, text):
        """Type text like a human with random delays between keystrokes"""
        self.human_delay(0.5, 1)
        element.click()
        self.human_delay(0.2, 0.5)

        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))

        self.human_delay(0.5, 1)

    def get_internet_speed(self):
        try:
            self.driver.get("https://www.speedtest.net/")
            self.human_delay(2, 4)

            # Accept cookies if present
            try:
                accept_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
                )
                accept_button.click()
                self.human_delay()
            except:
                pass

            # Start speed test
            go_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a"))
            )
            go_button.click()
            self.human_delay(2, 3)

            # Wait for test to complete
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".speedtest-container .result-container"))
            )
            self.human_delay(10, 15)  # Extra buffer time

            # Get results
            self.up = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".upload-speed"))
            ).text
            self.down = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".download-speed"))
            ).text

            print(f"Speed Test Results - Download: {self.down} Mbps, Upload: {self.up} Mbps")

        except Exception as e:
            print(f"Error during speed test: {e}")
            raise

    def tweet_at_provider(self):
        try:
            self.driver.get("https://twitter.com/login")
            self.human_delay(3, 5)

            # Handle Twitter login
            email_field = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            self.human_type(email_field, TWITTER_EMAIL)
            email_field.send_keys(Keys.RETURN)
            self.human_delay(1, 2)

            # Twitter might ask for username if account has 2FA
            try:
                username_field = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='on']"))
                )
                self.human_delay()
                username_field.clear()
                self.human_type(username_field, TWITTER_EMAIL.split('@')[0])
                username_field.send_keys(Keys.RETURN)
                self.human_delay(1, 2)
            except:
                pass

            password_field = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='current-password']"))
            )
            self.human_type(password_field, TWITTER_PASSWORD)
            password_field.send_keys(Keys.RETURN)
            self.human_delay(3, 5)

            # Compose tweet
            tweet_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/compose/tweet']"))
            )
            tweet_button.click()
            self.human_delay(1, 2)

            tweet_compose = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']"))
            )

            tweet_message = (
                f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up "
                f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up? "
                "#InternetSpeed #ISP"
            )

            self.human_type(tweet_compose, tweet_message)
            self.human_delay(1, 2)

            # Post tweet
            tweet_post = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetButton']"))
            )
            tweet_post.click()
            self.human_delay(2, 3)

            print("Tweet posted successfully!")

        except Exception as e:
            print(f"Error during Twitter posting: {e}")
            raise
        finally:
            self.human_delay(2, 4)
            self.driver.quit()


if __name__ == "__main__":
    # Verify environment variables
    if not all([TWITTER_EMAIL, TWITTER_PASSWORD]):
        raise ValueError("Please set TWITTER_EMAIL and TWITTER_PASSWORD in your .env file")

    bot = InternetSpeedTwitterBot()
    try:
        bot.get_internet_speed()
        bot.tweet_at_provider()
    except Exception as e:
        print(f"Bot encountered an error: {e}")
        bot.driver.save_screenshot('error_screenshot.png')
        print("Screenshot saved as error_screenshot.png")
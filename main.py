from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import random
import string
from datetime import datetime
import pyperclip
import re

def generate_random_username(length=8):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_dob():
    current_year = datetime.now().year
    year = random.randint(current_year - 50, current_year - 18)
    month = random.randint(1, 12)
    if month in [1,3,5,7,8,10,12]:
        day = random.randint(1, 31)
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    else:
        day = random.randint(1, 30)
    return (day, month, year)

def get_temp_email(driver):
    print("[INFO] Navigating to tempmail.la...")
    driver.get("https://tempmail.la/")
    try:
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-primary') and contains(@class, 'text-primary-foreground')]"))
        )
        button.click()
        print("[SUCCESS] Initial popup/button clicked.")
    except Exception:
        print("[INFO] Initial popup/button not found or not needed.")

    time.sleep(3)

    try:
        copy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'inline-flex') and contains(@class,'font-medium') and contains(@class,'rounded-md')]"))
        )
        print("[INFO] Trying to click email copy button...")

        try:
            copy_button.click()
        except UnexpectedAlertPresentException:
            print("[WARN] Alert appeared on clicking copy button, trying to accept alert...")
            try:
                alert = driver.switch_to.alert
                alert.accept()
                print("[SUCCESS] Alert accepted.")
                time.sleep(1)  # thoda wait karo alert accept hone ke liye
                copy_button.click()  # dobara click try karo
                print("[SUCCESS] Copy button clicked after alert accepted.")
            except NoAlertPresentException:
                print("[ERROR] Alert not found when expected.")
            except Exception as e:
                print(f"[ERROR] Could not accept alert: {e}")

        else:
            print("[SUCCESS] Copy button clicked successfully on first try.")
            
    except Exception as e:
        print(f"[ERROR] Could not click copy button: {e}")

    time.sleep(2)

    try:
        temp_email = pyperclip.paste()
        if temp_email and "@" in temp_email:
            print(f"[SUCCESS] Temporary email obtained from clipboard: {temp_email}")
            return temp_email
        else:
            print(f"[ERROR] Clipboard content invalid: '{temp_email}'")
            return None
    except Exception as e:
        print(f"[ERROR] Clipboard read failed: {e}")
        return None

def click_element(driver, element):
    try:
        element.click()
        print("[SUCCESS] Element clicked by normal click.")
        return True
    except Exception as e:
        print(f"[WARN] Normal click failed: {e}")

    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        element.click()
        print("[SUCCESS] Element clicked after scroll.")
        return True
    except Exception as e:
        print(f"[WARN] Scroll + click failed: {e}")

    try:
        driver.execute_script("arguments[0].click();", element)
        print("[SUCCESS] Element clicked by JavaScript click.")
        return True
    except Exception as e:
        print(f"[ERROR] JavaScript click failed: {e}")
        return False

def get_temp_email(driver):
    print("[INFO] Navigating to tempmail.la...")
    driver.get("https://tempmail.la/")
    try:
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-primary') and contains(@class, 'text-primary-foreground')]"))
        )
        button.click()
        print("[SUCCESS] Initial popup/button clicked.")
    except Exception:
        print("[INFO] Initial popup/button not found or not needed.")

    time.sleep(3)

    try:
        copy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'inline-flex') and contains(@class,'font-medium') and contains(@class,'rounded-md')]"))
        )
        print("[INFO] Trying to click email copy button...")
        
        if not click_element(driver, copy_button):
            print("[WARN] Could not click copy button by any method.")
            # Yahan aap manually copy karne ka message de sakte hain ya retry kar sakte hain

    except Exception as e:
        print(f"[ERROR] Could not find or click copy button: {e}")

    time.sleep(2)

    try:
        temp_email = pyperclip.paste()
        if temp_email and "@" in temp_email:
            print(f"[SUCCESS] Temporary email obtained from clipboard: {temp_email}")
            return temp_email
        else:
            print(f"[ERROR] Clipboard content invalid: '{temp_email}'")
            return None
    except Exception as e:
        print(f"[ERROR] Clipboard read failed: {e}")
        return None


def fill_instagram_signup_form(driver, email, fullname, username, password):
    wait = WebDriverWait(driver, 20)
    try:
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
        email_input.clear()
        email_input.send_keys(email)
        print("[INFO] Email entered.")
        fullname_input = wait.until(EC.presence_of_element_located((By.NAME, "fullName")))
        fullname_input.clear()
        fullname_input.send_keys(fullname)
        print("[INFO] Fullname entered.")
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.clear()
        username_input.send_keys(username)
        print("[INFO] Username entered.")
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.clear()
        password_input.send_keys(password)
        print("[INFO] Password entered.")
        sign_up_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign Up') or contains(text(),'Sign up')]"))
        )
        sign_up_button.click()
        print("[INFO] Sign Up button clicked.")
    except Exception as e:
        print(f"[ERROR] Exception during form fill: {e}")
        raise

def fill_dob(driver):
    wait = WebDriverWait(driver, 30)
    try:
        day, month, year = generate_random_dob()
        print(f"[INFO] Random DOB generated: {day}-{month}-{year}")
        month_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[title='Month:']")))
        day_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[title='Day:']")))
        year_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[title='Year:']")))
        month_name = datetime(year, month, day).strftime("%B")
        Select(month_select).select_by_visible_text(month_name)
        Select(day_select).select_by_visible_text(str(day))
        Select(year_select).select_by_visible_text(str(year))
        print(f"[INFO] DOB selected: {day} {month_name} {year}")
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
        )
        next_button.click()
        print("[INFO] DOB Next button clicked.")
        time.sleep(5)
    except Exception as e:
        print(f"[ERROR] DOB fill error: {e}")

def wait_for_otp_and_get_code(driver, timeout=180, poll_interval=5):
    print("[INFO] Waiting for OTP email from Instagram...")
    end_time = time.time() + timeout
    driver.switch_to.window(driver.window_handles[0])  # Switch to temp mail tab
    while time.time() < end_time:
        try:
            driver.refresh()
            time.sleep(5)
            emails = driver.find_elements(By.XPATH, "//li[contains(@class,'cursor-pointer')]")
            otp_email = None
            for email in emails:
                try:
                    sender = email.find_element(By.XPATH, ".//h3[contains(text(),'no-reply@mail.instagram.com')]")
                    if sender:
                        otp_email = email
                        break
                except:
                    continue
            if otp_email:
                otp_email.click()
                print("[INFO] OTP email opened.")
                time.sleep(5)
                try:
                    iframe = driver.find_element(By.TAG_NAME, "iframe")
                    driver.switch_to.frame(iframe)
                    print("[INFO] Switched to email iframe.")
                except:
                    print("[INFO] No iframe found, continuing...")
                otp_td = None
                try:
                    otp_td = driver.find_element(By.XPATH,
                        "//td[contains(@style,'font-size:32px') and contains(@style,'text-align:center')]")
                except:
                    pass
                if otp_td:
                    otp_code = otp_td.text.strip()
                    print(f"[INFO] OTP code extracted: {otp_code}")
                    driver.switch_to.default_content()
                    return otp_code
                else:
                    driver.switch_to.default_content()
                    email_body_text = driver.find_element(By.TAG_NAME, "body").text
                    match = re.search(r"\b(\d{6})\b", email_body_text)
                    if match:
                        otp_code = match.group(1)
                        print(f"[INFO] OTP code extracted via regex: {otp_code}")
                        return otp_code
                print("[WARN] OTP code not found in email, retrying...")
            else:
                print("[INFO] OTP email not yet arrived, retrying...")
        except Exception as e:
            print(f"[ERROR] Exception while fetching OTP email: {e}")
        time.sleep(poll_interval)
    print("[ERROR] Timeout reached while waiting for OTP email.")
    return None

def enter_otp_on_instagram(driver, otp_code):
    wait = WebDriverWait(driver, 30)
    try:
        driver.switch_to.window(driver.window_handles[1])
        print("[INFO] Switched back to Instagram tab.")

        otp_input = wait.until(EC.presence_of_element_located((By.NAME, "email_confirmation_code")))
        otp_input.clear()
        otp_input.send_keys(otp_code)
        print(f"[INFO] OTP code '{otp_code}' entered.")

        time.sleep(1)

        # Sirf custom div button click karna hai
        try:
            next_div_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(),'Next')]"))
            )
            print("[INFO] Found custom 'Next' div button, trying to click...")
            if not click_element(driver, next_div_button):
                print("[WARN] Failed to click custom 'Next' div button.")
        except Exception as e:
            print(f"[ERROR] Could not find or click custom 'Next' div button: {e}")

        time.sleep(5)

    except Exception as e:
        print(f"[ERROR] Error entering OTP or clicking Next button: {e}")


def insta_signup_with_temp_email(fullname, password):
    options = Options()
    # options.add_argument("--headless")  # Debugging ke liye headless off rakho
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    try:
        print("[INFO] Getting temporary email...")
        temp_email = get_temp_email(driver)
        if not temp_email:
            print("[ERROR] Temporary email not fetched, aborting.")
            return
        print("[INFO] Opening Instagram signup page...")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(5)
        username = generate_random_username()
        print(f"[INFO] Generated username: {username}")
        fill_instagram_signup_form(driver, temp_email, fullname, username, password)
        print("[INFO] Waiting for DOB page to load...")
        time.sleep(5)
        fill_dob(driver)
        otp_code = wait_for_otp_and_get_code(driver)
        if otp_code:
            enter_otp_on_instagram(driver, otp_code)
        else:
            print("[WARN] OTP code not retrieved, manual intervention needed.")
        print("[INFO] Signup flow done. Ab manual CAPTCHA solve karo agar aaye.")
        time.sleep(60)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        print("[INFO] Closing browser.")
        driver.quit()

if __name__ == "__main__":
    fullname = "Your Full Name"
    password = "YourStrongPassword123"
    insta_signup_with_temp_email(fullname, password)

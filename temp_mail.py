import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_temp_email(driver):
    driver.get("https://tempmail.la/")
    time.sleep(5)  # Page load aur email generate hone ka wait

    # Try copy button click (optional)
    try:
        copy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'inline-flex') and contains(@class,'font-medium')]")
            )
        )
        copy_button.click()
        print("[INFO] Copy button clicked successfully.")
    except Exception as e:
        print(f"[WARN] Could not click copy button: {e}")

    # Try to get email from input box
    temp_email = None

    possible_selectors = [
        "input[readonly]",
        "input#email",          # agar id ho to
        "input[type='text']",   # input text ka koi aur
        "div#email",            # kabhi div me bhi hota hai
        "span#email",           # ya span me bhi
    ]

    for selector in possible_selectors:
        try:
            elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            temp_email = elem.get_attribute("value") or elem.text
            if temp_email and "@" in temp_email:
                print(f"[INFO] Temporary email fetched using selector '{selector}': {temp_email}")
                break
        except Exception:
            continue

    if not temp_email:
        print("[ERROR] Could not fetch temporary email using known selectors.")
    return temp_email

def wait_for_instagram_email_and_get_otp(driver, wait_seconds=120):
    timeout = wait_seconds
    while timeout > 0:
        try:
            mails = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            for mail in mails:
                subject = mail.find_element(By.CSS_SELECTOR, "td.subject").text
                if "Instagram" in subject:
                    mail.click()
                    time.sleep(5)
                    body = driver.find_element(By.ID, "email-body").text
                    otp = re.findall(r"\b\d{6}\b", body)
                    if otp:
                        print(f"[INFO] OTP found: {otp[0]}")
                        return otp[0]
            time.sleep(5)
            timeout -= 5
        except Exception as e:
            print(f"[WARN] Waiting for OTP... {e}")
            time.sleep(5)
            timeout -= 5
    return None

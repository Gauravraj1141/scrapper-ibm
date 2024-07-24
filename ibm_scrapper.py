from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import poplib,imaplib
import email
from email import policy
from bs4 import BeautifulSoup
import re
import chardet

def decode_email_body(part):
    payload = part.get_payload(decode=True)
    result = chardet.detect(payload)
    encoding = result['encoding']
    return payload.decode(encoding)



def create_ibm_account():
    website = "https://login.ibm.com/"

    driver = webdriver.Chrome()
    driver.get(website)

    create_new_ac = driver.find_element(By.CLASS_NAME, "register-text")
    create_new_ac.click()

    # now fill the details in the input boxes 
    driver.find_element(By.ID, "email").send_keys("gauravthakur81711296@gmail.com")
    driver.find_element(By.ID, "password").send_keys("GauravRaj@321r")
    driver.find_element(By.ID, "firstName").send_keys("Gaurav")
    driver.find_element(By.ID, "lastName").send_keys("Rajput")
    driver.find_element(By.ID, "country").send_keys("India")
    time.sleep(5)
    driver.find_element(By.ID, "state").send_keys("Uttar Pradesh")
    label_yes = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='isStudentYes']"))
        )
    label_yes.click()
    driver.find_element(By.CLASS_NAME,"section-button-container").click()
    time.sleep(5)
    print("we are waiting for 5 seconds for latest confirmation code ")
    password = 'otwe vqxk eoln opbk'
    email_id = 'gauravthakur81711296@gmail.com'
    code = get_confirmation_code(email_id,password)
    print(code)
    driver.find_element(By.ID, "token").send_keys(code)

    driver.find_element(By.CLASS_NAME,"button-container").click()

    # now click on proceed button 
    proceed_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed')]")
    proceed_button.click()
    
    otp = get_confirmation_code(email_id,password,process="Verify your identity")
    driver.find_element(By.ID, "otp").send_keys(otp)
    time.sleep(2)
    verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
    verify_button.click()

    time.sleep(10)

    # now go to profile page and fill the details
   
        

    time.sleep(50)


def login_to_ibm_profile():
    website = "https://community.ibm.com/community/user/businessanalytics/home"

    driver = webdriver.Chrome()
    driver.get(website)

    try:
        # Wait for and click the consent button if it appears
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "truste-consent-button"))
        ).click()
        
        # Click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Join / Log in')]"))
        )
        login_button.click()

        # Enter username
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys("gauravthakur81711296@gmail.com")

        # Click continue
        driver.find_element(By.ID, "continue-button").click()

        # Wait for password field to be visible and enter password
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys("GauravRaj@321r")

        # Click sign-in button
        driver.find_element(By.ID, "signinbutton").click()

        # Wait for some time to ensure login process completes
        time.sleep(150)

    finally:
        driver.quit()





def get_confirmation_code(email_id,password,process="New User Registration"):
    imap = imaplib.IMAP4_SSL('pop.mailinator.com')
    imap.login(email_id, password)
    imap.select('inbox')
    # Search for all emails in the inbox
    status, messages = imap.search(None, 'ALL')
    email_ids = messages[0].split()

    # Fetch the latest 10 emails
    latest_email_ids = reversed(email_ids[-10:])

    messages = []
    for e_id in latest_email_ids:
        _, msg_data = imap.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1], policy=policy.default)
                messages.append(msg)
    confirmation_code = None
    for message in messages:
        if 'IBM' in message['from'] and process in message['subject']:
            for part in message.walk():
                if part.get_content_type() == 'text/html':
                    body = decode_email_body(part)
                    if process == "Verify your identity":
                        confirmation_code = re.search(r'\b\d{4}-\d{6}\b', body).group()
                        confirmation_code = confirmation_code.split("-")[1]
                        return confirmation_code
                    else:
                        soup = BeautifulSoup(body, 'html.parser')
                        h2_tag = soup.find('h2', class_='code')
                        if h2_tag:
                            confirmation_code = h2_tag.text.strip()
                            confirmation_code = confirmation_code
                            return confirmation_code
    return confirmation_code

if __name__ == "__main__":
    create_ibm_account()
    login_to_ibm_profile()
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
#driver = webdriver.Safari()

last_url='https://binothaimeen.net/ar/voice_library/sectionDetails/%D8%A7%D9%84%D9%84%D9%82%D8%A7%D8%A1%D8%A7%D8%AA%20%D9%88%D8%A7%D9%84%D9%81%D8%AA%D8%A7%D9%88%D9%89/%D9%81%D8%AA%D8%A7%D9%88%D9%89%20%D9%86%D9%88%D8%B1%20%D8%B9%D9%84%D9%89%20%D8%A7%D9%84%D8%AF%D8%B1%D8%A8/%D8%A7%D9%84%D8%B4%D8%B1%D9%8A%D8%B7%20%D8%B1%D9%82%D9%85%20[3]%20/569de6a4-731b-4eb4-a80f-2bcd053c4f51?'
driver.get(last_url)

# Wait for elements to load
wait = WebDriverWait(driver, 10)
#wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[contains(@style, 'cursor: pointer')]")))
#wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(@style, 'cursor: pointer')]")))
# Find all elements that have 'cursor: pointer' in their style attribute

#ibrahim added this code....
element = driver.find_element(By.CSS_SELECTOR, ".MuiAccordionSummary-content.MuiAccordionSummary-contentGutters.css-17o5nyn")
driver.execute_script("arguments[0].scrollIntoView();", element)
element.click()
element = driver.find_element(By.CLASS_NAME, "list-group-item")
driver.execute_script("arguments[0].scrollIntoView();", element)
element.click()
wait = WebDriverWait(driver, 10)
driver.back()
wait = WebDriverWait(driver, 3)
driver.execute_script("window.scrollTo(0, 0);")
wait = WebDriverWait(driver, 2)
#till here


elements = driver.find_elements(By.XPATH, "//p[contains(@style, 'cursor: pointer')]")
eletexts=[x.text for x in elements]
for x in eletexts:
    print(x)
print('now trying to click')

#element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[text()='{elements[3].text}']")))
element=elements[0]
print(element.text)

elements = driver.find_elements(By.XPATH, "//p[contains(@style, 'cursor: pointer')]")
element.click()


#driver.execute_script("arguments[0].scrollIntoView(true);", element)
#driver.execute_script("arguments[0].click();", element)

action = ActionChains(driver)
# Move to the element
action.move_to_element(element).perform()
print('now waiting')
#time.sleep(10)  # Adjust sleep time as needed
# Click the element
print('now trying simple click')
action.click(element).perform()
print('now trying context click')
action.context_click(element).perform();

#element.send_keys(Keys.RETURN)
#element.send_keys(Keys.ENTER)



time.sleep(5)  # Adjust sleep time as needed

print(driver.current_url)

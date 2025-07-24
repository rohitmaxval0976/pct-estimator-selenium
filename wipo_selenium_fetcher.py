
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def fetch_wipo_with_selenium(pct_number):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=options)
        driver.get("https://patentscope.wipo.int/search/en/search.jsf")
        time.sleep(3)

        search_input = driver.find_element(By.ID, "simpleSearchForm:fpSearch:searchField")
        search_input.clear()
        search_input.send_keys(pct_number)

        search_btn = driver.find_element(By.ID, "simpleSearchForm:fpSearch:searchButtonImage")
        search_btn.click()
        time.sleep(5)

        # Click the result link
        result_link = driver.find_element(By.CSS_SELECTOR, "a.searchResultLink")
        result_link.click()
        time.sleep(5)

        # Extract Filing Date
        filing_date = driver.find_element(By.ID, "detailForm:applicationDate").text.strip()

        # Extract Priority Date
        priority_date = driver.find_element(By.ID, "detailForm:priorityDate").text.strip()

        # Extract Claim Count
        try:
            driver.find_element(By.LINK_TEXT, "Claims").click()
            time.sleep(2)
            claims_text = driver.find_element(By.ID, "detailForm:claimsText").text
            claim_count = claims_text.count("claim") + claims_text.count("Claim")
        except:
            claims_text = ""
            claim_count = 0

        # Extract Description
        try:
            driver.find_element(By.LINK_TEXT, "Description").click()
            time.sleep(2)
            description_text = driver.find_element(By.ID, "detailForm:descriptionText").text
        except:
            description_text = ""

        # Abstract
        try:
            abstract_text = driver.find_element(By.ID, "detailForm:abstractText").text
        except:
            abstract_text = ""

        # Word count
        total_words = len(abstract_text.split()) + len(description_text.split()) + len(claims_text.split())

        driver.quit()

        return {
            "filing_date": filing_date,
            "priority_date": priority_date,
            "claim_count": claim_count,
            "word_count": total_words,
            "abstract_word_count": len(abstract_text.split()),
            "description_word_count": len(description_text.split()),
            "claims_word_count": len(claims_text.split())
        }

    except Exception as e:
        return {"error": "Selenium fetch failed", "details": str(e)}

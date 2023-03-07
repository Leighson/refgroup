def document_initialised(driver):
    import time

    time.sleep(2)
    return driver.execute_script("if (document.readyState === 'complete') {return true;} else {window.addEventListener('load', () => {return true;});}")

def scrape_data(driver):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.support.wait import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select

    # find the resulting number of pages
    max_pages = driver.find_element(By.CLASS_NAME, "data-page-max").text
    data = list()

    for _ in range(1, int(max_pages)+1):
        # scrape table headings
        heading_names = list()
        headings = driver.find_elements(By.XPATH, "//thead[@id = 'searchResultsHeader']/tr/th")

        for heading in headings:
            heading_names.append(heading.text)

        # print(heading_names)

        # scrape entries from table
        rows = driver.find_elements(By.XPATH, "//tbody[@id = 'searchResultsPage']/tr")

        for row in rows:
            row_data = list()
            for col in row.find_elements(By.TAG_NAME, "td"):
                row_data.append(col.text)
            data.append(row_data)

        # go to the next page
        driver.find_elements(By.CLASS_NAME, "next")[0].click()
        WebDriverWait(driver, timeout=10).until(document_initialised)
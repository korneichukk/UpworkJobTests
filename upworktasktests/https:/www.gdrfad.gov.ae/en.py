from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

test_data = [
    {
        "id_number": "784198782154748",
        "date_of_birth": "1987-02-12",
        "current_nationality": "india",
    },
    {
        "id_number": "784197538662285",
        "date_of_birth": "1975-07-10",
        "current_nationality": "India",
    },
    {
        "id_number": "784199805295963",
        "date_of_birth": "1998-01-27",
        "current_nationality": "India",
    },
]


def set_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def go_login(driver) -> bool:
    driver.get("https://www.gdrfad.gov.ae/en")

    try:
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.ID, "profileBtn"))
        ).click()
    except Exception as e:
        print(e)
        return False

    driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]/a",
    ).click()

    driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[2]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div/a",
    ).click()

    return True


def set_country(driver, country: str):
    driver.find_element(By.ID, "select2-chosen-1").click()
    option_holder = driver.find_element(By.ID, "select2-results-1")
    options = option_holder.find_elements(By.TAG_NAME, "li")

    for option in options:
        if country.upper() in option.text:
            option.click()
            break


def set_eid(driver, id_number):
    eid = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[1]/div[2]/div[1]/div/div[2]/input",
    )
    eid.clear()
    eid.send_keys(id_number)


def set_doB(driver, date_of_birth):
    dob = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[1]/div[2]/div[2]/div/div[2]/input",
    )
    dob.clear()
    dob.send_keys(date_of_birth)


def solve_captcha(driver):
    iframe = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[2]/div[2]/a/div[1]/div/div/iframe",
    )

    if not iframe:
        print("iframe not found")
        exit(1)

    solver = RecaptchaSolver(driver=driver)
    solver.click_recaptcha_v2(iframe=iframe)


def click_conditions(driver):
    driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[2]/div[4]/div/div[1]/input",
    ).click()


def submit(driver):
    driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[2]/div[4]/input",
    ).click()


def parse_data(driver):
    name_en = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[2]/div/div[1]/div[1]/div[2]/span",
    ).text
    name_ar = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[2]/div/div[1]/div[2]/div[2]/span",
    ).text
    phone_no = driver.find_element(
        By.XPATH,
        "/html/body/form/div[3]/main/div[3]/div/div/div[2]/div/div[3]/div/div[2]/div[2]",
    ).text

    return name_en, name_ar, phone_no


def login(driver, data_item):
    # set eid
    set_eid(driver, data_item.get("id_number"))
    set_country(driver, data_item.get("current_nationality"))
    set_doB(driver, data_item.get("date_of_birth").split("-")[0])
    solve_captcha(driver)
    click_conditions(driver)
    submit(driver)
    time.sleep(5)

    data = parse_data(driver)
    return data


if __name__ == "__main__":
    driver = set_driver()
    for data_item in test_data:
        if not go_login(driver):
            print("login failed. Skip.")
            continue
        data_item_data = login(driver, data_item=data_item)
        data_item_new = data_item
        data_item_new["name_en"] = data_item_data[0]
        data_item_new["name_ar"] = data_item_data[1]
        data_item_new["phone_no"] = data_item_data[2]

        print(data_item_new)

    import json

    with open("data.json", "w") as f:
        json.dump(test_data, f, indent=4)

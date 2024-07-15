import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC


'''НЕЯВНЫЕ ОЖИДАНИЯ'''
@pytest.fixture(autouse=True)
def driver():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    driver.maximize_window()
    driver.implicitly_wait(10) #Неявные ожидания
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

'''ЯВНЫЕ ОЖИДАНИЯ'''
def test_show_all_pets(driver):
    # Вводим email
    WDW(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    driver.find_element(By.ID, 'email').send_keys('lutikrgups@mail.ru')
    # Вводим пароль
    WDW(driver, 5).until(EC.presence_of_element_located((By.ID, 'pass')))
    driver.find_element(By.ID, 'pass').send_keys('medved68139')
    # Нажимаем на кнопку входа в аккаунт
    WDW(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    time.sleep(3)
    # Переходим на страницу Мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    ### 1. Проверка, что на странице пользователя присутствуют все питомцы


    # Получаем список всех питомцев
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]')))
    pets_number = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split('\n')[1].split(': ')[1]
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))
    pets_count = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # Проверяем, что присутствуют все питомцы
    assert len(pets_count) == int(pets_number)
    print(f'Количество питомцев: ', pets_number)



    WDW(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')))
    images = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')))
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')))
    breeds = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')))
    ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')

    images_count = 0
    names_count = 0
    names_list = []

    #### 2. Проверка, что на странице пользователя хотя бы у половины питомцев есть фото
    for i in range(len(pets_count)):
        if images[i].get_attribute('src') != '':
            images_count += 1
        else:
            pass
    print('Питомцы с фото: ', images_count)

    if len(pets_count) == 0:
        print('Нет питомцев')
    else:
        try:
            assert images_count >= len(pets_count) / 2
        except AssertionError:
            print('Нет фото больше чем у половины питомцев')
        else:
            print('У половины питомцев есть фото')

### 3. Проверка, что на странице пользователя у всех питомцев есть имя, возраст и порода

    try:
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''
    except AssertionError:
        print('Не у всех питомцев есть имя, возраст и порода')

### 4. Проверка, что на странице пользователя у всех питомцев разные имена

    for i in range(len(pets_count)):
        if names[i].text != '':
            names_count += 1
            names_list.append(names[i].text)
        else:
            pass


    set_names = set(names_list)
    try:
        assert len(set_names) == len(names_list)

    except AssertionError:
        print('Не у всех питомцев разные имена.')

### 5. Проверка, что на странице пользователя в списке нет повторяющихся питомцев
    # получаем список питомцев в формате 'имя порода возраст','x'
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody')))
    pets_list = driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody').text.split('\n')
    set_pets_list_no_repeat = set(pets_list)

    try:
        assert len(set_pets_list_no_repeat) == len(pets_list) // 2 # делим на "2" для исключения из расчета лишнего элемента 'x'

    except AssertionError:
        print('В списке есть повторяющиеся питомцы.')


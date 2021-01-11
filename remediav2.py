from selenium import webdriver
import pandas as pd
import time
browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe') ## CAMBIAR

medicamentos = ['Amlodipine',
                'Amoxicillin',
                'Anastrozole',
                'Atorvastatin',
                'Azithromycin',
                'Azithromycin',
                'Fluoxetine',
                'Lamotrigine',
                'Letrozole',
                'Losartan',
                'Metformin',
                'Sertraline',
                'Terbinafine']

comunas = ['Independencia','La Florida','Maipu']
comuna = 'Independencia' ### CAMBIAR ESTO

products = []
locales = []
medicamento_df = []

url = 'https://www.remedia.cl/precios'
#browser.get(url)
#time.sleep(5)

for medicamento in medicamentos:
    try:
        browser.get(url)
        time.sleep(5)
        path_medicamento = r"/html/body/app-root/ion-app/ion-split-pane/ion-router-outlet/ion-tabs/div/ion-router-outlet/app-prices/ion-content/ion-searchbar/div/input"
        elem = browser.find_element_by_xpath(path_medicamento)
        elem.click()
        elem.send_keys(medicamento)
        time.sleep(5)
        containers = browser.find_elements_by_xpath("//ion-item[@class='item md in-list ion-focusable item-label hydrated']")
        
        for container in containers:
            try:
                browser.execute_script("arguments[0].scrollIntoView();", container)
                time.sleep(5)
                container.click()
                time.sleep(3)
    
                try:
                    elem = browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-split-pane/ion-router-outlet/ion-tabs/div/ion-router-outlet/app-results/ion-content/div/ion-item/ion-label/ion-text")
                    elem.click()
                    time.sleep(3)
    
                    active_ele = browser.switch_to.active_element
                    active_ele.send_keys(comuna) 
                    time.sleep(3)
                    
                    elem = browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-modal/div/app-geo-config/ion-content/ion-list/ion-item[2]/ion-label")
                    elem.click()
                    time.sleep(3)
                    
                    #time.sleep(3)
                    #browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-modal/div/app-geo-config/ion-header/ion-toolbar/ion-buttons/ion-button//button/span").click()
                except:
                    pass
    
                time.sleep(10)
                mini_containers = browser.find_elements_by_xpath("//ion-card[@class='md hydrated']")
                for mini in mini_containers:
                    browser.execute_script("arguments[0].scrollIntoView();", mini)
                    time.sleep(3)
                    mini.click()
                    time.sleep(3)
                    medicamento_df.append(medicamento)
                    try:
                        product = browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-modal/div/app-price-item/ion-content/ion-card/ion-item[1]/ion-label/ion-item/ion-label").text
                        products.append(product)
                    except:
                        products.append(None)
    
                    try:
                        local = browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-modal/div/app-price-item/ion-content/ion-card/ion-item[3]/ion-badge").text
                        locales.append(local)
                    except:
                        locales.append(None)
    
                    time.sleep(3)
                    browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-modal/div/app-price-item/ion-header/ion-toolbar/ion-buttons[2]/ion-button").click()
    
                time.sleep(3)
                browser.find_element_by_xpath("/html/body/app-root/ion-app/ion-split-pane/ion-router-outlet/ion-tabs/div/ion-router-outlet/app-results/ion-header/ion-toolbar/ion-buttons[1]/ion-back-button").click()
            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)
        pass
        
df = pd.DataFrame(list(zip(medicamento_df, products, locales)), 
                  columns =['medicamento', 'products', 'locales'])
df.to_csv('datos_%s.csv'%comuna) 
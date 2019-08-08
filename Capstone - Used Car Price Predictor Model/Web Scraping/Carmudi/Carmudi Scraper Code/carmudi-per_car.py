#############################################################################################
######################################### LIBRARIES #########################################
#############################################################################################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver import ActionChains

import os
import pandas as pd






#############################################################################################
######################################### MAIN CODE #########################################
#############################################################################################


##################################
##### Creating the Dataframe #####

### List of categories / features
primaryDetails_fields = ['colorFamily', 'doors', 'driveType', 'edition']
generalCategories_fields = ['interior', 'exterior', 'equipment', 'description']
sellerInfos_fields = ['sellerName', 'sellerType', 'sellerLocation']

### Make column list of categories / features for the creation of dataframe
column_list = ['webPage', 'listingID', 'postedDate', 'title', 'price', 'negotiable', 'featured', 'mileage', 'transmission', 'fuelType', 'engineSize']

for p in primaryDetails_fields:
	column_list.append(p)

for g in generalCategories_fields:
	column_list.append(g)

for s in sellerInfos_fields:
	column_list.append(s)

### Create empty dataframe
df = pd.DataFrame(columns=column_list)


######################################################################
##### Import text file containing list of webpages to be scraped #####

list_wpg = []
with open('Desktop/list_wpg.txt') as a:
    list_wpg = a.readlines()
list_wpg = [x.rstrip('\n') for x in list_wpg] 
print list_wpg


####################################
##### Chromedriver and Browser #####

dirpath = os.getcwd()
filepath = dirpath + '/chromedriver'
print 'Path to Driver: ', filepath

#####################################
##### Run function for scraping #####

for wpg in list_wpg:

	print ""	
	print "################################################################################"

	browser = webdriver.Chrome(executable_path = filepath)    
	#wpg = "https://www.carmudi.com.ph/2018-toyota-hiace-3-1252749-36.html"
	print wpg
	browser.get(wpg)


	##################
	##### Scrape #####

	try:
		loaded = WebDriverWait(browser, 500).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-container"]')))
		ActionChains(browser).move_to_element(loaded).perform()
		#sleep(1)


		### Featured
		try:
			ifFeatured = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-featured')))
			ActionChains(browser).move_to_element(ifFeatured).perform()
			featured = 1
		except Exception as e:
			featured = 0

		
		### Title
		try:
			listingTitle = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-listing-title')))
			ActionChains(browser).move_to_element(listingTitle).perform()
			title = listingTitle.text
		except Exception as e:
			print "Listing title exception: ", e
			title = ''
		

		### Price
		try:
			listingPrice = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-listing-price')))
			ActionChains(browser).move_to_element(listingPrice).perform()
			price = listingPrice.get_attribute('innerHTML').encode('utf-8')
		except Exception as e:
			print "Listing price exception:", e
			price = ''
			

		### Negotiable
		try:
			c_negotiable = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-negotiable')))
			ActionChains(browser).move_to_element(c_negotiable).perform()
			negotiable = c_negotiable.text
		except Exception as e:
			print "Negotiable exception:", e
			negotiable = ''


		### Basic Car Details: Mileage, Fuel Type, Transmission, Engine Size
		mileage = ''
		transmission = ''
		fuelType = ''
		engineSize = ''

		try:
			basic_details = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-container"]/div[1]/div[1]/div[1]/div[4]/div[3]/div')))
			ActionChains(browser).move_to_element(basic_details).perform()
			#sleep(1)

			basic_details_fields = basic_details.find_elements_by_class_name("c-basic-car-details__container")

			for a in basic_details_fields:
				attribute_name = str(a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//small").get_attribute('innerHTML'))

				if 'Mileage' in attribute_name:
					mileage = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML')

				if 'Transmission' in attribute_name:
					transmission = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML')
				
				if 'Fuel type' in attribute_name:
					fuelType = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML')

				if 'Engine size' in attribute_name:
					engineSize = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML')

		except Exception as e:
			print "Basic car details exception:", e


		### Primary Details: Color Family, Doors, Drive Type, Edition 
		colorFamily = ''
		doors = ''
		driveType = ''
		edition = ''

		try:
			primary_details = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-primary-details"]')))
			ActionChains(browser).move_to_element(primary_details).perform()
			#sleep(1)

			primary_details_fields = primary_details.find_elements_by_class_name("py-1")

			for a in primary_details_fields:
				attribute_name = str(a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML'))

				if 'Color Family' in attribute_name:
					colorFamily = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML')

				if 'Doors' in attribute_name:
					doors = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML')
				
				if 'Drive Type' in attribute_name:
					driveType = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML')

				if 'Edition' in attribute_name:
					edition = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML')
					
		except Exception as e:
			print "Primary details exception:", e


		### List of Interiors
		interior = []

		try:
			interior_card = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-interior"]')))
			ActionChains(browser).move_to_element(interior_card).perform()
			#sleep(1)

			interiors = interior_card.find_elements_by_class_name("py-1")

			for a in interiors:
				isYes = str(a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML'))

				if 'Yes' in isYes:
					get_interior = a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8').lower()
					interior.append(get_interior)
					
		except Exception as e:
			print "Interior List exception:", e


		### List of Exteriors
		exterior = []

		try:
			exterior_card = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-exterior"]')))
			ActionChains(browser).move_to_element(exterior_card).perform()
			#sleep(1)

			exteriors = exterior_card.find_elements_by_class_name("py-1")

			for a in exteriors:
				isYes = str(a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML'))

				if 'Yes' in isYes:
					get_exterior = a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8').lower()
					exterior.append(get_exterior)
					
		except Exception as e:
			print "Interior List exception:", e


		### List of Equipments
		equipment = []

		try:
			equipment_card = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-equipment"]')))
			ActionChains(browser).move_to_element(equipment_card).perform()
			#sleep(1)

			equipments = equipment_card.find_elements_by_class_name("py-1")

			for a in equipments:
				isYes = str(a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML'))

				if 'Yes' in isYes:
					get_equipment = a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8').lower()
					equipment.append(get_equipment)
					
		except Exception as e:
			print "Interior List exception:", e


		### Seller's Description 
		description = ''

		try:
			description_card = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-seller\'s-description"]')))
			ActionChains(browser).move_to_element(description_card).perform()

			description = description_card.find_element_by_class_name("w-100").text

		except Exception as e:
			print "Seller's Description exception:", e


		### Seller Information
		sellerName = ''
		sellerType = ''
		sellerLocation = ''

		try:
			seller_card = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-seller-details')))
			ActionChains(browser).move_to_element(seller_card).perform()
			#sleep(1)

			sellerInfos = seller_card.find_element_by_class_name("px-3")

			sellerName = sellerInfos.find_element_by_xpath(".//a[1]").get_attribute('title')
			sellerType = sellerInfos.find_element_by_xpath(".//div[1]/img").get_attribute('alt')
			sellerLocation = sellerInfos.find_element_by_xpath(".//div[2]/span").get_attribute('title')

		except Exception as e:
			print "Seller Information exception:", e


		### Listing ID and Posted Date
		listingID = ''
		postedDate = ''

		try:
			card = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-listing-technical-details')))
			ActionChains(browser).move_to_element(card).perform()
			#sleep(1)

			listings = card.find_elements_by_class_name("my-2")

			for l in listings:
				label = l.find_element_by_xpath(".//strong").get_attribute('innerHTML')

				if 'Listing ID' in label:
					listingID = l.find_element_by_xpath(".//span").get_attribute('innerHTML')
				if 'Posted date' in label:
					postedDate = l.find_element_by_xpath(".//span").get_attribute('innerHTML')
		except Exception as e:
			print "Listing ID / Date exception:", e


		### Print all data gathered
		print "------------------------------------------------------------------------"
		print "Listing ID:", listingID
		print "Posted Date:", postedDate
		print "Title:", title
		print "Price:", price
		print "Featured:", featured
		print "Negotiable:", negotiable
		print "------------------------------------------------------------------------"
		print "Mileage:", mileage
		print "Transmission:", transmission
		print "Fuel Type:", fuelType
		print "Engine Size:", engineSize
		print "------------------------------------------------------------------------"
		print "Primary Details"
		print "     Color Family:", colorFamily
		print "     Doors:", doors
		print "     Drive Type:", driveType
		print "     Edition:", edition
		print "------------------------------------------------------------------------"
		print "Interior:", interior
		print "Exterior:", exterior
		print "Equipment:", equipment
		print "Description:", description
		print "------------------------------------------------------------------------"
		print "About the Seller"
		print "     Name:", sellerName
		print "     Type:", sellerType
		print "     Location:", sellerLocation
		print "------------------------------------------------------------------------"
		

		### Save into new_entry that will be appended to the dataframe
		new_entry = {'webPage': wpg, 'listingID': listingID, 'postedDate': postedDate, 'title': title, 'price': price, 'negotiable': negotiable, 'featured': featured, 
		'mileage': mileage, 'transmission': transmission, 'fuelType': fuelType, 'engineSize': engineSize, 
		'colorFamily': colorFamily, 'doors': doors, 'driveType': driveType, 'edition': edition,
		'interior': interior, 'exterior': exterior, 'equipment': equipment, 'description': description, 
		'sellerName': sellerName, 'sellerType': sellerType, 'sellerLocation': sellerLocation}

		df = df.append(new_entry, ignore_index=True)
		print "df shape:", df.shape

	except Exception as e:
		print "Error occured:", e
		browser.quit()

	finally:
		print "Finished", wpg
		browser.quit()


#######################################
##### Export the dataframe to CSV #####

savepath = "C:/Users/acelo/Desktop/carmudi.csv"
carmudi = df.to_csv(savepath, index=None, header=True)

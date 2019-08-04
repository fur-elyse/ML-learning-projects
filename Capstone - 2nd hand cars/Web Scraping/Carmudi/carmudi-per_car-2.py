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
import numpy as np

from collections import deque





#############################################################################################
########################################## SET UP ###########################################
#############################################################################################

### File path of CSV file containing links of car pages
carLinksCSV = "Desktop/Book1.csv"

### Path/Location of Chromedriver
dirpath = os.getcwd()
filepath = dirpath + '/chromedriver'

### File name and path/location where the dataframe will be exported to CSV
filename = "carmudi-toyota.csv"
savepath = "C:/Users/acelo/Desktop/" + filename





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
column_list = ['webPage', 'listingID', 'postedDate', 'title', 'brand', 'condition', 'price', 'negotiable', 'featured', 'mileage', 'transmission', 'fuelType', 'engineSize']

for p in primaryDetails_fields:
	column_list.append(p)

for g in generalCategories_fields:
	column_list.append(g)

for s in sellerInfos_fields:
	column_list.append(s)

### Create empty dataframe
df = pd.DataFrame(columns=column_list)


#####################################################################
##### Import CSV file containing list of webpages to be scraped #####

#list_wpg_csv = []
df_wpg = pd.read_csv(carLinksCSV)


####################################
##### Chromedriver and Browser #####

print 'Path to Driver: ', filepath


#####################################
##### Run function for scraping #####

for rowNum in range(0,len(df_wpg.index)):

	print ""
	print "################################################################################"

	brand = df_wpg.iat[rowNum, 1]
	condition = df_wpg.iat[rowNum, 2]
	wpg = df_wpg.iat[rowNum, 3]


	##################
	##### Scrape #####

	try:
		browser = webdriver.Chrome(executable_path = filepath)    
		#wpg = "https://www.carmudi.com.ph/2018-toyota-hiace-3-1252749-36.html"
		print wpg
		browser.get(wpg)

		loaded = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-container"]/div[1]')))
		#ActionChains(browser).move_to_element(loaded).perform()
		#sleep(1)


		### Featured
		try:
			ifFeatured = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-featured')))
			#ActionChains(browser).move_to_element(ifFeatured).perform()
			featured = 1
		except Exception as e:
			featured = 0

		
		### Title
		try:
			listingTitle = loaded.find_element_by_class_name("c-listing-title") #WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-listing-title')))
			#ActionChains(browser).move_to_element(listingTitle).perform()
			title = listingTitle.text.encode('utf-8')
		except Exception as e:
			print "Listing title exception: ", e
			title = ''
		

		### Price
		try:
			listingPrice = loaded.find_element_by_class_name("c-listing-price") #WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-listing-price')))
			#ActionChains(browser).move_to_element(listingPrice).perform()
			price = listingPrice.get_attribute('innerHTML').encode('utf-8')
		except Exception as e:
			print "Listing price exception:", e
			price = ''
			

		### Negotiable
		try:
			c_negotiable = loaded.find_element_by_class_name("c-negotiable") #WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-negotiable')))
			#ActionChains(browser).move_to_element(c_negotiable).perform()
			negotiable = c_negotiable.text.encode('utf-8')
		except Exception as e:
			print "Negotiable exception:", e
			negotiable = ''


		### Basic Car Details: Mileage, Fuel Type, Transmission, Engine Size
		mileage = ''
		transmission = ''
		fuelType = ''
		engineSize = ''

		try:
			basic_details = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-container"]/div[1]/div[1]/div[1]/div[4]/div[3]/div')))
			#ActionChains(browser).move_to_element(basic_details).perform()
			#sleep(1)

			basic_details_fields = basic_details.find_elements_by_class_name("c-basic-car-details__container")

			for a in basic_details_fields:
				attribute_name = str(a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//small").get_attribute('innerHTML'))

				if 'Mileage' in attribute_name:
					mileage = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML').encode('utf-8')

				if 'Transmission' in attribute_name:
					transmission = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML').encode('utf-8')
				
				if 'Fuel type' in attribute_name:
					fuelType = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML').encode('utf-8')

				if 'Engine size' in attribute_name:
					engineSize = a.find_element_by_class_name("c-basic-car-details__attribute").find_element_by_xpath(".//span").get_attribute('innerHTML').encode('utf-8')

		except Exception as e:
			print "Basic car details exception:", e


		### Primary Details: Color Family, Doors, Drive Type, Edition 
		colorFamily = ''
		doors = ''
		driveType = ''
		edition = ''

		try:
			primary_details = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-primary-details"]')))
			#ActionChains(browser).move_to_element(primary_details).perform()
			#sleep(1)

			primary_details_fields = primary_details.find_elements_by_class_name("py-1")

			for a in primary_details_fields:
				attribute_name = str(a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML'))

				if 'Color Family' in attribute_name:
					colorFamily = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML').encode('utf-8')

				if 'Doors' in attribute_name:
					doors = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML').encode('utf-8')
				
				if 'Drive Type' in attribute_name:
					driveType = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML').encode('utf-8')

				if 'Edition' in attribute_name:
					edition = a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML').encode('utf-8')
					
		except Exception as e:
			print "Primary details exception:", e


		### List of Interiors
		interior = []
		dq_interior = deque()

		try:
			interior_card = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-interior"]')))
			#ActionChains(browser).move_to_element(interior_card).perform()
			#sleep(1)

			interiors = interior_card.find_elements_by_class_name("py-1")

			for a in interiors:
				isYes = str(a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML'))

				if 'Yes' in isYes:
					get_interior = a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8').lower().encode('utf-8')
					#interior.append(get_interior)
					dq_interior.appendleft(get_interior)

			interior = list(dq_interior)
					
		except Exception as e:
			print "Interior List exception:", e


		### List of Exteriors
		exterior = []
		dq_exterior = deque()

		try:
			exterior_card = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-exterior"]')))
			#ActionChains(browser).move_to_element(exterior_card).perform()
			#sleep(1)

			exteriors = exterior_card.find_elements_by_class_name("py-1")

			for a in exteriors:
				isYes = str(a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML'))

				if 'Yes' in isYes:
					get_exterior = a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8').lower().encode('utf-8')
					#exterior.append(get_exterior)
					dq_exterior.appendleft(get_exterior)

			exterior = list(dq_exterior)
					
		except Exception as e:
			print "Exterior List exception:", e


		### List of Equipments
		equipment = []
		dq_equipment = deque()

		try:
			equipment_card = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-equipment"]')))
			#ActionChains(browser).move_to_element(equipment_card).perform()
			#sleep(1)

			equipments = equipment_card.find_elements_by_class_name("py-1")

			for a in equipments:
				isYes = str(a.find_element_by_xpath(".//div[2]").get_attribute('innerHTML'))

				if 'Yes' in isYes:
					get_equipment = a.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8').lower().encode('utf-8')
					#equipment.append(get_equipment)
					dq_equipment.appendleft(get_equipment)

			equipment = list(dq_equipment)
					
		except Exception as e:
			print "Equipment List exception:", e


		### Seller's Description 
		description = ''

		try:
			description_card = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-c-seller\'s-description"]')))
			#ActionChains(browser).move_to_element(description_card).perform()

			description = description_card.find_element_by_class_name("w-100").text.encode('utf-8')

		except Exception as e:
			print "Seller's Description exception:", e


		### Seller Information
		sellerName = ''
		sellerType = ''
		sellerLocation = ''

		try:
			seller_card = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-seller-details')))
			#ActionChains(browser).move_to_element(seller_card).perform()
			#sleep(1)

			sellerInfos = seller_card.find_element_by_class_name("px-3")

			sellerName = sellerInfos.find_element_by_tag_name("h3").get_attribute('innerHTML').encode('utf-8') #sellerInfos.find_element_by_xpath(".//a[1]").get_attribute('title').encode('utf-8')
			sellerType = sellerInfos.find_element_by_xpath(".//div[1]/strong").get_attribute('innerHTML').encode('utf-8')
			sellerLocation = sellerInfos.find_element_by_xpath(".//div[2]/span").get_attribute('title').encode('utf-8')

		except Exception as e:
			print "Seller Information exception:", e


		### Listing ID and Posted Date
		listingID = ''
		postedDate = ''

		try:
			card = loaded.find_element_by_class_name('c-listing-technical-details') #WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-listing-technical-details')))
			#ActionChains(browser).move_to_element(card).perform()
			#sleep(1)

			listings = card.find_elements_by_class_name("my-2")

			for l in listings:
				label = l.find_element_by_xpath(".//strong").get_attribute('innerHTML')

				if 'Listing ID' in label:
					listingID = l.find_element_by_xpath(".//span").get_attribute('innerHTML').encode('utf-8')
				if 'Posted date' in label:
					postedDate = l.find_element_by_xpath(".//span").get_attribute('innerHTML').encode('utf-8')

		except Exception as e:
			print "Listing ID / Date exception:", e


		### Save into new_entry that will be appended to the dataframe
		new_entry = {'webPage': wpg, 'listingID': listingID, 'postedDate': postedDate, 
		'title': title, 'brand': brand, 'condition': condition, 'price': price, 'negotiable': negotiable, 'featured': featured, 
		'mileage': mileage, 'transmission': transmission, 'fuelType': fuelType, 'engineSize': engineSize, 
		'colorFamily': colorFamily, 'doors': doors, 'driveType': driveType, 'edition': edition,
		'interior': interior, 'exterior': exterior, 'equipment': equipment, 'description': description, 
		'sellerName': sellerName, 'sellerType': sellerType, 'sellerLocation': sellerLocation}

		df = df.append(new_entry, ignore_index=True)


		### Print all data gathered
		print "------------------------------------------------------------------------"
		print "Listing ID:", listingID
		print "Posted Date:", postedDate
		print "Title:", title
		print "Brand:", brand
		print "Condition:", condition
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
		

	except Exception as e:
		print "Error occured:", e
		#browser.quit()


	print "df shape:", df.shape
	print "Finished", wpg
	
	browser.quit()


#######################################
##### Export the dataframe to CSV #####

carmudi = df.to_csv(savepath, index=None, header=True)

print "DF saved as", savepath

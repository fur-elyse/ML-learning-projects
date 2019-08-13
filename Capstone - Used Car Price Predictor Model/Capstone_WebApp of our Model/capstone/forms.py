
###############################################
#################### FORMS ####################
###############################################



##### For Django #####
from django import forms

##### Others #####
import json
import os



##### Get dictionary of data #####
dirpath = os.getcwd() 
with open(dirpath+'\\capstone\\static\\capstone\\label_encode.json', 'r') as f:
	le = json.load(f)



##### Class for Car Form at Home page #####
class CarForm(forms.Form):
	brand = forms.ChoiceField(choices=[(le['encode']['brand'][l], l) for l in le['encode']['brand'].keys()], 
								widget=forms.Select(attrs={
									'name':'brand', 'class':'form-control', 'data-live-search':"true"}))

	model = forms.ChoiceField(choices=[(le['encode']['model'][l], l) for l in le['encode']['model'].keys()],
								widget=forms.Select(attrs={
									'name':'model', 'class':'form-control', 'data-live-search':"true"}))

	body_type = forms.ChoiceField(choices=[(le['encode']['body_type'][l], l) for l in le['encode']['body_type'].keys()], 
								widget=forms.Select(attrs={
									'name':'body_type', 'class':'form-control', 'data-live-search':"true"}))

	age_of_car = forms.IntegerField(widget=forms.NumberInput(attrs={
									'class':'form-control', 'name':'age_of_car'}))

	mileage_in_km = forms.IntegerField(widget=forms.NumberInput(attrs={
									'class':'form-control', 'name':'mileage_in_km'}))

	retail = forms.IntegerField(widget=forms.NumberInput(attrs={
									'class':'form-control', 'name':'retail'}))

	color = forms.ChoiceField(choices=[(le['encode']['color'][l], l) for l in le['encode']['color'].keys()], 
								widget=forms.Select(attrs={
									'name':'color', 'class':'form-control', 'data-live-search':"true"}))

	location = forms.ChoiceField(choices=[(le['encode']['location'][l], l) for l in le['encode']['location'].keys()], 
								widget=forms.Select(attrs={
									'name':'location', 'class':'form-control',  'data-live-search':"true"}))

	transmission = forms.ChoiceField(choices=[(le['encode']['transmission'][l], l) for l in le['encode']['transmission'].keys()], 
								widget=forms.RadioSelect(attrs={
									'name':'transmission'}))

	fuel_type = forms.ChoiceField(choices=[(le['encode']['fuel_type'][l], l) for l in le['encode']['fuel_type'].keys()], 
								widget=forms.RadioSelect(attrs={
									'name':'fuel_type', 'class':'form-control',  'data-live-search':"true"}))

	post_age_in_days = forms.IntegerField(widget=forms.NumberInput(attrs={
								'class':'form-control', 'name':'post_age_in_days'}))

	poster_type = forms.ChoiceField(choices=[(le['encode']['poster_type'][l], l) for l in le['encode']['poster_type'].keys()], 
								widget=forms.RadioSelect(attrs={
									'name':'poster_type', 'class':'form-control', 'data-live-search':"true"}))
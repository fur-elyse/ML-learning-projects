
##########################################################
#################### Import Libraries ####################
##########################################################

##### For Django #####
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CarForm

##### For Machine Learning #####
import numpy as np
import pandas as pd
import os
from sklearn.externals import joblib
import pickle
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV


###################################################
#################### Functions ####################
###################################################

# Create your views here.

###### Home page / Main #####
def home(request):

	context = {"title": "Home", "form": CarForm(), "predicted": 0}

	if request.method == 'POST':
		form = CarForm(request.POST)
		if form.is_valid():
			print("##############\n", form.cleaned_data, "\n############")	
			context["predicted"] = predict(form.cleaned_data)

	return render(request, 'capstone/home.html', context)


##### Function for prediction #####

def predict(data):
	data_df = pd.DataFrame({0:data}).transpose()
	#data_df["age_of_car"] = 2019 - data_df.loc[0,"year"]
	#data_df.drop(columns=['year'],inplace=True,axis=1)

	print(data_df)

	dirpath = os.getcwd() 
	#model = joblib.load(dirpath+'\\capstone\\static\\capstone\\rf_jl')	
	pkl_path = dirpath+'\\capstone\\static\\capstone\\rforest.pkl'
	with open(pkl_path, 'rb') as pkl_file:
		model = pickle.load(pkl_file)

	predicted_log = model.predict(data_df)

	return np.exp(predicted_log[0])

from django.shortcuts import render,HttpResponse
import requests
from .models import Crop,FarmersQuery
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .ml.ml_algo import * 

w_key = "4c14c1a61b22493a98a122059191012"
latitude = 0
longitude = 0
# Create your views here.
def home(request):
    context = {}
    return render(request,"home.html",context)
@csrf_exempt
def example(request):
    global latitude
    global longitude
    latitude = request.POST['lat']
    longitude = request.POST['long']
    # latitude = "19.997454"
    # longitude = "73.789803"
    return HttpResponse("OK")


def result(request):
    if request.method == "POST":
        startdate = "2009-07-22"
        enddate = "2009-09-22"
        # response = requests.get('http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + str(w_key) + '&q='+ str(latitude) + ',' + str(longitude) + '&fx24=yes&date=' + startdate + '&tp=24&enddate='+ enddate + '&mca=yes&format=json')
        response = requests.get('http://api.worldweatheronline.com/premium/v1/weather.ashx?key=' + str(w_key) + '&q='+ str(latitude) + ',' + str(longitude) + '&fx=no&mca=yes&cc=no&format=json')
        print(response)
        rainfall = response.json()['data']['ClimateAverages'][0]['month']
        rainfall_values = []
        temp = []
        
        for i in range(0,12):
            # print("Avg: ", rainfall[i]['avgDailyRainfall'])
            rainfall_values.append(float(rainfall[i]['avgDailyRainfall'])*30)
            temperature = (float(rainfall[i]['avgMinTemp']) + float(rainfall[i]['absMaxTemp']))/2
            temp.append(temperature)

        
    context = {'data': setData(rainfall_values,temp,"Rajasthan")}
    return render(request, "result.html", context)

def getDetails(cropName):
    details = {}
    try:
        import pandas as pd
        data = pd.read_csv('basicApp/code/crop-details.csv')
        # data = data.loc[data['Crop'] == cropName, 11:].values
        data = data.loc[data['Crop'] == cropName]
        value = data.iloc[:, 11].values[0]
        if value.find('*') == -1:
            details['Sowing Time'] = value
        value = data.iloc[:, 12].values[0]
        if value.find('*') == -1:
            details['Irrigation Time'] = value
        value = data.iloc[:, 13].values[0]
        if value.find('*') == -1:
            details['Weeding Time'] = value
        value = data.iloc[:, 14].values[0]
        if value.find('*') == -1:
            details['Harvesting Time'] = value
        value = data.iloc[:, 15].values[0]
        if value.find('*') == -1:
            details['Additional Details'] = value
        return details
    except:
        return {'no crop named ' + cropName : ' exsist in our database'}

def cropDetails(request):
    try:
        context = {'data' : getDetails(request.GET['name'])}
        return render(request, "crop-detail.html", context)
    except:
        return HttpResponse("<h1>I think You Are Lost</h1>")
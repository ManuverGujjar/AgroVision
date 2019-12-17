from django.shortcuts import render,HttpResponse
import requests
from .models import Crop,FarmersQuery
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .ml.ml_algo import * 
from django.utils.encoding import smart_str

w_key = "4c14c1a61b22493a98a122059191012"
latitude = 0
longitude = 0
state = ""
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
    global state
    state = request.POST['state']
    
    # latitude = "19.997454"
    # longitude = "73.789803"
    return HttpResponse("OK")


def result(request):
    if request.method == "GET":
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

    print("state ;", state) 
    context = {'data': setData(rainfall_values,temp, state)}
    return render(request, "result.html", context)

def getDetails(cropName):
    details = {}
    try:
        from datetime import datetime  
        from datetime import timedelta

        import pandas as pd
        
        data = pd.read_csv('basicApp/code/crop-details.csv')
        # data = data.loc[data['Crop'] == cropName, 11:].values
        data = data.loc[data['Crop'] == cropName]
        value = data.iloc[:, 11].values[0]
        if value.find('*') == -1:
            details['Sowing Time'] = f"You should sow {cropName} around "+ str(datetime.now() + timedelta(days=int(value)))[:10]
        value = data.iloc[:, 12].values[0]
        if value.find('*') == -1:
            details['Irrigation Time'] = f"You should irrigate {cropName} around "+ str(datetime.now() + timedelta(days=int(value)))[:10]

        value = data.iloc[:, 13].values[0]
        if value.find('*') == -1:
            details['Weeding Time'] = f"You should start pulling unwanted crops {cropName} around "+ str(datetime.now() + timedelta(days=int(value)))[:10]
        value = data.iloc[:, 14].values[0]
        if value.find('*') == -1:
            details['Harvesting Time'] = f"Start harvesting {cropName} around "+ str(datetime.now() + timedelta(days=int(value)))[:10]
        value = data.iloc[:, 15].values[0]
        if value.find('*') == -1:
            details['Additional Details'] = value
        return details
    except Exception as e:
        print(e)
        return {'no crop named ' + cropName : ' exsist in our database'}

def cropDetails(request):
    try:
        context = {'data' : getDetails(request.GET['name']), 'cropName': request.GET['name']}
        return render(request, "crop-detail.html", context)
    except Exception as e:
        print(e)
        return HttpResponse("<h1>I think You Are Lost</h1>")
    

def getPdf(request):
    try:
        pdfPath = 'basicApp/pdfs/'
        from googlesearch import search
        import pdfkit as pdf
        filename = request.GET['name'] + '.pdf'
        filePath = pdfPath + filename
        file = None
        try:
            file = open(filePath, 'r')
        except Exception as e:
            print(e)
            try:
                for result in search("how to cultivate " + str(request.GET['name']),tld="co.in", num=1, stop=1, pause=1):
                    pdf.from_url(result, filePath)
            except Exception as e:
                print(99, e)
                
        finally:
            try:
                from django.views.static import serve
                return serve(request, os.path.basename(filePath), os.path.dirname(filePath))
            except Exception as e:
                print(e)


    except Exception as e:
        print(e)
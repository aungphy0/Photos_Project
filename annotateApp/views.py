from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
#import PIL.Image
from GPSPhoto import gpsphoto
import reverse_geocoder as rg
import pprint
import geopy
from geopy.geocoders import Nominatim
#get the metadata of the image
import pymysql
import os

def index(request):
    images = os.listdir('media/photos')
    return render(request, 'annotateApp/index.html', {'images' : images})

def saveimage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
            s = name
            s1 = 'media/photos/' + str(s)

            form.save()
            ls = getImage(s1)
            insert(ls[0], ls[1], ls[2], ls[3], ls[4])
            return redirect('index')
    else:
        form = ImageForm()

    return render(request, 'annotateApp/saveimage.html', {'form' : form})
    # num = 9
    # s = 'media/photos/IMG-9.JPG'
    # ls = getImage(s)
    # #print(ls[0])
    # insert(ls[0], ls[1], ls[2], ls[3], ls[4])
    # return render(request, 'annotateApp/saveimage.html',{'num': ls})


def getImage(filepath):
    img = filepath
    data = gpsphoto.getGPSData(img)
    s = img.split("/")
    img_path = s[1] + "/" + s[2]
    lat = data['Latitude']
    lon = data['Longitude']
    #time = data['UTC-Time'] + " " + data['Date']
    time = data['Date']
    #print(data)
    coordinates = (data['Latitude'], data['Longitude'])
    # result = rg.search(coordinate)
    # r = dict(result[0])
    # print(r['admin2'])

    locator = Nominatim(user_agent='myGeocoder')
    #coordinates = “53.480837, -2.244914”
    #for i in range(10):
    location = locator.reverse(coordinates)
    # name = location.raw['display_name']
    # n = name.split(",")
    # d_name = n[0] + n[1]
    p_id = location.raw['place_id']
    return [p_id, lat, lon, time, img_path]

def insert(place_id, lat, lon, time, image):
    print("Inserting image into photos table")
    try:
        connection = pymysql.connect(host='localhost',
                                     database='Metadata',
                                     user='root',
                                     password='')

        cursor = connection.cursor()
        sql_insert = """ INSERT INTO annotateApp_data
                           (place_id, lat, lon, time, image) VALUES (%s,%s,%s,%s,%s)"""


        picture = image
        # Convert data into tuple format
        insert_data = (place_id, lat, lon, time, picture)
        result = cursor.execute(sql_insert, insert_data)
        connection.commit()
        print("Image inserted successfully into photos table", result)

    except pymysql.Error as error:
        print("error pymysql %d: %s" %(e.args[0], e.args[1]))


    finally:
        #if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
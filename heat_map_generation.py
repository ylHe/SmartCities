from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import gmaps
import gmaps.datasets
import pandas as pd
import numpy as np
import download_files_from_drive
from ipywidgets.embed import embed_minimal_html

credFile = 'mycreds.txt'
mimetype = 'text/csv'
camlistfile = '1E81xv8S3neRQJR5uXa9eptQf0ZV5cJTc'
gmapsApiKey = 'AIzaSyCxPhdzmarsSOCWOzOuktzYJy9W5HWwJpI'
mapCenter = (18.591363, 73.738929)
csv_file_content = ""

def isStartTimeSmaller(start,end):
    if (start < end):
        return True
    else:
        return False

def get_csv_content_from_drive():
    return download_files_from_drive.download_csv_content()

def getTrafficData(fileid):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credFile)
    drive = GoogleDrive(gauth)
    file2 = drive.CreateFile({'id': fileid})
    content = file2.GetContentString(mimetype=mimetype)
    camList = content.split('\n')
    del camList[-1]
    return camList

def getCamList():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credFile)
    drive = GoogleDrive(gauth)
    file2 = drive.CreateFile({'id': camlistfile})
    content = file2.GetContentString(mimetype='text/csv')
    camList = content.split('\n')
    del camList[-1]
    return camList

class CameraLocation:
    lat = 0.0
    long = 0.0
    cameraId = 0
    camFile = ""
    def __init__(self, lat, long,cameraId,camfile):
        self.lat = lat
        self.long = long
        self.cameraId = cameraId
        self.camfile = camfile
    def getLocTouple():
        return (lat,long)

class TrafficData:
    incomingCount = 0
    outgoingCount = 0
    timeStamp = '2001-01-01 23:59:59'
    def __init__(self, inCount, outCount, timeStamp):
        incomingCount = inCount
        outgoingCount = outCount
        timeStamp = timeStamp

class HeatMapPoint:
    location = CameraLocation(0,0,0,'')
    carCount = 0
    def __init__(self, loc, carCount):
        self.location = loc
        self.carCount = carCount
    def getLocTouple():
        return location.getLocTouple()


def getHeatMapPoint(item):
    itemList = item.split(',')
    loc = CameraLocation(float(itemList[0]),float(itemList[1]),float(itemList[2]),itemList[3])
    point = HeatMapPoint(loc,50)
    return point

def getLatLong(point):
    return (point.location.lat,point.location.long)
def getWeights(point):
    return point.carCount

def filterTrafficDataByDate(trafficData,date):
    print(trafficData)

csv_file_content = get_csv_content_from_drive()
print(csv_file_content)
gmaps.configure(api_key=gmapsApiKey) # Fill in with your API key
camList = getCamList()
print(camList)
heatmapPoint = map(getHeatMapPoint, camList)
loc = map(getLatLong, list(heatmapPoint))
heatmapPoint = map(getHeatMapPoint, camList)
carCount = map(getWeights, list(heatmapPoint))
carCount = np.asarray(list(carCount))
weights = pd.Series(carCount)

fig = gmaps.figure(center=mapCenter, zoom_level=10)
heatmap_layer = gmaps.heatmap_layer(list(loc), weights=weights, point_radius=10)
heatmap_layer.max_intensity = 50
fig.add_layer(heatmap_layer)
embed_minimal_html('export.html', views=[fig])
#fig

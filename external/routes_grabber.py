from pymongo import MongoClient
import requests, json
#Step 1: Create data
def filter_routes(r):
    route_filtered = []
    for i in range(0, len(r)):
        route_fil = dict([])
        route_fil['RouteKey'] = r[i]['Key']
        route_fil['RouteName'] = r[i]['Name']
        route_fil['RouteShortName'] = r[i]['ShortName']
        route_fil['RouteDescription'] = r[i]['Description']
        for j in r[i]['PatternList']:
            route_fil['PatternListKey'] = j['Key']
            route_fil['DirectionKey'] = j['Direction']['DirectionKey']
            route_fil['DirectionName'] = j['Direction']['DirectionName']
        route_filtered.append(route_fil.copy()) 
    #print(route_filtered)
    return route_filtered

def filter_vehicles(veh):
    vehicle_filtered = []
    for i in range(0, len(veh)):
        vehicle_fil = dict([])
        vehicle_fil['RouteKey'] = veh[i]['RouteKey']
        vehicle_fil['DirectionKey'] = veh[i]['DirectionKey']
        for j in veh[i]['VehiclesByPattern']:
            for k in j['Vehicles']:
                vehicle_fil['PatternKey'] = j['PatternKey']
                vehicle_fil['PatternName'] = j['Pattern']['Name']
                vehicle_fil['DirectionName'] = j['Pattern']['Direction']['DirectionName']
                vehicle_fil['VehicleKey'] = k['Key']
                vehicle_fil['VehicleName'] = k['Name']
                vehicle_fil['PercentFilled'] = k['PercentFilled']
                vehicle_fil['GpsDate'] = k['GPS']['Date']
                vehicle_fil['GpsLat'] = k['GPS']['Lat']
                vehicle_fil['GpsLong'] = k['GPS']['Long']
                vehicle_fil['GpsSpd'] = k['GPS']['Spd']
                vehicle_fil['GpsDir'] = k['GPS']['Dir']
                vehicle_fil['RouteKey'] = k['Route']['Key']
                vehicle_fil['RouteName'] = k['Route']['Name']
                vehicle_fil['RouteShortName'] = k['Route']['ShortName']
                vehicle_fil['NextStopKey'] = k['NextStop']['Key']
                vehicle_fil['NextStopName'] = k['NextStop']['Name']
                vehicle_fil['NextStopArrivalAtStop'] = k['NextStop']['ArrivalAtStop']
                vehicle_fil['NextStopTimeToStop'] = k['NextStop']['TimeToStop']
                vehicle_fil['NextStopIsTimePoint'] = k['NextStop']['IsTimePoint']
                vehicle_fil['NextStopStopCode'] = k['NextStop']['StopCode']
                vehicle_fil['NextStopEstimatedDepartTime'] = k['NextStop']['EstimatedDepartTime']
                vehicle_fil['NextStopScheduledWorkDate'] = k['NextStop']['ScheduledWorkDate']
                vehicle_fil['RequestedStop'] = k['RequestedStop']
                vehicle_fil['IsLastVehicle'] = k['IsLastVehicle']
                vehicle_fil['PassengerCapacity'] = k['PassengerCapacity']
                vehicle_fil['PassengersOnboard'] = k['PassengersOnboard']
                vehicle_fil['Work'] = k['Work']
        vehicle_filtered.append(vehicle_fil.copy()) 
    #print(vehicle_filtered)
    return vehicle_filtered
        
def get_all_routes():
    #GetRoutes
    route_r = requests.post('http://www.myridebarrie.ca/RouteMap/GetRoutes/')
    route_data = route_r.json()
    return filter_routes(route_data)

get_all_routes();
 
def get_all_vehicles():
    #GetRoutes
    route_r = requests.post('http://www.myridebarrie.ca/RouteMap/GetRoutes/')
    route_data = route_r.json()
    #GetVehicles
    vehicle_array = []
    for i in range(0, len(route_data)):
        #direction_key = ('routeDirectionKeys[%d][DirectionKey]' %i)
        direction_value = route_data[i]['PatternList'][0]['Direction']['DirectionKey']
        #route_key = ('routeDirectionKeys[%d][RouteKey]' %i)
        route_value = route_data[i]['Key']
        vehicle_params = "routeDirectionKeys[0][RouteKey]={0}&routeDirectionKeys[0][DirectionKey]={1}".format(route_value,direction_value)
        headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }
        vehicle_r = requests.post('http://www.myridebarrie.ca/RouteMap/GetVehicles/', data = vehicle_params, headers = headers)
        vehicle_data = vehicle_r.json()
        vehicle_draft = json.dumps(vehicle_data)
        vehicle = json.loads(vehicle_draft)
        vehicle_array = vehicle_array + vehicle
        #print(vehicle_array)
    return filter_vehicles(vehicle_array)

get_all_vehicles();

#Step 2: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db = client.barrieTransit
   
#Step 3: Insert data into the mongoDB into a collection called routes
routes = db.routes.insert_many(get_all_routes())
vehicles = db.vehicles.insert_many(get_all_vehicles())    

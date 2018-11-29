import requests, json

mapping = {
    'Key':'PatternKey',
    'Name':'PatternName',
}

pattern_mapping = {
    'Key': 'PatternPointListKey',
    'Longitude': 'PatternLong',
    'Latitude': 'PatternLat',
    'PointTypeCode': 'PointTypeCode',
    'Stop.Key': 'StopKey',
    'Stop.Name': 'StopName',
    'Stop.ArrivalAtStop': 'StopArrivalAtStop',
    'Stop.StopCode': 'StopCode',
    'IsLastPoint': 'StopIsLastPoint'
}

def get_pat_data(dct, layers):
    if isinstance(layers, str):
        return dct[layers]
    if dct is None:
        return None
    if layers:
        k = layers.pop(0)
        return get_pat_data(dct[k], layers)
    return dct
        
def filter_patterns(r):
    pat_filtered = []
    for dct_item in r:
        pat_fil = {}
        for patt_key, final_key in mapping.items():
            pat_fil[final_key] = get_pat_data(
                dct_item,
                patt_key.split('.') if '.' in patt_key else patt_key
            )

        pattern_point_list = []
        for pattern_item in dct_item['PatternPointList']:
            pat_fil_item = {}
            for patt_key, final_pattern_key in pattern_mapping.items():
                pat_fil_item[final_pattern_key] = get_pat_data(
                    pattern_item,
                    patt_key.split('.') if '.' in patt_key else patt_key
                )
            pattern_point_list.append(pat_fil_item)
        pat_fil['PatternPointList'] = pattern_point_list
        pat_filtered.append(pat_fil)

###############################

def get_all_patterns():
#GetRoutes
    route_r = requests.post('http://www.myridebarrie.ca/RouteMap/GetRoutes/')
    route_data = route_r.json()
#GetPatterns
    pattern_array = []
    for i in range(0, len(route_data)):
        route_value = route_data[i]['Key']
        pattern_params = "routeKey={0}".format(route_value)
        headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }
        pattern_r = requests.post('http://www.myridebarrie.ca/RouteMap/GetPatternPoints/', data = pattern_params, headers = headers)
        pattern_data = pattern_r.json()
        pattern_draft = json.dumps(pattern_data)
        pattern = json.loads(pattern_draft)
        pattern_array = pattern_array + pattern
        filter_patterns(pattern_array)

if __name__ == "__main__":
    db = get_db()
    db.patterns.insert_many(get_all_patterns())    


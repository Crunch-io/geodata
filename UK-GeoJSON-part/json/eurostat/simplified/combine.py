import json


def combine():

    files = ['england.geojson', 'scotland.geojson', 'northern_ireland.geojson']


    all = None
    for f in files:
        jsn = json.load(file(f))
        if all is None:
            all = jsn
        else:
            all['features'].extend(jsn['features'])


    for x in all['features']:
        x['properties']['name'] = x['properties'].get('NUTS112NM', x['properties'].get('NUTS2_NAME', x['properties'].get('name')))
        if 'NUTS112NM' in x['properties']:
            del x['properties']['NUTS112NM']
        if 'NUTS2_NAME' in x['properties']:
            del x['properties']['NUTS2_NAME']
        print x['properties']['name']

    json.dump(all, file('combined.geojson', 'w'))



def create_geojson_from_waypoints(locale):


    waypoints = file(locale + '_waypoints.txt').read().split('\n')

    polys = []
    poly = []

    for i, point in enumerate(waypoints):
        if point in ['', '\r']:
            polys.append(poly)
            poly = []
            continue
        if point[0] == '#':
            continue
        point = point.split(' ')
        poly.append([float(point[1]), float(point[0][:-1])])


    feature = {"type": "Feature", "properties": {"name": "Northern Ireland"}, "geometry": {"type": "MultiPolygon", "coordinates": [polys]}}

    geo = {"crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
     "type": "FeatureCollection", "features": [feature]}

    json.dump(geo, file(locale + '.geojson', 'w'))


if __name__ == '__main__':
    create_geojson_from_waypoints('northern_ireland')
    #create_geojson_from_waypoints('scotland')
    combine()

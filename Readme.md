# ValhallaPY

This is a quick python wrapper for the [Valhalla]() service from MapZen

## Instalation

pip install valhallapy

## Running

```python
from valhalla import Valhalla

valhalla = Valhalla(host="http://192.168.99.100:5333")

start = {'lat': '', 'lon':''}
end   = {'lat':'', 'lon':''}
route  = valhalla.route(start, end, costing='pedestrian')
print 'that route as %d km long and took %d s ' %(route.distance(), route.time())
print 'GEOJSON %s' % ((route.geoJSON())
```

## Connection

To connect to a server initialize a valhalla object

```python
from valhalla import Valhalla

valhalla = Valhalla(host="http://192.168.99.100:5333", api_key="")
```

where the api key is optional (get your api keys [here](https://mapzen.com/developers/sign_in) if you are running locally. Once you have a connection, request a route by

## Get a route

Request a route using the following

```python
  route = valhalla.route(start, end, costing)
```

where costing can be 'pedestrian', 'auto' etc ([full list of costing models](https://mapzen.com/documentation/turn-by-turn/api-reference/#costing-models)).

This returns a ValhallaRoute object which can be interegated for information about the returned route

```python
route.time() # The time in seconds the route will take
route.distance() # The distance in km the route was
route.instructions() # A set of turn by turn instructions for the route
route.geoJSON(parameters=[]) # Return the route as geojson appending extra parameters in the optional parameters argument
```




## To Do

* [ ] refactor
* [ ] create a method to do batches of routes
* [ ] change the route method to allow for multiple waypoints

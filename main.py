#!/usr/bin/env python3

import requests
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.types import Type, Field, list_of
from typing import List
from pprint import pprint


Coordinates = List[int]


def address_search(address: str) -> Coordinates:
    url = f'https://api.digitransit.fi/geocoding/v1/search?text={address}&size=1'
    response = requests.get(url)
    content = response.json()
    return content['features'][0]['geometry']['coordinates']


class Plan(Type):
    pass

class Location(Type):
    lat: float
    lon: float

class Query(Type):
    plan = Field(Plan, args={'from': Location, 'to': Location, 'num_itineraries': int})


def route(from_coords: Coordinatos, to_coords: Coordinates) -> dict:
    url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
    headers = {}
    query = f'''\
        {
          plan(
            from: {lat: 60.168992, lon: 24.932366}
            to: {lat: 60.175294, lon: 24.684855}
            numItineraries: 3
          ) {
            itineraries {
              legs {
                startTime
                endTime
                mode
                duration
                realTime
                distance
                transitLeg
              }
            }
          }
        }
    '''
    variables = {'varName': 'value'}
    endpoint = HTTPEndpoint(url, headers)
    data = endpoint(query, variables)
    return data


if __name__ == '__main__':
    pprint(route())
    #coordinates = address_search('Alaportti 1 A')
    #pprint(coordinates)

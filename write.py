"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
from os import name
from helpers import datetime_to_str
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    # TODO: Write the results to a CSV file, following the specification in the instructions.
    with open(filename,'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = fieldnames)
        writer.writeheader()
        for element in results:
            if element.neo.name == None:
                element.neo.name = ''
            if element.neo.hazardous == True:
                element.neo.hazardous = 'True'
            else:
                element.neo.hazardous = 'False'

            writer.writerow(
                {
                    fieldnames[0]: element.time_str,
                    fieldnames[1]: element.distance,
                    fieldnames[2]: element.velocity,
                    fieldnames[3]: element._designation,
                    fieldnames[4]: element.neo.name,
                    fieldnames[5]: element.neo.diameter,
                    fieldnames[6]: element.neo.hazardous
                }
            )



def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.
    json_data = list()
    for element in results:
        if element.neo.name == None:
            element.neo.name = ''
        json_data.append(
            {
            'datetime_utc' : datetime_to_str(element.time),
            'distance_au'  : element.distance,
            'velocity_km_s': element.velocity,
            'neo':{
                'designation': element.neo.designation,
                'name'       : element.neo.name,
                'diameter_km': element.neo.diameter,
                'potentially_hazardous': element.neo.hazardous
            }
        }
        )
    
    with open(filename,'w') as outfile:
        outfile.write(json.dumps(json_data, indent = '\t'))

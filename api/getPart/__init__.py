import logging

import azure.functions as func
from AltiumDatabase import AltiumDatabase
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("GetPart: {}".format(req.params.get('PartNumber')))
    database = AltiumDatabase(downloadAll=False)
    part = database.SearchPart(req.params.get('PartNumber'))
    if part == None:
        return func.HttpResponse(
        json.dumps(),
        mimetype="application/json",
    ) 
    return func.HttpResponse(
        json.dumps(part.dictionary),
        mimetype="application/json",
    ) 

import logging

import azure.functions as func
from AltiumDatabase import AltiumDatabase
import json

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("GetPartList: {}")
    database = AltiumDatabase(downloadAll=False)
    PartNames = database.GetPartNumbers()
    # return jsonify(PartNames)
    return func.HttpResponse(
        json.dumps(PartNames),
        mimetype="application/json",
    ) 

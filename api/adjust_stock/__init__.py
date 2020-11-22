import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    formPartNumber = req.params.get('PartNumber')
    Stock = req.params.get('Stock')
    Box = req.params.get('Box')
    if formPartNumber != None or formPartNumber!= '':
        logging.info("PN: {} Box: {} Stock: {}".format(formPartNumber, Box, Stock))
        print(formPartNumber)
        print(Box)
        print(Stock)
        database = AltiumDatabase(downloadAll=False)
        database.AdjustStock(formPartNumber,Box,Stock)
        return func.HttpResponse(
        json.dumps({'Part Number':formPartNumber}),
        mimetype="application/json",
    ) 
    else:   
        return func.HttpResponse(
        json.dumps(),
        mimetype="application/json",
    ) 
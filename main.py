from fastapi import FastAPI,Response,status
import order_model
import utilsPostgres
import json
from fastapi.encoders import jsonable_encoder
from datetime import datetime

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/Order")
async def Order(order: order_model.Orders):
    print('call order: ')
    print(order.accessionNumber)

    try:
        utilsPostgres.insert_order(order)
        return {"body": "123",
                "header":
                    {
                        "message": "Order created successfully",
                        "code": status.HTTP_200_OK,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }

    except Exception as exc:
        return {"body": "123",
                "header":
                    {
                        "message": "insert_order error: " + str(exc),
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }


@app.get("/GetOrder")
async def get_order(order: order_model.Orders):
    print('call GetOrder: ')
    print(order.accessionNumber)
    try:
        data = utilsPostgres.get_order_by_accessionNumber(order.accessionNumber)
        #json_compatible_item_data = jsonable_encoder(data.service)
        #service = json.dumps(data.service,indent=4)
        xml = order_model.get_order_XML(data)
        if xml is None:
            return {"body": {},
                    "header":
                        {
                            "message": "GetOrder successfully",
                            "code": status.HTTP_200_OK,
                            "datetime": datetime.today().strftime("%Y%m%d%H%M")

                        }
                    }

        return {"body": xml,
                "header":
                    {
                        "message": "GetOrder successfully",
                        "code": status.HTTP_200_OK,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }

    except Exception as exc:
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(exc) + " A problem when get AccessionNumber: " + order.accessionNumber,
        )
@app.post("/InsertResult")
async def InsertResult(result: order_model.Result):
    print('call InsertResult: ')
    print(result.accessionNumber)
    try:
        result = utilsPostgres.insert_result(result)
        if result is None:
            return {"body": {},
                "header":
                    {
                        "message": "InsertResult is not found",
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }
        return {"body":"123",
                "header":
                    {
                        "message": "InsertResult is successfully",
                        "code": 200,
                        "datetime":datetime.today().strftime("%Y%m%d%H%M")

                    }
                }
    except Exception as exc:
        return {"body": "123",
                "header":
                    {
                        "message": "InsertResult error: " + str(exc),
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }




@app.get("/GetResult")
async def GetResult(result: order_model.Result):
    print('call get GetResult: ')
    print(result.accessionNumber)
    try:
        data = utilsPostgres.get_result(result.accessionNumber)
        if(data is None):
            return {"body": {},
                    "header":
                        {
                            "message": "GetResult successfully",
                            "code": 200,
                            "datetime": datetime.today().strftime("%Y%m%d%H%M")

                        }
                    }
        return {"body": order_model.get_result_XML(data),
                "header":
                    {
                        "message": "GetResult successfully",
                        "code": 200,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }
    except Exception as exc:
        return {"body": "123",
                "header":
                    {
                        "message": "GetResult error: " + str(exc),
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "datetime": datetime.today().strftime("%Y%m%d%H%M")

                    }
                }


@app.get("/GetViewImage")
async def GetViewImage(name: str):
    return {"message": f"Hello {name}"}
@app.post("/Delete")
async def Delete(name: str):
    return {"message": f"Hello {name}"}

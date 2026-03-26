from hit_endpoints import hit_endpoints
from hit_endpoints import load_endpts

def handler(event, context):

    endpts = load_endpts()
    res = hit_endpoints(endpts)

    if res:
        return {"statusCode": 200, "body": "End points check successful!"}
    else:
        return {"statusCode": 200, "body": "End points check failed!"}

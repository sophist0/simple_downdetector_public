from downdetector_app.lambda_code.hit_endpoints import hit_endpoints

def test_hit_endpoint_success():
    succeed = {"succeed": "https://www.google.com"}
    assert hit_endpoints(succeed)

def test_hit_endpoint_fail():
    fail = {"fail": "https://www.gooogle.com"}
    assert not hit_endpoints(fail)
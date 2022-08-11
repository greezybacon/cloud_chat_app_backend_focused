from behave import given, then, when

class RestApiClient:
    def __init__(self, client):
        self.client = client

    def make_request(self, url_path, verb='get', *, ignore_bad_status=False,
        **data):
        # method would be the method of the client which implements the
        # requested HTTP verb.
        method = getattr(self.client, verb)
        response = method(url_path, data=data)
        if not ignore_bad_status:
            print("server said,", response.text)
            assert response.status_code != 500
            assert response.status_code != 404

        return response

@given('a connection to the REST API')
def step_impl(context):
    assert context.api_client
    context.api = RestApiClient(context.api_client)

@then('api response was {result}')
def step_impl(context, result):
    if result == 'successful':
        assert context.last_api_response.status_code == 200

    else:
        assert context.last_api_response.status_code != 200

@when('sending request to /{path}')
def step_impl(context, path):
    context.last_api_response = context.api.make_request(path)

@then('the api response body was "{body}"')
def step_impl(context, body):
    assert context.last_api_response.text.strip() == body

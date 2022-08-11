from behave import given, when

@given('an account with username="{username}"')
@when('creating a new account with username="{username}"')
def step_impl(context, username):
    assert context.api
    response = context.api.make_request(f'/user/{username}/create', 'post')
    context.last_api_response = response

@when('logging in with username="{username}"')
def authenticate_as(context, username):
    assert context.api
    response = context.api.make_request(f'/user/{username}/signin', 'post',
        ignore_bad_status=True)
    context.last_api_response = response

@given('a session with username="{username}"')
def step_impl(context, username):
    authenticate_as(context, username)
    assert context.last_api_response.status_code == 200
from behave import then, when

@when('creating a chat room with name="{roomname}"')
def step_impl(context, roomname):
    assert context.api
    response = context.api.make_request(f'/room/{roomname}/create', 'post')
    context.last_api_response = response

@when('joining a chat room with name="{roomname}"')
def step_impl(context, roomname):
    assert context.api
    response = context.api.make_request(f'/room/{roomname}/subscribe', 'post')
    context.last_api_response = response

@when('posting a message to chat room with name="{roomname}"')
def step_impl(context, roomname):
    assert context.api
    response = context.api.make_request(f'/room/{roomname}/publish', 'post',
        content=context.text)
    context.last_api_response = response

@then('the chat room with name="{roomname}" has {count} message')
@then('the chat room with name="{roomname}" has {count} messages')
def step_impl(context, roomname, count):
    assert context.api
    response = context.api.make_request(f'/room/{roomname}/activity')
    context.last_api_response = response

    assert len(response.get_json()) == int(count)
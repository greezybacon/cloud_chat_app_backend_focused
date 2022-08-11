Feature: Api sports a PING endpoint
    Background:
        Given a connection to the REST API

        Scenario:
            When sending request to /ping
            Then api response was successful
             And the api response body was "pong"

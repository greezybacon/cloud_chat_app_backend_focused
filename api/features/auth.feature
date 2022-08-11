Feature: Authentication is done using username only. Passwords are not necessary.
    Background:
        Given a connection to the REST API
          And an account with username="mr.robot"

        Scenario: User can log in with already-created account
            When logging in with username="mr.robot"
            Then api response was successful

        Scenario: User cannot log in without an account
            When logging in with username="nobody"
            Then api response was unsuccessful

        Scenario: Little Bobby Tables can log in too
            When creating a new account with username="Robert'); DROP TABLE chat.user;--"
            Then api response was successful
            When logging in with username="Robert'); DROP TABLE chat.user;--"
            Then api response was successful

        Scenario: Mr.Robot could still log in after Bobby Tables...
            When logging in with username="mr.robot"
            Then api response was successful

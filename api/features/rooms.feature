Feature: Users can create and join chat rooms

    Background:
        Given a connection to the REST API
          And an account with username="mr.robot"
          And a session with username="mr.robot"

    Scenario: Users can create a chat room
        When creating a chat room with name="personal"
        Then api response was successful

    Scenario: Users canNOT create a chat room with duplicate name
        When creating a chat room with name="personal"
        Then api response was successful
        When creating a chat room with name="personal"
        Then api response was unsuccessful

    Scenario: Users cannot join a non-existant room
        When joining a chat room with name="know-where"
        Then api response was unsuccessful
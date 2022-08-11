Feature: Users must have a unique username. No other attributes describing the
         user are necessary.

    Background:
        Given a connection to the REST API

        Scenario: User can create a new, unique user account
            When creating a new account with username="mr.robot"
            Then api response was successful

        Scenario: User cannot create a non-unique user account
            When creating a new account with username="mr.robot"
            Then api response was successful
            When creating a new account with username="mr.robot"
            Then api response was unsuccessful
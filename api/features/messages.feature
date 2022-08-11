Feature: Users can post messages to chat rooms

    Background:
        Given a connection to the REST API
          And an account with username="mr.robot"
          And a session with username="mr.robot"
         When creating a chat room with name="personal"
           
        Scenario: The chatroom initially has no history
            When joining a chat room with name="personal"
            Then the chat room with name="personal" has 0 messages

        Scenario: User can join a room and post a messages
            When joining a chat room with name="personal"
             And posting a message to chat room with name="personal"
             """
             Hello, world!
             """
            Then api response was successful
             And the chat room with name="personal" has 1 message
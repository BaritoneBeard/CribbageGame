Feature: create read update delete

  Scenario: Search for valid connection
    Given The server is running
    Then I will be able to connect
    And I will be able to give a pathway and data
    And I will be able to update existing data
    And I will be able to delete existing data

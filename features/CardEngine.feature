Feature: CRUD cards
  Scenario: Create deck, draw from deck, delete deck
    Given The server is up
    Then I can create a deck
    And I can draw from the deck
    And I can delete the deck
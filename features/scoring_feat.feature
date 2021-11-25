Feature: I can tally up the score of a player's hand.
  Scenario: I can tally up the score of a player's hand
    Given I have a list of card ranks
    Then I can tally how many combinations total fifteen
    And I can tally how many cards of a kind exist
    And I can tally how many cards are in a run
    And I can determine a flush
    And I can determine a nob
Feature: Calculate point totals during the pegging round of cribbage
  Scenario: I can count up point totals
    Given There is a list of cards
      And The total number of points does not exceed 31
        Then I can check if a player added to the pegging
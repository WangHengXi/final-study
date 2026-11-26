## MODIFIED Requirements

### Requirement: Authenticated navigation

The default shared navbar SHALL give authenticated users a brand link to the public homepage and one keyboard-operable navigation menu. The menu SHALL contain links to the study overview, study calendar, and course list, a non-navigating "複習分析（即將推出）" item, and a safe POST logout action with a CSRF token without requiring a UserProfile.

#### Scenario: Authenticated user opens the navigation menu

- **WHEN** an authenticated user activates the navigation menu
- **THEN** the menu exposes links to the study overview, study calendar, and course list
- **AND THEN** it displays the unavailable review-analysis item without a navigation target
- **AND THEN** it contains a POST logout form with a CSRF token.

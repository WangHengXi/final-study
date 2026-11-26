## MODIFIED Requirements

### Requirement: Authenticated navigation

The default shared navbar SHALL give authenticated users access to the StudyTrack home page, their study dashboard, study calendar, course list, and a safe logout action without requiring a UserProfile.

#### Scenario: An authenticated user without a UserProfile views a learning page

- **WHEN** an authenticated Django user without a UserProfile requests a course list page they are authorized to access
- **THEN** the response renders successfully
- **AND THEN** the navbar contains links to the home page, study dashboard, study calendar, and course list
- **AND THEN** it contains a POST logout form with a CSRF token.

##### Example: User without a profile can navigate

- **GIVEN** an authenticated user named `no-profile-user` has no UserProfile and requests `/learning/courses/`
- **WHEN** Django renders the response
- **THEN** the response status is 200
- **AND THEN** the navbar contains links to `/`, the study dashboard, `/learning/calendar/`, and `/learning/courses/`
- **AND THEN** it contains a POST form targeting `/accounts/logout/` with `csrfmiddlewaretoken`.

## Purpose

The study dashboard is the authenticated starting point for daily preparation. It presents a learner's work for the current date and routes them to calendar planning and course management.

## ADDED Requirements

### Requirement: Authenticated users reach a personal study dashboard

The system SHALL use the study dashboard as the default destination after successful sign-in. An authenticated request to the home route SHALL render the dashboard, while an unauthenticated request to the same route SHALL render the public homepage.

#### Scenario: User signs in and reaches the dashboard

- **WHEN** a user successfully signs in without a requested return URL
- **THEN** the response redirects to the study dashboard
- **AND THEN** a subsequent home-route request renders the dashboard for that user.

#### Scenario: Visitor sees the public homepage

- **WHEN** an unauthenticated visitor requests the home route
- **THEN** the response renders the public homepage
- **AND THEN** it does not render personal study tasks.

### Requirement: Dashboard summarizes only today's personal tasks

The study dashboard SHALL display the current date's StudyTask records for the authenticated user, separated by incomplete and completed state. It SHALL include an explicit empty state when the user has no task for the current date and SHALL provide links to create a task, view the calendar, and view the user's courses.

#### Scenario: Dashboard excludes another user's task

- **GIVEN** two users each own a StudyTask scheduled for the current date
- **WHEN** one user opens the study dashboard
- **THEN** the dashboard displays only that user's task
- **AND THEN** it distinguishes whether that task is complete.

#### Scenario: Dashboard handles no tasks today

- **GIVEN** an authenticated user owns no StudyTask scheduled for the current date
- **WHEN** the user opens the study dashboard
- **THEN** the dashboard displays a no-tasks-today message
- **AND THEN** it provides a link to create a task for the current date.

## Purpose

The study overview provides an authenticated personal entry point without replacing the public product homepage. It summarizes current study work and gives users a stable hub for their planning tools.

## ADDED Requirements

### Requirement: Authenticated study overview route

The system SHALL provide an authenticated study overview at `/overview/`. Successful login without a requested return URL SHALL redirect to this route. The overview SHALL show only the requesting user's current-day StudyTask records and SHALL provide an explicit empty state when none exist.

#### Scenario: Signed-in user opens the overview

- **GIVEN** an authenticated user owns a StudyTask scheduled for the current date
- **WHEN** the user requests `/overview/`
- **THEN** the response displays that task
- **AND THEN** it excludes tasks owned by other users.

#### Scenario: User has no tasks today

- **GIVEN** an authenticated user owns no StudyTask scheduled for the current date
- **WHEN** the user requests `/overview/`
- **THEN** the response displays a no-tasks-today state.

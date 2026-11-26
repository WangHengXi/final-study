## Purpose

The study calendar gives each authenticated learner a private month view for planning daily study work. It connects a dated task to an optional existing course without exposing one user's plans to another user.

## ADDED Requirements

### Requirement: Private monthly study calendar

The system SHALL provide an authenticated calendar page at `/learning/calendar/`. It SHALL render the requested `month` query value in `YYYY-MM` format, or the current month when the value is absent or invalid. The calendar SHALL show only StudyTask records owned by the requesting user in that displayed month, grouped by scheduled date, and SHALL provide controls for the previous month, next month, and creating a task for a date.

#### Scenario: User views a month containing personal tasks

- **GIVEN** an authenticated user owns a task scheduled for 2026-12-08 and another user owns a task scheduled for 2026-12-08
- **WHEN** the authenticated user requests `/learning/calendar/?month=2026-12`
- **THEN** the December calendar includes the authenticated user's task and excludes the other user's task
- **AND THEN** the calendar provides links targeting November 2026 and January 2027.

#### Scenario: Invalid month preserves calendar access

- **WHEN** an authenticated user requests the calendar with `month=not-a-month`
- **THEN** the response is successful
- **AND THEN** it renders the current month rather than returning a server error.

### Requirement: Create and edit a dated study task

The system SHALL let an authenticated user create and edit a StudyTask containing a required title of no more than 120 characters, a required scheduled date, an optional note, and an optional course selected only from that user's courses. A successful submission SHALL redirect to a page that displays the task's scheduled month. Invalid input SHALL preserve submitted values, show field errors, and SHALL NOT persist a task or an update.

#### Scenario: User creates a task linked to an owned course

- **GIVEN** an authenticated user owns a course named "專業課"
- **WHEN** the user submits a task titled "閱讀第二章" for 2026-12-08 and selects "專業課"
- **THEN** a StudyTask owned by that user is created with that date and course
- **AND THEN** the redirect shows the December 2026 calendar.

#### Scenario: User cannot attach another user's course

- **GIVEN** an authenticated user submits a valid title and date with a course identifier owned by another user
- **WHEN** the system validates the submission
- **THEN** the response shows a course validation error
- **AND THEN** no StudyTask is created or reassigned.

### Requirement: Manage completion and removal of personal tasks

The system SHALL let an authenticated task owner toggle completion and delete a StudyTask through CSRF-protected POST requests. A request targeting a StudyTask not owned by the current user SHALL return 404 and SHALL NOT change or disclose the task.

#### Scenario: Task owner completes a task

- **GIVEN** an authenticated user owns an incomplete task scheduled for 2026-12-08
- **WHEN** the user submits the task completion action
- **THEN** the task is marked completed
- **AND THEN** the response redirects to the task's displayed month.

#### Scenario: Other user cannot change a task

- **GIVEN** one authenticated user owns a StudyTask
- **WHEN** a different authenticated user submits an edit, completion, or deletion request using that task's identifier
- **THEN** the response status is 404
- **AND THEN** the owned task remains unchanged.

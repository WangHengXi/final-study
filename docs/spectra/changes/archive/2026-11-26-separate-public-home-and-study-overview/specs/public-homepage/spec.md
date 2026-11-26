## MODIFIED Requirements

### Requirement: Accurate public learning workflow

The system SHALL present the root route as a public Morandi-purple and warm-white introduction to organizing independent study for every visitor, including authenticated users. It SHALL describe only the available course, chapter, question, error-reason, tag, learning-setting, and personal study-planning workflows. Illustrative labels SHALL use neutral preparation-oriented content rather than school-level example subjects. The homepage SHALL NOT render a user's personal StudyTask records and SHALL NOT represent answer status, redo history, accuracy percentages, trend charts, progress analytics, reminders, recurring schedules, or external calendar synchronization as available product functionality.

#### Scenario: Any user sees the public product introduction

- **WHEN** an unauthenticated visitor or authenticated user requests the root route
- **THEN** the response renders the public product introduction
- **AND THEN** it does not render personal tasks or a personal dashboard.

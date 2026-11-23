## Purpose

The public homepage introduces StudyTrack with an accurate description of its current learning-management workflow. It guides visitors and signed-in users to the appropriate first action without promising unavailable analytics features.

## ADDED Requirements

### Requirement: Accurate public learning workflow

The system SHALL present the public homepage as a warm stationery-style introduction to creating courses, organizing chapters, recording questions and error reasons, applying tags, and setting a review interval. The homepage SHALL NOT represent answer status, redo history, accuracy percentages, trend charts, or progress analytics as available product functionality.

#### Scenario: Visitor reviews supported features

- **WHEN** a visitor views the public homepage
- **THEN** the feature introduction describes only course, chapter, question, error-reason, tag, and learning-setting workflows
- **AND THEN** no feature card or illustrative data claims that redo outcomes, accuracy trends, or progress analytics are available

### Requirement: Auth-aware first-course action

The system SHALL expose a primary action labeled to start the user's first course. The action SHALL direct an unauthenticated visitor to the existing login route and SHALL direct an authenticated user to the existing course-list route.

#### Scenario: Unauthenticated visitor starts a course

- **WHEN** an unauthenticated visitor activates the primary action on the public homepage
- **THEN** the browser navigates to the existing login route

#### Scenario: Authenticated user starts a course

- **WHEN** an authenticated user activates the primary action on the public homepage
- **THEN** the browser navigates to the existing course-list route

### Requirement: Accessible responsive homepage

The system SHALL keep the primary action and the learning-workflow content available at narrow viewport widths and without JavaScript. Interactive controls SHALL expose a visible keyboard focus indicator. When the user prefers reduced motion, decorative motion and smooth-scroll behavior SHALL be disabled.

#### Scenario: Keyboard user reaches the primary action

- **WHEN** a keyboard user tabs through the public homepage
- **THEN** the primary action receives a visible focus indicator and can be activated

#### Scenario: User disables non-essential motion

- **WHEN** a user has enabled the reduced-motion preference
- **THEN** the homepage does not require animation or smooth scrolling to read the workflow or use the primary action

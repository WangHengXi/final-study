## Purpose

The Morandi purple-and-white visual system provides a single, restrained color language for StudyTrack's public and authenticated study surfaces. It removes decorative pink and green styling so the product presents a consistent, mature study-planning experience.

## ADDED Requirements

### Requirement: A shared Morandi purple-and-white palette

The system SHALL provide one shared visual palette for public and authenticated user-facing pages: page background `#FAF9FC`, card surface `#FFFFFF`, subtle surface `#EEEAF2`, primary gray-purple `#766782`, primary text `#403849`, muted text `#6F6678`, and border `#DDD5E4`. Decorative page surfaces, primary actions, labels, calendar items, course cards, and navigation controls SHALL use only these palette roles and their transparency or white variants.

#### Scenario: A visitor and a signed-in user view supported surfaces

- **WHEN** a visitor opens the public homepage and a signed-in user opens the Overview, calendar, course list, course detail, or course form
- **THEN** each page renders the shared purple-and-white palette for its decorative surfaces, controls, text hierarchy, and borders
- **AND** no page requires a page-local pink, green, or rose palette to render its primary interface.

### Requirement: Decorative multicolor course styling is absent

The system SHALL NOT render pink, green, or rose decorative backgrounds, course dots, badges, buttons, or cards on the supported study surfaces. Course identity and task grouping SHALL be communicated with text, placement, white and subtle-purple surfaces, borders, and gray-purple interaction states instead of per-course color hues.

#### Scenario: A user reads course and calendar content

- **WHEN** a signed-in user views a course list, course detail, course-related form, calendar day, or study task form
- **THEN** the visible decorative elements use white, subtle purple, gray-purple, and neutral text roles
- **AND** course and task elements do not introduce a distinct pink or green accent.

### Requirement: Interactive and validation feedback remain distinguishable

The system SHALL preserve visible keyboard focus, hover feedback, disabled-state readability, and form validation feedback while applying the single decorative palette. Validation errors MUST remain textual and readable, and MUST NOT depend on a pink, green, or rose decorative surface.

#### Scenario: A keyboard user and a form user receive feedback

- **WHEN** a user focuses a link, button, select, input, or textarea, or submits a form with an invalid required value
- **THEN** the focused control has a visible gray-purple focus treatment
- **AND** the invalid form presents readable validation feedback without adding a decorative multicolor card or surface.

### Requirement: Deprecated decorative palette sources do not return

The shared theme and affected page styles SHALL define palette roles directly rather than depend on override selectors for obsolete pink, green, or rose source values. The affected home, navigation, calendar, and course templates and stylesheets SHALL NOT contain the retired decorative color values `#EAD1D7`, `#DFBEC7`, `#DFBCC6`, `#F0F3F0`, `#F0E7EB`, or `#E7ECE9`.

#### Scenario: Theme sources are inspected after a visual update

- **WHEN** the shared theme and affected page templates and stylesheets are checked
- **THEN** the retired decorative color values are absent
- **AND** the shared palette values remain available to the supported surfaces.

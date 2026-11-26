# morandi-purple-white-visual-system Specification

## Purpose

The Morandi purple-and-white visual system provides a single, restrained color language for StudyTrack's public and authenticated study surfaces. It removes decorative pink and green styling so the product presents a consistent, mature study-planning experience.

## Requirements

### Requirement: A shared Morandi purple-and-white palette

The system SHALL provide one shared visual palette for public and authenticated user-facing pages: page background `#FAF9FC`, card surface `#FFFFFF`, subtle surface `#EEEAF2`, primary gray-purple `#766782`, primary text `#403849`, muted text `#6F6678`, and border `#DDD5E4`. Decorative page surfaces, primary actions, labels, calendar items, course cards, and navigation controls SHALL use only these palette roles and their transparency or white variants.

#### Scenario: A visitor and a signed-in user view supported surfaces

- **WHEN** a visitor opens the public homepage and a signed-in user opens the Overview, calendar, course list, course detail, or course form
- **THEN** each page renders the shared purple-and-white palette for its decorative surfaces, controls, text hierarchy, and borders
- **AND** no page requires a page-local pink, green, or rose palette to render its primary interface.


<!-- @trace
source: unify-morandi-purple-white-theme
updated: 2026-11-26
code:
  - apps/learning/templates/learning/course_form.html
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - apps/learning/templates/learning/study_calendar.html
  - apps/core/static/core/navbar.css
  - apps/learning/templates/learning/study_task_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - apps/learning/templates/learning/question_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - staticfiles/final-study/js/course-list.js.gz
  - staticfiles/facebook/js/fbconnect.js
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - apps/learning/migrations/0007_studytask.py
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/core/urls.py
  - staticfiles/final-study/css/study-calendar.css
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_detail.html
  - apps/core/templates/core/home.html
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - apps/core/tests.py
  - staticfiles/final-study/css/course-list.css
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
  - .env.example
  - staticfiles/final-study/js/course-list.js
  - apps/learning/tests.py
  - staticfiles/core/studytrack-theme.css
  - apps/learning/views.py
  - apps/learning/templates/learning/course_list.html
  - staticfiles/final-study/css/study-calendar.css.gz
  - staticfiles/facebook/js/fbconnect.js.gz
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - apps/learning/models.py
  - config/settings/base.py
  - apps/core/templates/core/dashboard.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/staticfiles.json
  - apps/core/static/core/studytrack-theme.css
  - config/settings/dev.py
  - apps/learning/forms.py
  - staticfiles/final-study/css/home.css
  - staticfiles/core/studytrack-theme.css.gz
  - static/final-study/css/home.css
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - apps/learning/urls.py
  - apps/core/templates/core/includes/navbar.html
  - apps/core/views.py
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->

---
### Requirement: Decorative multicolor course styling is absent

The system SHALL NOT render pink, green, or rose decorative backgrounds, course dots, badges, buttons, or cards on the supported study surfaces. Course identity and task grouping SHALL be communicated with text, placement, white and subtle-purple surfaces, borders, and gray-purple interaction states instead of per-course color hues.

#### Scenario: A user reads course and calendar content

- **WHEN** a signed-in user views a course list, course detail, course-related form, calendar day, or study task form
- **THEN** the visible decorative elements use white, subtle purple, gray-purple, and neutral text roles
- **AND** course and task elements do not introduce a distinct pink or green accent.


<!-- @trace
source: unify-morandi-purple-white-theme
updated: 2026-11-26
code:
  - apps/learning/templates/learning/course_form.html
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - apps/learning/templates/learning/study_calendar.html
  - apps/core/static/core/navbar.css
  - apps/learning/templates/learning/study_task_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - apps/learning/templates/learning/question_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - staticfiles/final-study/js/course-list.js.gz
  - staticfiles/facebook/js/fbconnect.js
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - apps/learning/migrations/0007_studytask.py
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/core/urls.py
  - staticfiles/final-study/css/study-calendar.css
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_detail.html
  - apps/core/templates/core/home.html
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - apps/core/tests.py
  - staticfiles/final-study/css/course-list.css
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
  - .env.example
  - staticfiles/final-study/js/course-list.js
  - apps/learning/tests.py
  - staticfiles/core/studytrack-theme.css
  - apps/learning/views.py
  - apps/learning/templates/learning/course_list.html
  - staticfiles/final-study/css/study-calendar.css.gz
  - staticfiles/facebook/js/fbconnect.js.gz
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - apps/learning/models.py
  - config/settings/base.py
  - apps/core/templates/core/dashboard.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/staticfiles.json
  - apps/core/static/core/studytrack-theme.css
  - config/settings/dev.py
  - apps/learning/forms.py
  - staticfiles/final-study/css/home.css
  - staticfiles/core/studytrack-theme.css.gz
  - static/final-study/css/home.css
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - apps/learning/urls.py
  - apps/core/templates/core/includes/navbar.html
  - apps/core/views.py
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->

---
### Requirement: Interactive and validation feedback remain distinguishable

The system SHALL preserve visible keyboard focus, hover feedback, disabled-state readability, and form validation feedback while applying the single decorative palette. Validation errors MUST remain textual and readable, and MUST NOT depend on a pink, green, or rose decorative surface.

#### Scenario: A keyboard user and a form user receive feedback

- **WHEN** a user focuses a link, button, select, input, or textarea, or submits a form with an invalid required value
- **THEN** the focused control has a visible gray-purple focus treatment
- **AND** the invalid form presents readable validation feedback without adding a decorative multicolor card or surface.


<!-- @trace
source: unify-morandi-purple-white-theme
updated: 2026-11-26
code:
  - apps/learning/templates/learning/course_form.html
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - apps/learning/templates/learning/study_calendar.html
  - apps/core/static/core/navbar.css
  - apps/learning/templates/learning/study_task_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - apps/learning/templates/learning/question_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - staticfiles/final-study/js/course-list.js.gz
  - staticfiles/facebook/js/fbconnect.js
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - apps/learning/migrations/0007_studytask.py
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/core/urls.py
  - staticfiles/final-study/css/study-calendar.css
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_detail.html
  - apps/core/templates/core/home.html
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - apps/core/tests.py
  - staticfiles/final-study/css/course-list.css
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
  - .env.example
  - staticfiles/final-study/js/course-list.js
  - apps/learning/tests.py
  - staticfiles/core/studytrack-theme.css
  - apps/learning/views.py
  - apps/learning/templates/learning/course_list.html
  - staticfiles/final-study/css/study-calendar.css.gz
  - staticfiles/facebook/js/fbconnect.js.gz
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - apps/learning/models.py
  - config/settings/base.py
  - apps/core/templates/core/dashboard.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/staticfiles.json
  - apps/core/static/core/studytrack-theme.css
  - config/settings/dev.py
  - apps/learning/forms.py
  - staticfiles/final-study/css/home.css
  - staticfiles/core/studytrack-theme.css.gz
  - static/final-study/css/home.css
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - apps/learning/urls.py
  - apps/core/templates/core/includes/navbar.html
  - apps/core/views.py
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->

---
### Requirement: Deprecated decorative palette sources do not return

The shared theme and affected page styles SHALL define palette roles directly rather than depend on override selectors for obsolete pink, green, or rose source values. The affected home, navigation, calendar, and course templates and stylesheets SHALL NOT contain the retired decorative color values `#EAD1D7`, `#DFBEC7`, `#DFBCC6`, `#F0F3F0`, `#F0E7EB`, or `#E7ECE9`.

#### Scenario: Theme sources are inspected after a visual update

- **WHEN** the shared theme and affected page templates and stylesheets are checked
- **THEN** the retired decorative color values are absent
- **AND** the shared palette values remain available to the supported surfaces.

<!-- @trace
source: unify-morandi-purple-white-theme
updated: 2026-11-26
code:
  - apps/learning/templates/learning/course_form.html
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - apps/learning/templates/learning/study_calendar.html
  - apps/core/static/core/navbar.css
  - apps/learning/templates/learning/study_task_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - apps/learning/templates/learning/question_form.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - staticfiles/final-study/js/course-list.js.gz
  - staticfiles/facebook/js/fbconnect.js
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - apps/learning/migrations/0007_studytask.py
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/core/urls.py
  - staticfiles/final-study/css/study-calendar.css
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_detail.html
  - apps/core/templates/core/home.html
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - apps/core/tests.py
  - staticfiles/final-study/css/course-list.css
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
  - .env.example
  - staticfiles/final-study/js/course-list.js
  - apps/learning/tests.py
  - staticfiles/core/studytrack-theme.css
  - apps/learning/views.py
  - apps/learning/templates/learning/course_list.html
  - staticfiles/final-study/css/study-calendar.css.gz
  - staticfiles/facebook/js/fbconnect.js.gz
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - apps/learning/models.py
  - config/settings/base.py
  - apps/core/templates/core/dashboard.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/staticfiles.json
  - apps/core/static/core/studytrack-theme.css
  - config/settings/dev.py
  - apps/learning/forms.py
  - staticfiles/final-study/css/home.css
  - staticfiles/core/studytrack-theme.css.gz
  - static/final-study/css/home.css
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - apps/learning/urls.py
  - apps/core/templates/core/includes/navbar.html
  - apps/core/views.py
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->
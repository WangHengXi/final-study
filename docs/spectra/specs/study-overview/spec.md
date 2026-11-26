# study-overview Specification

## Purpose

The study overview provides an authenticated personal entry point without replacing the public product homepage. It summarizes current study work and gives users a stable hub for their planning tools.

## Requirements

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

<!-- @trace
source: separate-public-home-and-study-overview
updated: 2026-11-26
code:
  - apps/core/static/core/studytrack-theme.css
  - apps/learning/urls.py
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - staticfiles/facebook/js/fbconnect.js.gz
  - staticfiles/final-study/js/course-list.js
  - apps/core/static/core/navbar.css
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/learning/templates/learning/course_list.html
  - apps/core/views.py
  - staticfiles/final-study/css/course-list.css
  - config/settings/dev.py
  - staticfiles/final-study/js/course-list.js.gz
  - .env.example
  - apps/learning/templates/learning/course_setting_form.html
  - apps/core/tests.py
  - config/settings/base.py
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/core/studytrack-theme.css
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/facebook/js/fbconnect.js
  - apps/learning/models.py
  - apps/learning/templates/learning/course_form.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - apps/learning/templates/learning/question_form.html
  - apps/learning/templates/learning/study_task_form.html
  - apps/learning/migrations/0007_studytask.py
  - apps/learning/templates/learning/study_calendar.html
  - apps/learning/tests.py
  - static/final-study/css/home.css
  - apps/core/urls.py
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - apps/core/templates/core/includes/navbar.html
  - apps/learning/views.py
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - staticfiles/final-study/css/study-calendar.css.gz
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - staticfiles/final-study/css/home.css
  - apps/core/templates/core/home.html
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/staticfiles.json
  - apps/learning/forms.py
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - staticfiles/core/studytrack-theme.css.gz
  - apps/core/templates/core/dashboard.html
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - staticfiles/final-study/css/study-calendar.css
  - apps/learning/templates/learning/course_detail.html
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->
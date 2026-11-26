# study-dashboard Specification

## Purpose

The study dashboard is the authenticated starting point for daily preparation. It presents a learner's work for the current date and routes them to calendar planning and course management.

## Requirements

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


<!-- @trace
source: refresh-landing-and-add-study-calendar
updated: 2026-11-26
code:
  - apps/core/templates/core/includes/navbar.html
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/core/views.py
  - apps/learning/templates/learning/question_form.html
  - apps/core/templates/core/dashboard.html
  - apps/learning/templates/learning/course_setting_form.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
  - apps/learning/urls.py
  - apps/core/static/core/studytrack-theme.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/staticfiles.json
  - static/final-study/css/home.css
  - staticfiles/final-study/css/study-calendar.css.gz
  - apps/learning/models.py
  - apps/core/urls.py
  - config/settings/dev.py
  - staticfiles/core/studytrack-theme.css
  - apps/learning/templates/learning/study_task_form.html
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/core/studytrack-theme.css.gz
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - staticfiles/final-study/css/home.css
  - staticfiles/final-study/js/course-list.js.gz
  - apps/core/tests.py
  - apps/learning/forms.py
  - apps/learning/tests.py
  - apps/core/static/core/navbar.css
  - staticfiles/final-study/css/study-calendar.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - apps/learning/views.py
  - config/settings/base.py
  - staticfiles/facebook/js/fbconnect.js
  - apps/learning/templates/learning/course_detail.html
  - apps/learning/templates/learning/study_calendar.html
  - staticfiles/facebook/js/fbconnect.js.gz
  - .env.example
  - apps/core/templates/core/home.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - staticfiles/final-study/css/course-list.css
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - apps/learning/templates/learning/course_form.html
  - apps/learning/migrations/0007_studytask.py
  - apps/learning/templates/learning/course_list.html
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - staticfiles/final-study/js/course-list.js
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->

---
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

<!-- @trace
source: refresh-landing-and-add-study-calendar
updated: 2026-11-26
code:
  - apps/core/templates/core/includes/navbar.html
  - staticfiles/core/studytrack-theme.1548516580d0.css.gz
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js.gz
  - apps/core/views.py
  - apps/learning/templates/learning/question_form.html
  - apps/core/templates/core/dashboard.html
  - apps/learning/templates/learning/course_setting_form.html
  - static/final-study/css/study-calendar.css
  - staticfiles/final-study/css/course-list.665fc8c21769.css.gz
  - staticfiles/final-study/js/course-list.f6e433f1b9fb.js
  - apps/learning/urls.py
  - apps/core/static/core/studytrack-theme.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js.gz
  - staticfiles/final-study/css/course-list.css.gz
  - staticfiles/staticfiles.json
  - static/final-study/css/home.css
  - staticfiles/final-study/css/study-calendar.css.gz
  - apps/learning/models.py
  - apps/core/urls.py
  - config/settings/dev.py
  - staticfiles/core/studytrack-theme.css
  - apps/learning/templates/learning/study_task_form.html
  - staticfiles/core/studytrack-theme.1548516580d0.css
  - staticfiles/final-study/css/home.css.gz
  - staticfiles/core/studytrack-theme.css.gz
  - staticfiles/final-study/css/home.6d88c3e6e35b.css
  - staticfiles/final-study/css/home.css
  - staticfiles/final-study/js/course-list.js.gz
  - apps/core/tests.py
  - apps/learning/forms.py
  - apps/learning/tests.py
  - apps/core/static/core/navbar.css
  - staticfiles/final-study/css/study-calendar.css
  - staticfiles/facebook/js/fbconnect.7274cde18d11.js
  - staticfiles/final-study/css/course-list.665fc8c21769.css
  - apps/learning/views.py
  - config/settings/base.py
  - staticfiles/facebook/js/fbconnect.js
  - apps/learning/templates/learning/course_detail.html
  - apps/learning/templates/learning/study_calendar.html
  - staticfiles/facebook/js/fbconnect.js.gz
  - .env.example
  - apps/core/templates/core/home.html
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css.gz
  - staticfiles/final-study/css/course-list.css
  - staticfiles/final-study/css/study-calendar.ace1e748b3f7.css
  - apps/learning/templates/learning/course_form.html
  - apps/learning/migrations/0007_studytask.py
  - apps/learning/templates/learning/course_list.html
  - staticfiles/final-study/css/home.6d88c3e6e35b.css.gz
  - staticfiles/final-study/js/course-list.js
tests:
  - apps/core/test_navigation.py
  - apps/core/test_visual_theme.py
-->
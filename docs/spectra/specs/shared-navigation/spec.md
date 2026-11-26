# shared-navigation Specification

## Purpose

提供一致且可安全渲染的全站導航與模板框架，減少 Django 模板的重複 head 與登入狀態標記，同時保留各頁的情境式導覽與既有視覺行為。

## Requirements

### Requirement: Shared application shell

The system SHALL provide a core-owned base template that lets user-facing pages supply their title, page-specific CSS, optional vendor assets, navigation override, and page content through documented template blocks.

#### Scenario: A learning page uses the shared shell

- **WHEN** an authenticated user requests a course list, course detail, course creation, question creation, or course-setting page
- **THEN** the response is rendered through the core base template
- **AND** it retains that page's existing `static/final-study/css/` stylesheet link
- **AND** it contains exactly one Tailwind CDN script.

##### Example: Course list retains its page stylesheet

- **GIVEN** an authenticated user requests `/learning/courses/`
- **WHEN** Django renders the response
- **THEN** the response contains `/static/final-study/css/course-list.css`
- **AND** it contains one `https://cdn.tailwindcss.com` script.

#### Scenario: The home page preserves its existing vendor asset behavior

- **WHEN** a visitor requests the home page
- **THEN** the response is rendered through the core base template
- **AND** it retains the home stylesheet and core theme stylesheet links
- **AND** it does not add a Tailwind CDN script.

##### Example: Home page does not add Tailwind

- **GIVEN** a visitor requests `/`
- **WHEN** Django renders the response
- **THEN** the response contains `/static/final-study/css/home.css` and `/static/core/studytrack-theme.css`
- **AND** it does not contain `https://cdn.tailwindcss.com`.


<!-- @trace
source: shared-core-navbar
updated: 2026-11-16
code:
  - apps/core/templates/core/includes/navbar.html
  - static/final-study/css/course-setting-form.css
  - static/final-study/css/question-form.css
  - apps/core/static/core/navbar.css
  - AGENTS.md
  - static/final-study/css/account.css
  - apps/learning/templates/learning/question_form.html
  - .agents/skills/spectra-discuss/SKILL.md
  - .agents/skills/spectra-debug/SKILL.md
  - .agents/skills/spectra-audit/SKILL.md
  - templates/account/logout.html
  - static/final-study/css/course-detail.css
  - apps/core/templates/core/base.html
  - apps/learning/templates/learning/course_list.html
  - .agents/skills/spectra-propose/SKILL.md
  - CLAUDE.md
  - .agents/skills/spectra-apply/SKILL.md
  - templates/account/signup.html
  - templates/account/login.html
  - apps/learning/templates/learning/course_detail.html
  - .agents/skills/spectra-ingest/SKILL.md
  - .agents/skills/spectra-review/SKILL.md
  - config/settings/base.py
  - .agents/skills/spectra-commit/SKILL.md
  - .agents/skills/spectra-analyze/SKILL.md
  - apps/core/static/core/studytrack-theme.css
  - static/final-study/css/course-list.css
  - .agents/skills/spectra-verify/SKILL.md
  - .spectra.yaml
  - apps/core/templates/core/home.html
  - .agents/skills/spectra-drift/SKILL.md
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_form.html
  - apps/core/tests.py
  - .agents/skills/spectra-archive/SKILL.md
  - static/final-study/css/home.css
  - static/final-study/js/.gitkeep
tests:
  - apps/core/test_static_assets.py
  - apps/core/test_navigation.py
-->

---
### Requirement: Guest navigation

The default shared navbar SHALL give visitors access to the StudyTrack home page, login page, and signup page.

#### Scenario: A visitor views an account page

- **WHEN** an unauthenticated visitor requests the login or signup page
- **THEN** the response contains a brand link to the home page
- **AND** it contains links to login and signup
- **AND** it does not require a UserProfile to render.

##### Example: Login page shows all guest entry points

- **GIVEN** an unauthenticated visitor requests `/accounts/login/`
- **WHEN** Django renders the response
- **THEN** the navbar contains links to `/`, `/accounts/login/`, and `/accounts/signup/`.


<!-- @trace
source: shared-core-navbar
updated: 2026-11-16
code:
  - apps/core/templates/core/includes/navbar.html
  - static/final-study/css/course-setting-form.css
  - static/final-study/css/question-form.css
  - apps/core/static/core/navbar.css
  - AGENTS.md
  - static/final-study/css/account.css
  - apps/learning/templates/learning/question_form.html
  - .agents/skills/spectra-discuss/SKILL.md
  - .agents/skills/spectra-debug/SKILL.md
  - .agents/skills/spectra-audit/SKILL.md
  - templates/account/logout.html
  - static/final-study/css/course-detail.css
  - apps/core/templates/core/base.html
  - apps/learning/templates/learning/course_list.html
  - .agents/skills/spectra-propose/SKILL.md
  - CLAUDE.md
  - .agents/skills/spectra-apply/SKILL.md
  - templates/account/signup.html
  - templates/account/login.html
  - apps/learning/templates/learning/course_detail.html
  - .agents/skills/spectra-ingest/SKILL.md
  - .agents/skills/spectra-review/SKILL.md
  - config/settings/base.py
  - .agents/skills/spectra-commit/SKILL.md
  - .agents/skills/spectra-analyze/SKILL.md
  - apps/core/static/core/studytrack-theme.css
  - static/final-study/css/course-list.css
  - .agents/skills/spectra-verify/SKILL.md
  - .spectra.yaml
  - apps/core/templates/core/home.html
  - .agents/skills/spectra-drift/SKILL.md
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_form.html
  - apps/core/tests.py
  - .agents/skills/spectra-archive/SKILL.md
  - static/final-study/css/home.css
  - static/final-study/js/.gitkeep
tests:
  - apps/core/test_static_assets.py
  - apps/core/test_navigation.py
-->

---
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
### Requirement: Page-specific navigation remains available

The shared navbar SHALL not remove existing context-specific return links or replace the home page's existing branded header.

#### Scenario: A course detail page retains its return link

- **WHEN** a user requests a course detail page
- **THEN** the response contains the existing link back to the course list.

##### Example: Course detail retains the course-list return target

- **GIVEN** an authenticated course owner requests `/learning/courses/<course_id>/`
- **WHEN** Django renders the response
- **THEN** the response contains a link to `/learning/courses/` labelled `回到課程列表`.

#### Scenario: The home page avoids duplicate navigation

- **WHEN** a visitor requests the home page
- **THEN** the response contains the existing brand-and-tagline header
- **AND** it does not render the default shared navbar in addition to that header.

##### Example: Home page has one branded header

- **GIVEN** a visitor requests `/`
- **WHEN** Django renders the response
- **THEN** the response contains the existing header note `把每一次練習，收進自己的節奏。`
- **AND** it does not contain the default navbar identifier.

<!-- @trace
source: shared-core-navbar
updated: 2026-11-16
code:
  - apps/core/templates/core/includes/navbar.html
  - static/final-study/css/course-setting-form.css
  - static/final-study/css/question-form.css
  - apps/core/static/core/navbar.css
  - AGENTS.md
  - static/final-study/css/account.css
  - apps/learning/templates/learning/question_form.html
  - .agents/skills/spectra-discuss/SKILL.md
  - .agents/skills/spectra-debug/SKILL.md
  - .agents/skills/spectra-audit/SKILL.md
  - templates/account/logout.html
  - static/final-study/css/course-detail.css
  - apps/core/templates/core/base.html
  - apps/learning/templates/learning/course_list.html
  - .agents/skills/spectra-propose/SKILL.md
  - CLAUDE.md
  - .agents/skills/spectra-apply/SKILL.md
  - templates/account/signup.html
  - templates/account/login.html
  - apps/learning/templates/learning/course_detail.html
  - .agents/skills/spectra-ingest/SKILL.md
  - .agents/skills/spectra-review/SKILL.md
  - config/settings/base.py
  - .agents/skills/spectra-commit/SKILL.md
  - .agents/skills/spectra-analyze/SKILL.md
  - apps/core/static/core/studytrack-theme.css
  - static/final-study/css/course-list.css
  - .agents/skills/spectra-verify/SKILL.md
  - .spectra.yaml
  - apps/core/templates/core/home.html
  - .agents/skills/spectra-drift/SKILL.md
  - apps/learning/templates/learning/course_setting_form.html
  - apps/learning/templates/learning/course_form.html
  - apps/core/tests.py
  - .agents/skills/spectra-archive/SKILL.md
  - static/final-study/css/home.css
  - static/final-study/js/.gitkeep
tests:
  - apps/core/test_static_assets.py
  - apps/core/test_navigation.py
-->
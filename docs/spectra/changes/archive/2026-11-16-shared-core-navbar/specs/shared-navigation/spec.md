## Purpose

提供一致且可安全渲染的全站導航與模板框架，減少 Django 模板的重複 head 與登入狀態標記，同時保留各頁的情境式導覽與既有視覺行為。

## ADDED Requirements

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

### Requirement: Authenticated navigation

The default shared navbar SHALL give authenticated users access to the StudyTrack home page, their course list, and a safe logout action without requiring a UserProfile.

#### Scenario: An authenticated user without a UserProfile views a learning page

- **WHEN** an authenticated Django user without a UserProfile requests a course list page they are authorized to access
- **THEN** the response renders successfully
- **AND** the navbar contains links to the home page and course list
- **AND** the navbar contains a POST logout form with a CSRF token.

##### Example: User without a profile can navigate

- **GIVEN** an authenticated user named `no-profile-user` has no UserProfile and requests `/learning/courses/`
- **WHEN** Django renders the response
- **THEN** the response status is 200
- **AND** the navbar contains links to `/` and `/learning/courses/`
- **AND** it contains a POST form targeting `/accounts/logout/` with `csrfmiddlewaretoken`.

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

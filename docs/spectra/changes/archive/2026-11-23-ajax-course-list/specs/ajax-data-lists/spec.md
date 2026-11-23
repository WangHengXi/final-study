## Purpose

AJAX data lists provide paginated backend data to interactive list pages without full-page refreshes. They establish consistent loading, empty, and error behavior for the course list and for future backend-backed lists.

## ADDED Requirements

### Requirement: Authenticated paginated course data

The system SHALL provide an authenticated JSON endpoint at `/learning/courses/data/` for the requesting user's courses. The endpoint SHALL accept an optional `q` query parameter and a positive integer `page` query parameter, defaulting to page 1, and SHALL return at most 10 courses per page in descending creation order. A successful response SHALL include each course's id, name, code, display name of its owner, and detail URL, plus `page`, `page_size`, `total_count`, and `total_pages` pagination metadata. The `q` filter SHALL match course names case-insensitively and SHALL use the same trimmed search value as the course list page.

#### Scenario: A user reads a filtered second page

- **GIVEN** the authenticated user owns more than 10 courses whose names match the supplied query
- **WHEN** the user requests the data endpoint with that `q` value and `page=2`
- **THEN** the response is JSON containing only that user's second page of matching courses
- **AND** the response includes the matching total count and pagination metadata.

##### Example: Page size boundary

- **GIVEN** the user owns 11 courses matching `q=math`
- **WHEN** the user requests `q=math&page=2`
- **THEN** the response reports `page` as 2, `page_size` as 10, `total_count` as 11, and `total_pages` as 2
- **AND** `items` contains one course.

#### Scenario: Invalid page input is rejected as JSON

- **WHEN** an authenticated user requests the data endpoint with a non-positive or non-integer `page` value
- **THEN** the response status is 400
- **AND** the response is JSON that identifies the invalid request without exposing internal implementation details.

#### Scenario: An unauthenticated request does not receive an HTML login page as data

- **WHEN** an unauthenticated visitor requests the data endpoint
- **THEN** the response status is 401
- **AND** the response is JSON that identifies authentication as required.

### Requirement: AJAX course-list interaction states

The course-list page SHALL load course data from the course data endpoint after the page shell renders, rather than rendering the course cards from the initial HTML response. The page SHALL submit searches and page changes without a full-page navigation, reset pagination to page 1 when the search query changes, and keep the active `q` and `page` values in the browser URL.

#### Scenario: Initial course data is loading

- **WHEN** an authenticated user opens the course-list page before its first data response completes
- **THEN** the page shows a loading indicator in the list region
- **AND** the list region communicates that its content is loading to assistive technology.

#### Scenario: A search replaces the current results

- **GIVEN** the user is viewing a page other than page 1
- **WHEN** the user submits a new search term
- **THEN** the page requests page 1 using that search term without a full-page reload
- **AND** the browser URL represents the new term and page 1
- **AND** the returned results replace the prior course cards and pagination controls.

#### Scenario: A later request is in progress

- **GIVEN** the course-list page already displays a successful result set
- **WHEN** the user searches or selects another page
- **THEN** the page keeps the successful result set visible while indicating that updated results are loading
- **AND** it prevents duplicate requests from the same control.

#### Scenario: A course search has no matches

- **WHEN** a successful course data response contains no items for a supplied search term
- **THEN** the page presents a no-results message that distinguishes it from a data-loading failure
- **AND** it offers a way to clear the search.

#### Scenario: Course data cannot be loaded

- **WHEN** the initial course data request fails because of a network, server, malformed-response, or authentication error
- **THEN** the page presents an error state with a retry control
- **AND** it does not present the failure as an empty course list.

#### Scenario: An update request fails after results are visible

- **GIVEN** the course-list page already displays a successful result set
- **WHEN** a later search or page request fails
- **THEN** the page preserves the prior successful result set
- **AND** it announces the failure and provides a retry control for the failed request.

### Requirement: Backend data-list convention

Every new user-facing list that retrieves its items from the backend SHALL use an AJAX data endpoint and SHALL define paginated responses, a loading state, an empty-result state, and an error state with recovery action before implementation. Static navigation lists and lists whose items are fully available in the initial page markup are outside this requirement.

#### Scenario: A future backend-backed list is proposed

- **WHEN** a future change introduces a user-facing list whose items come from backend data
- **THEN** its specification defines an AJAX retrieval interface, pagination behavior, loading behavior, empty-result behavior, and an error recovery action.

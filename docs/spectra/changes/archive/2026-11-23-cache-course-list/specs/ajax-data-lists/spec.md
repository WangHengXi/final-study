## ADDED Requirements

### Requirement: User-isolated cached course data

The course data endpoint SHALL cache successful paginated course payloads using the configured default cache timeout. A cache identity SHALL include the authenticated user's identity, the trimmed search value, the requested page, and that user's course-list cache version. The endpoint SHALL NOT share a cached payload between users, searches, pages, or cache versions, and SHALL NOT cache authentication or validation errors.

#### Scenario: A repeated course-list request uses its own cached payload

- **GIVEN** an authenticated user's successful request for `q=math&page=1` has populated the cache
- **WHEN** the same user requests `q=math&page=1` again before the cached payload expires or is invalidated
- **THEN** the endpoint returns the same JSON payload from that user's cache
- **AND** it does not use another user's cached payload.

#### Scenario: Different query states do not share cached results

- **GIVEN** an authenticated user's successful request for `q=math&page=1` has populated the cache
- **WHEN** that user requests `q=english&page=1` or `q=math&page=2`
- **THEN** the endpoint uses a distinct cache identity for that request state.

### Requirement: Course creation invalidates cached course lists

After a course is successfully created for a user, the system SHALL advance that user's course-list cache version. Subsequent requests by that user SHALL bypass payloads from the earlier version and SHALL return a payload that includes the new course when it matches the request filter. Cache invalidation SHALL NOT affect another user's course-list cache version.

#### Scenario: A newly created course appears after cached empty results

- **GIVEN** an authenticated user's unfiltered course-list request has cached an empty payload
- **WHEN** that user creates a course named `Calculus` with code `MATH101`
- **THEN** the user's next unfiltered course-list request returns a payload containing `Calculus`
- **AND** another user's cached course-list version remains unchanged.

#### Scenario: The cache backend is unavailable

- **WHEN** the course data endpoint cannot read from or write to the configured cache backend
- **THEN** it returns the same authorized, paginated JSON payload by querying the database
- **AND** it does not expose cache-backend details in the response.

##### Example: Read failure falls back to course data

- **GIVEN** the authenticated user owns a course named `Calculus`
- **AND** the cache read raises an exception
- **WHEN** the user requests the first unfiltered course-data page
- **THEN** the response status is 200 and its items contain `Calculus`
- **AND** the response body does not contain the cache exception detail.

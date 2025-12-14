# Performance Report

## Test Setup
- Generated data: 100 users, 500 datasets, 50,000+ lines using scripts/performance-test.py
- Test date: 2025-12-15
- Flask app running locally on http://127.0.0.1:5000

## Database Seeding Performance

**Bulk data creation timing:**
- 100 users: 10.39s
- 500 datasets: <0.01s
- 50,000 lines: 0.21s 
- 6 tags + assignments: <0.01s
- **Total time: 10.62 seconds**

#### Observations
- This demonstrates the application can handle large-scale bulk database insertions efficiently. Most time spent on password hashing (users), while raw database writes are very fast.

## Automated Endpoint Testing

#### Methodology
- Testing tool: Custom Python script (scripts/performance_test.py) using requests library
- Measured HTTP GET request response times from request to response
- Each endpoint tested multiple times for consistency

#### Results

**Measured Response Times:**
- **Homepage (page 1)**: 69ms
- **Homepage (page 5)**: 8ms  
- **Search for 'test'**: 17ms
- **Search (no results)**: 3ms
- **Dataset #1**: 34ms
- **Dataset #10**: 7ms
- **User #1 profile**: 47ms

**Summary Statistics:**
- Average response time: 26ms
- Slowest endpoint: Homepage first page (69ms)
- Fastest endpoint: Empty search results (3ms)

#### Observations
- All endpoints respond in under 100ms
- Pagination performs efficiently, subsequent pages load faster
- Search functionality very fast even with 500 datasets
- No significant performance degradation with large dataset

## Manual Write Operations Testing

#### Methodology
- Browser: Chrome with DevTools Network tab
- Measured time from form submission to page reload/redirect
- Tested with large dataset already seeded in database

#### Results

**User Operations:**
- Creating new user account: ~134ms
- User login: ~115ms

**Dataset Operations:**
- Creating new dataset: ~24ms
- Editing dataset description: ~17ms
- Deleting dataset: ~25ms

**Bulk Line Operations:**
- Adding 100 lines (bulk paste): ~1170ms
- Adding 1000 lines (bulk paste): ~12200ms

**Comment Operations:**
- Adding single comment: ~15ms
- Deleting comment: ~23ms

**Tag Operations:**
- Adding tag to dataset: ~22ms
- Removing tag from dataset: ~18ms

#### Observations
- Single operations (create, edit, delete) complete in under 150ms - fast and responsive
- Bulk line addition scales linearly: 10x lines = 10x time, no exponential degradation
- Application handles 1000+ line insertions without issues (~12ms per line)
- Comment and tag operations very fast (~15-25ms)
- No crashes or errors observed during testing

## Conclusion

Application performs well with large datasets for both read and write operations. All tested endpoints respond quickly with no critical bottlenecks identified. The pagination system effectively handles hundreds of datasets without performance issues. Write operations complete in acceptable timeframes even with bulk data.
# Restful Booker API - Detailed Test Checklist

**API Base URL:** `https://restful-booker.herokuapp.com`  
**Last Updated:** 2026-01-15  
**Status:** 0/150 tests implemented  

---

## 1. Authentication API

### **POST /auth** - Create Authentication Token

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|-----|-------|
| AUTH-001 | Valid credentials (username:  admin, password: password123) | High | **200 OK** | `{"token": "abc123"}` | ✔️ | Token string returned |
| AUTH-002 | Invalid username | High | **200 OK** | `{"reason": "Bad credentials"}` | ❌ | Note: API returns 200, not 401 |
| AUTH-003 | Invalid password | High | **200 OK** | `{"reason": "Bad credentials"}` | ❌ | Note: API returns 200, not 401 |
| AUTH-004 | Missing username field | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | |
| AUTH-005 | Missing password field | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | |
| AUTH-006 | Empty username | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | |
| AUTH-007 | Empty password | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | |
| AUTH-008 | Empty request body | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | |
| AUTH-009 | Null values for credentials | Medium | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | |
| AUTH-010 | SQL injection in username | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | Security test |
| AUTH-011 | XSS payload in username | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | Security test |
| AUTH-012 | Very long username (1000+ chars) | Low | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | Boundary test |
| AUTH-013 | Special characters in credentials | Medium | **200 OK** | Valid response based on actual credentials | ✔️ | |
| AUTH-014 | Response time < 2000ms | Medium | **200 OK** | Response within acceptable time | ✔️ | Performance |
| AUTH-015 | Token format validation | High | **200 OK** | Token is alphanumeric string | ✔️ | Verify token structure |
| AUTH-016 | Content-Type header validation | Medium | **200 OK** | Response header:  `application/json` | ✔️ | |
| AUTH-017 | Invalid Content-Type in request | Low | **200/415** | Error or Bad credentials | ✔️ | |

**Request Example:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Success Response Example:**
```json
{
  "token": "abc123def456"
}
```

**Failure Response Example:**
```json
{
  "reason": "Bad credentials"
}
```

---

## 2. Health Check API

### **GET /ping** - Health Check

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| PING-001 | API is reachable | High | **201 Created** | Plain text:  "Created" | ✔️| Confirms API is running |
| PING-002 | Response time < 1000ms | Medium | **201 Created** | Response within 1 second | ✔️| Performance check |
| PING-003 | No authentication required | High | **201 Created** | Success without token | ✔️| Public endpoint |
| PING-004 | Response headers include Content-Type | Low | **201 Created** | Headers present | ✔️| |

---

## 3. Booking API - Retrieve Operations

### **GET /booking** - Get All Booking IDs

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| GET-001 | Get all booking IDs without filters | High | **200 OK** | `[{"bookingid": 1}, {"bookingid": 2}]` | ✔️| Array of booking objects |
| GET-002 | Filter by firstname | High | **200 OK** | Filtered array of bookings | ✔️| `? firstname=John` |
| GET-003 | Filter by lastname | High | **200 OK** | Filtered array of bookings | ✔️| `?lastname=Smith` |
| GET-004 | Filter by checkin date | High | **200 OK** | Filtered array of bookings | ✔️| `?checkin=2024-01-01` |
| GET-005 | Filter by checkout date | High | **200 OK** | Filtered array of bookings | ✔️| `?checkout=2024-01-10` |
| GET-006 | Filter by firstname AND lastname | Medium | **200 OK** | Filtered array matching both | ✔️| Combined filters |
| GET-007 | Filter by checkin AND checkout dates | Medium | **200 OK** | Filtered array within date range | ✔️| Date range query |
| GET-008 | Filter with all parameters | Medium | **200 OK** | Filtered array matching all criteria | ✔️| `?firstname=X&lastname=Y&checkin=Z&checkout=W` |
| GET-009 | No matching results | Medium | **200 OK** | `[]` (empty array) | ✔️| Valid filter but no matches |
| GET-010 | Invalid date format in filter | Low | **200/400** | Empty array or error | ✔️| `?checkin=invalid-date` |
| GET-011 | Special characters in firstname | Medium | **200 OK** | Filtered results or empty array | ✔️| Test encoding |
| GET-012 | Case sensitivity in name filters | Medium | **200 OK** | Check if case-sensitive or not | ✔️| `firstname=john` vs `firstname=John` |
| GET-013 | Response time < 2000ms | Medium | **200 OK** | Response within acceptable time | ✔️| Performance |
| GET-014 | Response is valid JSON array | High | **200 OK** | Valid JSON structure | ✔️| Schema validation |
| GET-015 | Each booking has bookingid field | High | **200 OK** | All objects contain `bookingid` | ✔️| Data validation |
| GET-016 | BookingID is numeric | High | **200 OK** | All bookingid values are numbers | ✔️| Data type validation |
| GET-017 | No authentication required | High | **200 OK** | Success without token | ✔️| Public endpoint |
| GET-018 | Large result set performance | Low | **200 OK** | Handle large number of bookings | ✔️| Load test |

**Success Response Example:**
```json
[
  {"bookingid": 1},
  {"bookingid": 2},
  {"bookingid": 3}
]
```

---

### **GET /booking/:id** - Get Specific Booking Details

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| GET-ID-001 | Get existing booking with valid ID | High | **200 OK** | Full booking object with all fields | ✔️| Returns complete booking details |
| GET-ID-002 | Verify all required fields present | High | **200 OK** | Contains:  firstname, lastname, totalprice, depositpaid, bookingdates, additionalneeds | ✔️| Schema validation |
| GET-ID-003 | Verify bookingdates structure | High | **200 OK** | `bookingdates:  {checkin: "date", checkout: "date"}` | ✔️| Nested object validation |
| GET-ID-004 | Verify data types - firstname | High | **200 OK** | firstname is string | ✔️| Type validation |
| GET-ID-005 | Verify data types - lastname | High | **200 OK** | lastname is string | ✔️| Type validation |
| GET-ID-006 | Verify data types - totalprice | High | **200 OK** | totalprice is number | ✔️| Type validation |
| GET-ID-007 | Verify data types - depositpaid | High | **200 OK** | depositpaid is boolean | ✔️| Type validation |
| GET-ID-008 | Verify date format (YYYY-MM-DD) | High | **200 OK** | Dates in ISO format | ✔️| Date format validation |
| GET-ID-009 | Non-existent booking ID | High | **404 Not Found** | "Not Found" (text) | ✔️| Invalid ID |
| GET-ID-010 | Invalid booking ID (string) | Medium | **404 Not Found** | "Not Found" | ✔️| `/booking/invalid` |
| GET-ID-011 | Negative booking ID | Medium | **404 Not Found** | "Not Found" | ✔️| `/booking/-1` |
| GET-ID-012 | Zero booking ID | Medium | **404 Not Found** | "Not Found" | ✔️| `/booking/0` |
| GET-ID-013 | Very large booking ID | Medium | **404 Not Found** | "Not Found" | ✔️| `/booking/999999999` |
| GET-ID-014 | Booking ID with special characters | Medium | **404 Not Found** | "Not Found" | ✔️| `/booking/123@#$` |
| GET-ID-015 | Response time < 1500ms | Medium | **200 OK** | Response within acceptable time | ✔️| Performance |
| GET-ID-016 | No authentication required | High | **200 OK** | Success without token | ✔️| Public endpoint |
| GET-ID-017 | Content-Type is application/json | Medium | **200 OK** | Response header correct | ✔️| Header validation |
| GET-ID-018 | Accept header variations | Low | **200 OK** | Handles different Accept headers | ✔️| `Accept: application/json` |

**Success Response Example:**
```json
{
  "firstname": "John",
  "lastname": "Smith",
  "totalprice": 111,
  "depositpaid": true,
  "bookingdates": {
    "checkin":  "2018-01-01",
    "checkout": "2019-01-01"
  },
  "additionalneeds":  "Breakfast"
}
```

**Error Response Example:**
```
Not Found
```

---

## 4. Booking API - Create Operation

### **POST /booking** - Create New Booking

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| POST-001 | Create booking with all valid required fields | High | **200 OK** | Full booking object with bookingid | ✔️| Success case |
| POST-002 | Verify bookingid is generated | High | **200 OK** | Response contains numeric bookingid | ✔️| ID generation |
| POST-003 | Verify created booking can be retrieved | High | **200 OK** | GET /booking/: id returns same data | ✔️| End-to-end validation |
| POST-004 | Create with additionalneeds field | High | **200 OK** | Field included in response | ✔️| Optional field |
| POST-005 | Create without additionalneeds field | High | **200 OK** | Success without optional field | ✔️| Optional field omitted |
| POST-006 | Missing firstname field | High | **500 Internal Server Error** | Server error | ✔️| Required field validation |
| POST-007 | Missing lastname field | High | **500 Internal Server Error** | Server error | ✔️| Required field validation |
| POST-008 | Missing totalprice field | High | **500 Internal Server Error** | Server error | ✔️| Required field validation |
| POST-009 | Missing depositpaid field | High | **500 Internal Server Error** | Server error | ✔️| Required field validation |
| POST-010 | Missing bookingdates object | High | **500 Internal Server Error** | Server error | ✔️| Required field validation |
| POST-011 | Missing checkin date | High | **500 Internal Server Error** | Server error | ✔️| Required nested field |
| POST-012 | Missing checkout date | High | **500 Internal Server Error** | Server error | ✔️| Required nested field |
| POST-013 | Empty firstname | Medium | **200/500** | Check API behavior | ✔️| Empty string validation |
| POST-014 | Empty lastname | Medium | **200/500** | Check API behavior | ✔️| Empty string validation |
| POST-015 | Null firstname | Medium | **500 Internal Server Error** | Server error | ✔️| Null validation |
| POST-016 | Null lastname | Medium | **500 Internal Server Error** | Server error | ✔️| Null validation |
| POST-017 | Negative totalprice | Medium | **200 OK** | Accepts negative values (check behavior) | ✔️| Business logic validation |
| POST-018 | Zero totalprice | Medium | **200 OK** | Accepts zero | ✔️| Boundary value |
| POST-019 | Decimal totalprice | Medium | **200 OK** | Accepts decimal values | ✔️| `111.50` |
| POST-020 | Very large totalprice | Low | **200 OK** | Handles large numbers | ✔️| `999999999` |
| POST-021 | String value for totalprice | High | **500 Internal Server Error** | Type mismatch error | ✔️| `"abc"` |
| POST-022 | String value for depositpaid | Medium | **500 Internal Server Error** | Type mismatch error | ✔️| `"yes"` |
| POST-023 | Non-boolean depositpaid (1/0) | Medium | **200/500** | Check if accepts numeric boolean | ✔️| Type coercion test |
| POST-024 | Invalid checkin date format | High | **500 Internal Server Error** | Date validation error | ✔️| `"01-01-2024"` |
| POST-025 | Invalid checkout date format | High | **500 Internal Server Error** | Date validation error | ✔️| `"2024/01/01"` |
| POST-026 | Checkout date before checkin date | Medium | **200 OK** | API may not validate this | ✔️| Business logic |
| POST-027 | Same checkin and checkout dates | Medium | **200 OK** | Check API behavior | ✔️| Edge case |
| POST-028 | Future dates (valid scenario) | High | **200 OK** | Accepts future bookings | ✔️| Valid use case |
| POST-029 | Past dates | Medium | **200 OK** | Check if historical bookings allowed | ✔️| Business logic |
| POST-030 | Special characters in firstname | Medium | **200 OK** | `"Seán"`, `"José"` | ✔️| Unicode support |
| POST-031 | Special characters in lastname | Medium | **200 OK** | `"O'Brien"`, `"María"` | ✔️| Unicode support |
| POST-032 | Very long firstname (255+ chars) | Low | **200/500** | Test field length limits | ✔️| Boundary test |
| POST-033 | Very long lastname (255+ chars) | Low | **200/500** | Test field length limits | ✔️| Boundary test |
| POST-034 | Very long additionalneeds (1000+ chars) | Low | **200/500** | Test field length limits | ✔️| Boundary test |
| POST-035 | SQL injection in firstname | High | **200 OK** | Should sanitize input | ✔️| `"'; DROP TABLE--"` |
| POST-036 | XSS payload in additionalneeds | High | **200 OK** | Should sanitize input | ✔️| `"<script>alert('XSS')</script>"` |
| POST-037 | Extra unknown fields in request | Medium | **200 OK** | Should ignore extra fields | ✔️| `{"extra": "field"}` |
| POST-038 | Empty request body | High | **500 Internal Server Error** | Missing required data | ✔️| Validation |
| POST-039 | Malformed JSON | High | **400 Bad Request** | JSON parse error | ✔️| `{invalid json}` |
| POST-040 | No Content-Type header | Medium | **500/415** | May reject request | ✔️| Header validation |
| POST-041 | Wrong Content-Type (text/plain) | Medium | **500/415** | May reject request | ✔️| Header validation |
| POST-042 | Response time < 2000ms | Medium | **200 OK** | Performance benchmark | ✔️| Performance |
| POST-043 | Create multiple bookings concurrently | Low | **200 OK** | All succeed with unique IDs | ✔️| Concurrency test |
| POST-044 | Create duplicate booking data | Medium | **200 OK** | Allows duplicates with different IDs | ✔️| Business logic |
| POST-045 | Response includes all submitted data | High | **200 OK** | Echo back all fields correctly | ✔️| Data integrity |
| POST-046 | No authentication required | High | **200 OK** | Public endpoint | ✔️| Auth not needed |

**Request Example:**
```json
{
  "firstname": "Jim",
  "lastname": "Brown",
  "totalprice":  111,
  "depositpaid":  true,
  "bookingdates": {
    "checkin": "2018-01-01",
    "checkout": "2019-01-01"
  },
  "additionalneeds": "Breakfast"
}
```

**Success Response Example:**
```json
{
  "bookingid": 1,
  "booking":  {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2018-01-01",
      "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"
  }
}
```

---

## 5. Booking API - Update Operations (Full)

### **PUT /booking/: id** - Update Entire Booking

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| PUT-001 | Update with valid token and all fields | High | **200 OK** | Updated booking object | ✔️| Success case |
| PUT-002 | Update without authentication | High | **403 Forbidden** | "Forbidden" | ✔️| Auth required |
| PUT-003 | Update with invalid token | High | **403 Forbidden** | "Forbidden" | ✔️| Invalid auth |
| PUT-004 | Update with empty token | High | **403 Forbidden** | "Forbidden" | ✔️| Missing token value |
| PUT-005 | Update with Basic Auth (username/password) | High | **200 OK** | Can use Basic Auth instead | ✔️| Alternative auth method |
| PUT-006 | Update with invalid Basic Auth | High | **403 Forbidden** | "Forbidden" | ✔️| Wrong credentials |
| PUT-007 | Update non-existent booking ID | High | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Invalid ID |
| PUT-008 | Verify all fields are updated | High | **200 OK** | All submitted fields changed | ✔️| Complete replacement |
| PUT-009 | Verify unchanged fields if any | High | **200 OK** | Only submitted fields present | ✔️| No partial update |
| PUT-010 | Update firstname only (missing other fields) | High | **400/500** | Should require all fields | ✔️| PUT requires complete object |
| PUT-011 | Update with partial data | High | **400/500** | Missing required fields error | ✔️| Validation |
| PUT-012 | Missing firstname | High | **400/500** | Required field error | ✔️| Validation |
| PUT-013 | Missing lastname | High | **400/500** | Required field error | ✔️| Validation |
| PUT-014 | Missing totalprice | High | **400/500** | Required field error | ✔️| Validation |
| PUT-015 | Missing depositpaid | High | **400/500** | Required field error | ✔️| Validation |
| PUT-016 | Missing bookingdates | High | **400/500** | Required field error | ✔️| Validation |
| PUT-017 | Invalid data types (same as POST) | Medium | **400/500** | Type validation errors | ✔️| Field validation |
| PUT-018 | Update with same data (idempotency) | Medium | **200 OK** | No changes, same response | ✔️| Idempotent operation |
| PUT-019 | Update multiple times consecutively | Medium | **200 OK** | Each update succeeds | ✔️| Multiple updates |
| PUT-020 | Verify updated booking via GET | High | **200 OK** | GET returns updated data | ✔️| End-to-end validation |
| PUT-021 | Special characters in updated fields | Medium | **200 OK** | Handles special chars | ✔️| Data validation |
| PUT-022 | SQL injection in updated fields | High | **200 OK** | Should sanitize | ✔️| Security |
| PUT-023 | XSS payload in updated fields | High | **200 OK** | Should sanitize | ✔️| Security |
| PUT-024 | Empty request body | High | **400/500** | Missing data error | ✔️| Validation |
| PUT-025 | Malformed JSON | High | **400 Bad Request** | JSON parse error | ✔️| Format validation |
| PUT-026 | Wrong Content-Type header | Medium | **400/415** | Header validation | ✔️| Header check |
| PUT-027 | Response time < 2000ms | Medium | **200 OK** | Performance check | ✔️| Performance |
| PUT-028 | Token in Cookie header | High | **200 OK** | Accepts token via Cookie | ✔️| `Cookie: token=abc123` |
| PUT-029 | Token in Authorization header | Medium | **200 OK** | Check if supported | ✔️| `Authorization: Bearer abc123` |
| PUT-030 | Concurrent updates to same booking | Low | **200 OK** | Last write wins or conflict | ✔️| Race condition |

**Request Headers:**
```
Content-Type: application/json
Cookie: token=abc123
OR
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Request Body:**
```json
{
  "firstname": "James",
  "lastname": "Brown",
  "totalprice":  111,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2018-01-01",
    "checkout":  "2019-01-01"
  },
  "additionalneeds": "Breakfast"
}
```

**Success Response:**
```json
{
  "firstname": "James",
  "lastname": "Brown",
  "totalprice": 111,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2018-01-01",
    "checkout": "2019-01-01"
  },
  "additionalneeds": "Breakfast"
}
```

---

## 6. Booking API - Update Operations (Partial)

### **PATCH /booking/:id** - Partial Update Booking

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| PATCH-001 | Update firstname only with valid token | High | **200 OK** | Updated booking with changed firstname | ✔️| Partial update success |
| PATCH-002 | Update lastname only | High | **200 OK** | Updated booking with changed lastname | ✔️| Single field update |
| PATCH-003 | Update totalprice only | High | **200 OK** | Updated booking with changed price | ✔️| Single field update |
| PATCH-004 | Update depositpaid only | High | **200 OK** | Updated booking with changed depositpaid | ✔️| Single field update |
| PATCH-005 | Update checkin date only | High | **200 OK** | Updated booking with changed checkin | ✔️| Nested field update |
| PATCH-006 | Update checkout date only | High | **200 OK** | Updated booking with changed checkout | ✔️| Nested field update |
| PATCH-007 | Update both dates | Medium | **200 OK** | Both dates changed | ✔️| `{"bookingdates": {... }}` |
| PATCH-008 | Update additionalneeds only | Medium | **200 OK** | Updated optional field | ✔️| Optional field update |
| PATCH-009 | Update multiple fields (firstname + lastname) | High | **200 OK** | Multiple fields changed | ✔️| Multi-field partial update |
| PATCH-010 | Update all fields (full patch) | Medium | **200 OK** | All fields updated | ✔️| Same as PUT but via PATCH |
| PATCH-011 | Verify unchanged fields remain same | High | **200 OK** | Only patched fields change | ✔️| Critical for PATCH |
| PATCH-012 | Update without authentication | High | **403 Forbidden** | "Forbidden" | ✔️| Auth required |
| PATCH-013 | Update with invalid token | High | **403 Forbidden** | "Forbidden" | ✔️| Invalid auth |
| PATCH-014 | Update with Basic Auth | High | **200 OK** | Success with Basic Auth | ✔️| Alternative auth |
| PATCH-015 | Update non-existent booking ID | High | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Invalid ID |
| PATCH-016 | Empty request body | Medium | **200/400** | Check API behavior | ✔️| No fields to update |
| PATCH-017 | Invalid field values | High | **400/500** | Validation errors | ✔️| Wrong data types |
| PATCH-018 | Update with null values | Medium | **200/400** | Check if nulls allowed | ✔️| `{"firstname": null}` |
| PATCH-019 | Update with empty strings | Medium | **200/400** | Check if empty allowed | ✔️| `{"firstname": ""}` |
| PATCH-020 | Update with invalid date format | High | **400/500** | Date validation error | ✔️| Format check |
| PATCH-021 | Update to negative totalprice | Medium | **200 OK** | Check business logic | ✔️| Validation |
| PATCH-022 | Update with extra unknown fields | Low | **200 OK** | Ignores extra fields | ✔️| Graceful handling |
| PATCH-023 | Verify patched booking via GET | High | **200 OK** | GET returns patched data | ✔️| End-to-end validation |
| PATCH-024 | Idempotent PATCH (same data twice) | Medium | **200 OK** | Same result both times | ✔️| Idempotency |
| PATCH-025 | Multiple sequential patches | Medium | **200 OK** | Each patch succeeds | ✔️| Sequential updates |
| PATCH-026 | Special characters in patched fields | Medium | **200 OK** | Handles special chars | ✔️| Data validation |
| PATCH-027 | SQL injection in patched fields | High | **200 OK** | Should sanitize | ✔️| Security |
| PATCH-028 | XSS payload in patched fields | High | **200 OK** | Should sanitize | ✔️| Security |
| PATCH-029 | Malformed JSON | High | **400 Bad Request** | JSON parse error | ✔️| Format validation |
| PATCH-030 | Wrong Content-Type header | Medium | **400/415** | Header validation | ✔️| Header check |
| PATCH-031 | Response time < 2000ms | Medium | **200 OK** | Performance check | ✔️| Performance |
| PATCH-032 | Token in Cookie header | High | **200 OK** | Accepts token via Cookie | ✔️| Auth method |
| PATCH-033 | Concurrent patches to same booking | Low | **200 OK** | Handle race conditions | ✔️| Concurrency |

**Request Headers:**
```
Content-Type: application/json
Cookie: token=abc123
```

**Request Body (Partial Update Example):**
```json
{
  "firstname": "James",
  "totalprice": 150
}
```

**Success Response:**
```json
{
  "firstname": "James",
  "lastname": "Brown",
  "totalprice": 150,
  "depositpaid": true,
  "bookingdates":  {
    "checkin": "2018-01-01",
    "checkout": "2019-01-01"
  },
  "additionalneeds": "Breakfast"
}
```

---

## 7. Booking API - Delete Operation

### **DELETE /booking/:id** - Delete Booking

| ID | Test Case | Priority | Expected Status | Expected Response | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| DEL-001 | Delete existing booking with valid token | High | **201 Created** | "Created" | ✔️| Success case (note unusual status) |
| DEL-002 | Delete without authentication | High | **403 Forbidden** | "Forbidden" | ✔️| Auth required |
| DEL-003 | Delete with invalid token | High | **403 Forbidden** | "Forbidden" | ✔️| Invalid auth |
| DEL-004 | Delete with Basic Auth | High | **201 Created** | "Created" | ✔️| Alternative auth method |
| DEL-005 | Delete non-existent booking ID | High | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Invalid ID |
| DEL-006 | Verify deleted booking returns 404 on GET | High | **404 Not Found** | GET after DELETE returns 404 | ✔️| Deletion confirmation |
| DEL-007 | Delete already deleted booking | Medium | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Double delete |
| DEL-008 | Delete with invalid booking ID (string) | Medium | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Invalid ID type |
| DEL-009 | Delete with negative booking ID | Medium | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Invalid ID |
| DEL-010 | Delete with zero booking ID | Medium | **405 Method Not Allowed** | "Method Not Allowed" | ✔️| Invalid ID |
| DEL-011 | Verify deletion is permanent | High | **404 Not Found** | Cannot retrieve after delete | ✔️| No soft delete |
| DEL-012 | Delete and verify not in list | Medium | **200 OK** | GET /booking doesn't include deleted ID | ✔️| List verification |
| DEL-013 | Try to update deleted booking | Medium | **405 Method Not Allowed** | Cannot update deleted booking | ✔️| Operations on deleted resource |
| DEL-014 | Try to patch deleted booking | Medium | **405 Method Not Allowed** | Cannot patch deleted booking | ✔️| Operations on deleted resource |
| DEL-015 | Response time < 1500ms | Medium | **201 Created** | Performance check | ✔️| Performance |
| DEL-016 | Token in Cookie header | High | **201 Created** | Accepts token via Cookie | ✔️| Auth method |
| DEL-017 | Concurrent delete requests | Low | **201/405** | First succeeds, second fails | ✔️| Race condition |
| DEL-018 | Delete with request body (should ignore) | Low | **201 Created** | Body ignored for DELETE | ✔️| HTTP spec compliance |

**Request Headers:**
```
Cookie: token=abc123
OR
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Success Response:**
```
Created
```

---

## 8. End-to-End Workflow Tests

| ID | Test Scenario | Priority | Expected Results | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| E2E-001 | Complete booking lifecycle:  Create → Read → Update → Delete | High | All operations succeed in sequence | ✔️| Happy path |
| E2E-002 | Authenticate → Create booking → Verify in list → Get details | High | Booking appears in list and can be retrieved | ✔️| Creation workflow |
| E2E-003 | Create → Partial update → Full update → Verify changes | Medium | All updates persist correctly | ✔️| Update workflow |
| E2E-004 | Create → Search by filters → Verify found | Medium | Can find created booking via filters | ✔️| Search workflow |
| E2E-005 | Create multiple bookings → Filter by different criteria | Medium | Filters work correctly with multiple bookings | ✔️| Multi-booking scenario |
| E2E-006 | Create → Update → Delete → Verify 404 | High | Complete lifecycle with verification | ✔️| Full CRUD |
| E2E-007 | Token expiration handling | Low | Expired token returns 403 | ✔️| Token lifecycle |
| E2E-008 | Create booking → Logout → Try to update | Medium | Update fails without valid token | ✔️| Auth flow |
| E2E-009 | Concurrent users creating bookings | Low | All bookings created with unique IDs | ✔️| Multi-user scenario |
| E2E-010 | Invalid auth → Get token → Successfully update | Medium | Auth recovery workflow | ✔️| Error recovery |

---

## 9. Security Tests

| ID | Test Case | Priority | Expected Status | Expected Behavior | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| SEC-001 | SQL Injection in firstname | High | **200 OK** | Input sanitized, no SQL executed | ✔️| `' OR '1'='1` |
| SEC-002 | SQL Injection in lastname | High | **200 OK** | Input sanitized | ✔️| `'; DROP TABLE bookings--` |
| SEC-003 | SQL Injection in additionalneeds | High | **200 OK** | Input sanitized | ✔️| `1' UNION SELECT * FROM users--` |
| SEC-004 | XSS in firstname | High | **200 OK** | Script tags escaped/sanitized | ✔️| `<script>alert('XSS')</script>` |
| SEC-005 | XSS in lastname | High | **200 OK** | Script tags escaped/sanitized | ✔️| `<img src=x onerror=alert(1)>` |
| SEC-006 | XSS in additionalneeds | High | **200 OK** | Script tags escaped/sanitized | ✔️| `<svg onload=alert(1)>` |
| SEC-007 | Command injection attempts | High | **200 OK** | Commands not executed | ✔️| `; ls -la` |
| SEC-008 | Path traversal in parameters | Medium | **200/404** | No file system access | ✔️| `../../etc/passwd` |
| SEC-009 | Authentication bypass attempts | High | **403 Forbidden** | Auth cannot be bypassed | ✔️| Various bypass techniques |
| SEC-010 | Token tampering | High | **403 Forbidden** | Modified tokens rejected | ✔️| Alter token value |
| SEC-011 | Reusing old/expired tokens | Medium | **403 Forbidden** | Old tokens rejected | ✔️| Token lifecycle |
| SEC-012 | CSRF protection (if applicable) | Medium | Varies | CSRF tokens validated | ✔️| Cross-site requests |
| SEC-013 | Excessive payload size | Medium | **413/400** | Large requests rejected | ✔️| DoS prevention |
| SEC-014 | Sensitive data exposure in errors | High | **N/A** | No sensitive info in error messages | ✔️| Error content review |
| SEC-015 | HTTPS enforcement (if production) | High | **N/A** | HTTP redirects to HTTPS | ✔️| Transport security |
| SEC-016 | Rate limiting on auth endpoint | Medium | **429 Too Many Requests** | Brute force prevention | ✔️| Multiple failed logins |
| SEC-017 | Authorization checks (user isolation) | High | **403 Forbidden** | Users can only modify own bookings | ✔️| If multi-user |
| SEC-018 | XML injection (if XML supported) | Medium | **200/400** | XML input sanitized | ✔️| XML Entity Expansion |
| SEC-019 | Header injection | Medium | **400** | Invalid headers rejected | ✔️| CRLF injection |
| SEC-020 | NULL byte injection | Low | **200/400** | NULL bytes handled safely | ✔️| `%00` in strings |

---

## 10. Performance & Load Tests

| ID | Test Case | Priority | Expected Result | Status | Notes |
|----|-----------|----------|----------------|--------|-------|
| PERF-001 | Baseline response time - GET /booking | Medium | < 2000ms | ✔️| Normal load |
| PERF-002 | Baseline response time - GET /booking/: id | Medium | < 1500ms | ✔️| Normal load |
| PERF-003 | Baseline response time - POST /booking | Medium | < 2000ms | ✔️| Normal load |
| PERF-004 | Baseline response time - PUT /booking/:id | Medium | < 2000ms | ✔️| Normal load |
| PERF-005 | Baseline response time - PATCH /booking/:id | Medium | < 2000ms | ✔️| Normal load |
| PERF-006 | Baseline response time - DELETE /booking/: id | Medium | < 1500ms | ✔️| Normal load |
| PERF-007 | Load test - 50 concurrent users | Medium | 90% success rate, acceptable response time | ✔️| Concurrent requests |
| PERF-008 | Load test - 100 concurrent users | Low | Measure degradation | ✔️| High load |
| PERF-009 | Stress test - increasing load | Low | Identify breaking point | ✔️| Capacity planning |
| PERF-010 | Spike test - sudden traffic increase | Low | System recovers gracefully | ✔️| Elasticity test |
| PERF-011 | Endurance test - sustained load (30+ min) | Low | No memory leaks, stable performance | ✔️| Stability test |
| PERF-012 | Large dataset - List all bookings (1000+) | Medium | Handles large response | ✔️| Scalability |
| PERF-013 | Rapid successive creates | Medium | All succeed with unique IDs | ✔️| ID generation under load |
| PERF-014 | Rapid successive updates to same booking | Low | No data corruption | ✔️| Concurrency handling |
| PERF-015 | Response size validation | Low | Reasonable payload sizes | ✔️| Bandwidth efficiency |

---

## 11. Data Validation & Schema Tests

| ID | Test Case | Priority | Expected Result | Status | Notes |
|----|-----------|----------|----------------|--------|-------|
| SCHEMA-001 | GET /booking returns array | High | Valid JSON array | ✔️| Schema validation |
| SCHEMA-002 | GET /booking/:id matches schema | High | All required fields present | ✔️| Response structure |
| SCHEMA-003 | POST response matches schema | High | Contains bookingid and booking object | ✔️| Creation response |
| SCHEMA-004 | PUT response matches schema | High | Returns updated booking | ✔️| Update response |
| SCHEMA-005 | PATCH response matches schema | High | Returns complete booking | ✔️| Patch response |
| SCHEMA-006 | Field data types correct | High | String, number, boolean, object as expected | ✔️| Type checking |
| SCHEMA-007 | Date format consistency | High | All dates in YYYY-MM-DD format | ✔️| Date formatting |
| SCHEMA-008 | BookingID is always numeric | High | Integer type for all IDs | ✔️| ID format |
| SCHEMA-009 | Boolean fields are true/false | High | Not "yes"/"no" or 1/0 | ✔️| Boolean format |
| SCHEMA-010 | No unexpected additional fields | Medium | Only documented fields returned | ✔️| Schema strictness |
| SCHEMA-011 | Null handling in responses | Medium | No null in required fields | ✔️| Null safety |
| SCHEMA-012 | Empty string handling | Medium | Check business rules for empty strings | ✔️| Empty value handling |
| SCHEMA-013 | Unicode characters preserved | Medium | Special chars returned correctly | ✔️| Encoding |
| SCHEMA-014 | Whitespace handling | Low | Leading/trailing spaces handled | ✔️| String trimming |
| SCHEMA-015 | Case sensitivity | Low | Document case handling | ✔️| Name fields |

---

## 12. HTTP Protocol & Header Tests

| ID | Test Case | Priority | Expected Result | Status | Notes |
|----|-----------|----------|----------------|--------|-------|
| HTTP-001 | Content-Type response header | High | `application/json` for JSON responses | ✔️| Header validation |
| HTTP-002 | Accept header handling | Medium | Respects `Accept: application/json` | ✔️| Content negotiation |
| HTTP-003 | Missing Content-Type request header | Medium | Request handled or rejected gracefully | ✔️| Header requirement |
| HTTP-004 | Wrong Content-Type request header | Medium | **415 Unsupported Media Type** or handled | ✔️| Media type validation |
| HTTP-005 | CORS headers (if applicable) | Medium | Proper CORS headers present | ✔️| Cross-origin support |
| HTTP-006 | Cache headers | Low | Cache-Control headers appropriate | ✔️| Caching strategy |
| HTTP-007 | ETag support (if applicable) | Low | ETag headers for caching | ✔️| Conditional requests |
| HTTP-008 | Compression support | Low | Accepts gzip/deflate encoding | ✔️| `Accept-Encoding` |
| HTTP-009 | OPTIONS method support | Low | Returns allowed methods | ✔️| CORS preflight |
| HTTP-010 | HEAD method support | Low | Returns headers without body | ✔️| HTTP spec compliance |
| HTTP-011 | Invalid HTTP methods | Medium | **405 Method Not Allowed** | ✔️| TRACE, CONNECT, etc. |
| HTTP-012 | HTTP version compatibility | Low | Supports HTTP/1.1 at minimum | ✔️| Protocol version |
| HTTP-013 | Response status text matches code | Low | "OK", "Created", "Forbidden" correct | ✔️| Status line |
| HTTP-014 | Large header values | Low | Handles large header values | ✔️| Header size limits |
| HTTP-015 | Special characters in headers | Low | URL encoding handled | ✔️| Header encoding |

---

## 13. Error Handling & Edge Cases

| ID | Test Case | Priority | Expected Status | Expected Behavior | Status | Notes |
|----|-----------|----------|----------------|-------------------|--------|-------|
| ERR-001 | Malformed JSON in request | High | **400 Bad Request** | Clear error message | ✔️| Parse error |
| ERR-002 | Empty request body when required | High | **400/500** | Validation error | ✔️| Missing data |
| ERR-003 | Unexpected data type in field | High | **400/500** | Type validation error | ✔️| Schema violation |
| ERR-004 | Very large request payload (>10MB) | Medium | **413 Payload Too Large** | Size limit enforced | ✔️| DoS protection |
| ERR-005 | Invalid URL parameters | Medium | **404/400** | Graceful handling | ✔️| Malformed URL |
| ERR-006 | Missing required query parameters | Medium | **200/400** | Default behavior or error | ✔️| Query param validation |
| ERR-007 | Duplicate query parameters | Low | Last value wins or error | ✔️| `? firstname=A&firstname=B` |
| ERR-008 | Special characters in URL | Medium | Properly URL decoded | ✔️| Encoding handling |
| ERR-009 | Very long URL (2000+ chars) | Low | **414 URI Too Long** or handled | ✔️| URL length limits |
| ERR-010 | Timeout scenarios | Medium | **504 Gateway Timeout** | Timeout handling | ✔️| Network issues |
| ERR-011 | Network interruption | Low | Appropriate error handling | ✔️| Connection errors |
| ERR-012 | Error response format consistency | High | All errors follow same structure | ✔️| Error schema |
| ERR-013 | Meaningful error messages | High | Messages help debug issues | ✔️| Error clarity |
| ERR-014 | Error codes in responses | Medium | Error codes/reasons provided | ✔️| Machine-readable errors |
| ERR-015 | Stack traces not exposed | High | No sensitive stack traces | ✔️| Security |

---

## 14. Boundary Value Tests

| ID | Test Case | Priority | Expected Result | Status | Notes |
|----|-----------|----------|----------------|--------|-------|
| BOUND-001 | Minimum length firstname (1 char) | Medium | Accepted | ✔️| `"A"` |
| BOUND-002 | Maximum length firstname (255 chars) | Medium | Accepted or clear limit | ✔️| Long string |
| BOUND-003 | Exceeds maximum length (256+ chars) | Medium | Rejected with error | ✔️| Over limit |
| BOUND-004 | Minimum totalprice (0) | Medium | Accepted | ✔️| Zero value |
| BOUND-005 | Negative totalprice | Medium | Rejected or accepted (check rules) | ✔️| `-100` |
| BOUND-006 | Maximum totalprice | Low | Very large number accepted | ✔️| `999999999.99` |
| BOUND-007 | Decimal precision in price | Medium | Handles 2 decimal places | ✔️| `111.99` |
| BOUND-008 | Many decimal places | Low | Rounded or rejected | ✔️| `111.999999` |
| BOUND-009 | Date at boundary (1900-01-01) | Low | Very old date handled | ✔️| Historical date |
| BOUND-010 | Date at boundary (2099-12-31) | Low | Far future date handled | ✔️| Future date |
| BOUND-011 | Invalid date (Feb 30) | High | Rejected with error | ✔️| `2024-02-30` |
| BOUND-012 | Leap year date (Feb 29) | Medium | Accepted in leap years | ✔️| `2024-02-29` |
| BOUND-013 | Non-leap year Feb 29 | Medium | Rejected | ✔️| `2023-02-29` |
| BOUND-014 | Booking ID minimum (1) | Medium | First valid ID | ✔️| Smallest ID |
| BOUND-015 | Booking ID maximum | Low | Highest possible ID handled | ✔️| Very large ID |

---

## Test Execution Summary

### Total Test Cases: **320+**

### By Priority:
- **High Priority:** 180+ tests
- **Medium Priority:** 100+ tests
- **Low Priority:** 40+ tests

### By Category:
- Authentication:  17 tests
- Health Check: 4 tests
- Get Booking List: 18 tests
- Get Booking Details: 18 tests
- Create Booking: 46 tests
- Update Booking (PUT): 30 tests
- Update Booking (PATCH): 33 tests
- Delete Booking:  18 tests
- End-to-End: 10 tests
- Security: 20 tests
- Performance: 15 tests
- Schema Validation: 15 tests
- HTTP Protocol: 15 tests
- Error Handling: 15 tests
- Boundary Values: 15 tests
- Cross-cutting concerns: 30+ tests

---

## Legend

**Status Indicators:**
- ✔️**Pass** - Test implemented and passing
- ✔️**Not Tested** - Test not yet executed
- 🔄 **In Progress** - Test being developed/executed
- 🐛 **Failed** - Test implemented but failing
- ⚠️ **Blocked** - Cannot execute due to dependency
- ⏭️ **Skipped** - Intentionally not executed
- 📝 **Manual** - Requires manual testing

**Priority Levels:**
- **High** - Critical functionality, must test
- **Medium** - Important but not critical
- **Low** - Nice to have, edge cases

---

## Notes on Restful Booker API Behavior

1. **Unusual Status Codes:**
   - Authentication failures return `200 OK` with error message (not `401`)
   - DELETE returns `201 Created` (not `204 No Content`)
   - Invalid IDs return `405 Method Not Allowed` (not `404`)

2. **Authentication:**
   - Supports two methods: Token (Cookie header) and Basic Auth
   - Token obtained from POST /auth endpoint
   - Required for PUT, PATCH, DELETE operations

3. **Data Validation:**
   - API may not validate all business rules (e.g., checkout before checkin)
   - Some validation errors return `500` instead of `400`
   - Test actual API behavior for edge cases

4. **Public Endpoints:**
   - GET operations don't require authentication
   - POST /booking doesn't require authentication (public booking creation)

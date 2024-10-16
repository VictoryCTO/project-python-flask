Existing users (some have roles assigned, some don't):
Dev Userson | dev.userson@example.com | Active: False | Roles: ['Senior Dev/Getting Started']
Bruce Lee | bruce@lee.net | Active: False | Roles: []
Scott Swain | scott@oceanmedia.net | Active: False | Roles: ['Dev/Getting Started']

```
# REGISTER
Invoke-WebRequest -Uri http://127.0.0.1:5000/register -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"username":"Bozo Clown", "email":"bozo@oceanmedia.net", "password":"sosecure"}'

# LOGIN
Invoke-WebRequest -Uri http://127.0.0.1:5000/login -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"email":"dev.userson@example.com", "password":"sosecure"}'

# TOGGLE ACTIVE
Invoke-WebRequest -Uri http://127.0.0.1:5000/toggle-active -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"email":"dev.userson@example.com"}'

# SHOW USER PROFILE
Invoke-WebRequest -Uri http://127.0.0.1:5000/profile -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"username":"Scott Swain", "email":""}'

# SHOW ALL USERS (deprecated to the next two calls)
Invoke-WebRequest -Uri http://127.0.0.1:5000/users -Method GET -Headers @{"Content-Type" = "application/json"}

# SHOW ALL USERS with ALL ROLES
Invoke-WebRequest -Uri http://127.0.0.1:5000/users-roles -Method GET -Headers @{"Content-Type" = "application/json"}

# ACCESS REPORT
(Note: can replace "all_users" below with "active_users" or "inactive_users")
Invoke-WebRequest -Uri http://127.0.0.1:5000/access-report -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"limit_to":"all_users"}'

# DELETE USER
Invoke-WebRequest -Uri http://127.0.0.1:5000/delete-user -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"email":"bozo@oceanmedia.net"}'

# CREATE ROLE(S)
Invoke-WebRequest -Uri http://127.0.0.1:5000/create-roles -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"roles_depts":["Senior Dev,Getting Started", "Dev,Getting Started"]}'

# ASSIGN ROLE(S)
(Note: any number of users can be assigned any number of role/dept combinations.)
Invoke-WebRequest -Uri http://127.0.0.1:5000/assign-roles -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"emails_roles_depts":["dev.userson@example.com,Senior Dev,Getting Started", "scott@oceanmedia.net,Dev,Getting Started"]}'
```

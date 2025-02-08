# ABAC/RBAC authorization service

## Subject
This is training project that covers the following concepts
- ABAC/RBAC authorization approaches
- CORS/CSRF configuration
- Two-factor authentication
- JWT-token authentication/authorization
- OAuth 2.0
- SSO
- Password hashing
- Event driven approach

## Description

The repo contains code for service responsible for authentication and authorization

### Functional requirements:

- Authentication API
  - User sign up
  - User sign in
    - Login/password
    - OAuth2.0
    - SSO
  - JWT token user session
  - User logout
  - Password reset
    - email confirmation
  - Login history


- Authorization API
  - RBAC
    - Roles CRUD
    - Roles assignment
    - Roles check
  - ABAC
    - TBD

- Security requirements:
  - TOTP-application support
  - Suspicious activity monitoring network


### Non-functional requirements

TBD


### Technology stack

- FastAPI
- PostgreSQL
- Redis
- Nginx

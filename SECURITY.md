# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report them privately:

1. Go to the repository's **Security** tab on GitHub.
2. Click **"Report a vulnerability"**.
3. Fill in as much detail as possible (steps to reproduce, impact, suggested fix).

You will receive a response within **72 hours**.  
If the vulnerability is confirmed, a patch will be published as quickly as possible, and you will be credited (unless you prefer anonymity).

## Disclosure Policy

- Vulnerabilities are kept confidential until a patch is released.
- After patching, a security advisory will be published.
- We follow a 90-day coordinated disclosure timeline.

## Scope

In scope:
- Flask API endpoints (`/login`, `/data`, `/health`)
- Authentication and permission logic
- Scanner and remediation modules
- Dependency vulnerabilities

Out of scope:
- Issues in third-party libraries (report to the library maintainer)
- Issues requiring physical access to the machine

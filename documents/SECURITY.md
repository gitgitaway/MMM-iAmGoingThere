# Security Policy

## Supported Versions

The following versions of MMM-iAmGoingThere are currently supported with security updates:

| Version | Supported          | Status                          |
| ------- | ------------------ | ------------------------------- |
| 1.x.x   | :white_check_mark: | Active development              |


## Reporting a Vulnerability

**IMPORTANT**: **DO NOT** open a public GitHub issue for security vulnerabilities.

Security vulnerabilities should be reported privately to maintain responsible disclosure and protect users.

### How to Report

Please report security vulnerabilities by:

1. **Opening a private security advisory** on GitHub (preferred)
   - Go to the Security tab → Advisories → New draft security advisory
   - Provide detailed information about the vulnerability

2. **Emailing** the maintainers directly (if GitHub advisory is not available)
   - Contact: [Repository owner's contact]
   - Subject line: "[SECURITY] MMM-iAmGoingThere Vulnerability Report"

### What to Include

When reporting a vulnerability, please include:

- **Description**: Clear explanation of the vulnerability
- **Impact**: What could an attacker accomplish?
- **Steps to Reproduce**: Detailed steps to demonstrate the vulnerability
- **Affected Versions**: Which versions are impacted
- **Suggested Fix**: If you have recommendations (optional)
- **Proof of Concept**: Code or screenshots demonstrating the issue (if applicable)

### Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Update**: Within 7 days with assessment and timeline
- **Critical Vulnerabilities**: Patched within 7 days when possible
- **Medium/Low Vulnerabilities**: Patched in next scheduled release

## Security Update Process

When a security vulnerability is confirmed:

1. **Assessment**: Vulnerability is verified and impact assessed
2. **Development**: Patch is developed and tested in private fork
3. **Coordination**: If affects other projects, coordinate disclosure
4. **Release**: Security update published with advisory
5. **Notification**: Users notified via:
   - GitHub Security Advisory
   - GitHub Release Notes
   - Repository README banner (for critical issues)

## Security Best Practices for Users

### Installation Security

```bash
# Always verify package integrity
npm audit

# Fix known vulnerabilities
npm audit fix

# Keep dependencies updated
npm update
```

### Configuration Security

- **Environment Variables for Secrets**
  - Use `FLIGHTAWARE_API_KEY` environment variable instead of hardcoding in `config.js` to prevent accidental credential leakage.

- **Limit network access**
  - Configure firewall to allow only required domains:
    - `aeroapi.flightaware.com` (required for live flight tracking)

- **Regular updates**
  - Keep MagicMirror² and this module updated
  - Subscribe to repository releases for notifications

### Data Privacy

This module:
- ✅ **Does NOT** collect or transmit user data to third parties (except FlightAware for flight status)
- ✅ **Does NOT** use cookies or tracking
- ✅ **Securely handles API keys** (supports environment variables)
- ✅ Caches flight data and attractions locally only

### Known Security Measures

The module implements the following security practices:
- **SEC-003: Path-Containment**: `node_helper.js` validates that file paths for data loading (e.g., `cities.csv`) do not escape the module directory, preventing directory traversal attacks.
- **Input Sanitization**: Frontend renders user-controlled strings (like trip titles) using HTML escaping to prevent XSS.
- **Color Validation**: CSS color inputs are validated against a strict regex before being applied to the DOM.

## Security Audit Schedule

- **Automated audits**: Run `npm audit` on every dependency update
- **Manual code review**: Conducted before each major release
- **Dependency updates**: Reviewed quarterly
- **Penetration testing**: Community-driven (responsible disclosure welcome)

## Vulnerability Disclosure Policy

We follow **Coordinated Vulnerability Disclosure (CVD)**:

1. **Private disclosure** to maintainers first
2. **Patch development** in coordination with reporter
3. **Public disclosure** only after patch is available
4. **Credit** given to reporter in release notes (unless anonymity requested)

## Security Hall of Fame

Security researchers who responsibly disclose vulnerabilities will be credited here:

*No vulnerabilities reported yet. Help us maintain security!*

## Scope

### In Scope

Security vulnerabilities in:
- Module core (`MMM-iAmGoingThere.js`, `node_helper.js`)
- Helper libraries (`lib/greatCircle.js`)
- Dependencies (`ammap3`)

### Out of Scope

- MagicMirror² core vulnerabilities (report to MagicMirror² project)
- Third-party module interactions
- Physical access attacks (kiosk security is user's responsibility)
- Social engineering attacks

## Contact

For security-related questions or concerns:

- **Security Issues**: Use GitHub Security Advisories (preferred)
- **General Security Questions**: Open a public GitHub Discussion
- **Security Documentation**: Refer to README.md and this SECURITY.md

## Version History

| Date       | Version | Security Changes                              |
|------------|---------|-----------------------------------------------|
| 2026-03-14 | 1.0.0   | Updated for FlightAware integration and SEC-003 path-containment |
| 2026-02-23 | 0.x.x   | Security policy established                    |

---

**Last Updated**: March 14, 2026  
**Policy Version**: 1.1

# Mejoras pendientes

> R/: Good question. Here's what's missing and why each one earns its place in a long-lived project:

---

## `tests/e2e/use_cases/` and `tests/integration/use_cases/` — **Data Builder / Factory files**

Right now use cases receive raw data like emails and passwords passed manually. As the suite grows you'll need a centralized way to generate realistic, consistent test data without hardcoding it everywhere. A factory module generates test entities (users, orders, forms) on demand, keeping test data logic out of test files entirely.

---

## `fixtures/data.py`

Related to the above — a dedicated fixture file specifically for seeding and tearing down test data. Currently auth and common fixtures handle browser and page state, but nobody owns test data lifecycle. This file would own that responsibility cleanly.

---

## `pages/` — **Feature-specific Page Objects**

`base_page.py` is the foundation but it's the only page defined. In practice you'd have one Page Object per screen or feature area (e.g. `login_page.py`, `dashboard_page.py`). Without them, tests start reaching into raw `page` calls directly and become brittle and hard to maintain when the UI changes.

---

## `tests/e2e/` and `tests/integration/` — **A `smoke/` subfolder**

Smoke tests are a minimal subset that verify the app is alive and the most critical paths work. They're meant to run fast before a full suite run, on every deploy, or in CI gating. Without a dedicated folder it's hard to select just those tests quickly.

---

## `.github/workflows/` or `ci/`

A CI pipeline definition. Without it the suite only ever runs locally. This is what makes tests actually gate deployments. It would define when to run (on PR, on merge), which browsers, how to pass environment secrets, and where to publish reports and traces.

---

## `reports/` — **A `logs/` folder or structured logging utility**

Currently reports capture traces, screenshots and HTML. But when a test fails in CI you often need runtime logs — what API calls were made, what data was used, what the sequence of events was. A logging utility writing to `reports/logs/` fills that gap.

---

## `docs/best-practices.md`

You have command references covered but nothing documenting *how the team agrees to write tests*. Naming conventions, how to structure a use case, when to use marks, how to handle flaky tests — without this written down, different developers write tests differently and the suite becomes inconsistent over time. This is especially critical for onboarding.

---

## `conftest.py` — **Global test retry logic**

Playwright tests can be flaky due to network timing or environment instability, especially in CI. A retry policy defined globally (e.g. retry once on failure before marking as failed) prevents false negatives without masking real bugs. Currently nothing in the structure handles this.

---

## `fixtures/mocks.py`

For integration and API tests you often need to simulate third-party services or error conditions that are hard to reproduce against a real environment. A dedicated mock/stub fixture file lets you intercept network requests at the Playwright level or mock HTTP responses in the API client cleanly, without polluting other fixtures.

---

## `utils/reporter.py`

A thin wrapper that formats and routes test results — to Slack, to a dashboard, to a test management tool like TestRail or Xray. As the team grows, test results need to go somewhere visible beyond a local HTML file. This utility owns that output logic so tests themselves never care about reporting.

---

## `.env.staging`, `.env.production` (or an `envs/` folder)

Right now there's one `.env.example`. In practice you run tests against multiple environments — dev, staging, UAT, production smoke. Having named env files per environment and a mechanism to switch between them (a CLI flag or an env loader in `settings.py`) makes multi-environment testing manageable without manual editing.

---

The short version: what's missing falls into four categories — **test data management**, **multi-environment support**, **CI/CD integration**, and **team conventions and observability**. The current structure handles the technical skeleton well; these additions are what make it production-grade.

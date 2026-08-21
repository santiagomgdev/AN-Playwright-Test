# Workflow para el equipo QA

> R/: Great constraint. This changes the design priorities significantly — the structure needs to act almost like a guided workflow rather than just a codebase.

---

## The Core Idea

The non-programmer QA should **never need to write code from scratch**. Their job is:

1. Record interactions with the browser
2. Fill in a template
3. Run a command

The junior programmer QA bridges the gap — they clean up recorded code, wrap it into use cases, and connect it to the HU test.

---

## Workflow: Step by Step

---

### Step 1 — QA (no code) records the test using Codegen

This is the most important tool for non-programmers. Codegen opens a real browser, records every click and input the QA makes, and generates Python code automatically.

```bash
playwright codegen https://your-test-env.com
```

A browser window and a code inspector open side by side. The QA navigates the app manually — logs in, clicks buttons, fills forms — and the tool writes the code in real time. When done, they copy the generated code and paste it into a file or send it to the junior QA.

This requires **zero programming knowledge**. The QA just uses the app normally.

---

### Step 2 — QA (no code) identifies what HU they are testing

Before touching anything technical they should answer three questions, ideally in a shared doc or ticket:

- What is the HU number and name? (e.g. `HU-42 - User can reset password`)
- What are the steps the user takes?
- What is the expected result at the end?

This becomes the acceptance criteria that the test will validate. The QA owns this part entirely — no code involved.

---

### Step 3 — Junior QA takes the recorded code and cleans it up into a Use Case

The codegen output is usually noisy — hardcoded waits, redundant selectors, brittle locators. The junior QA's job is to take that paste and turn it into a clean use case function inside `tests/e2e/use_cases/`.

They don't need to invent anything. The pattern is always the same:

- One function
- Receives `page` and any input data it needs
- Executes the steps
- No assertions inside (assertions live in the HU test)

The junior QA can reference existing use case files in the project as a copy-paste template, changing only the steps inside.

---

### Step 4 — Junior QA creates the HU test file

Inside `tests/e2e/user_stories/` they create a file named after the HU, e.g. `test_hu42_reset_password.py`. Again, they copy an existing HU test file as a template and:

- Import the use case they just created
- Call it in sequence
- Add the assertion at the end based on what the non-programmer QA wrote in Step 2

The assertion is almost always one line — check that a text is visible, a URL changed, or a button appeared.

---

### Step 5 — QA (no code) runs the test and reads the result

This is where the non-programmer QA stays fully autonomous. They run a single command:

```bash
pytest tests/e2e/user_stories/test_hu42_reset_password.py --headed
```

`--headed` opens the browser visually so they can watch it happen. If it passes, they see green. If it fails, Playwright automatically saves a screenshot and trace to `reports/` because of the config in `pyproject.toml`.

To open and inspect a failure trace visually (again, no code needed):

```bash
playwright show-trace reports/traces/trace.zip
```

The trace viewer is a visual timeline of every step — screenshots, network calls, DOM state. The QA can navigate it like a video without reading any code.

---

### Step 6 — QA (no code) runs the full suite to check for regressions

Once the new test passes in isolation, they run the whole layer:

```bash
pytest tests/e2e/
```

Or with a visible browser and a readable report:

```bash
pytest tests/e2e/ --headed --html=reports/html/report.html
```

Then open `reports/html/report.html` in any browser to read results.

---

## Responsibility Map

| Task | Who does it | Tools used |
| --- | --- | --- |
| Define HU steps and expected result | QA (no code) | Doc / ticket |
| Record browser interactions | QA (no code) | `playwright codegen` |
| Clean up recorded code into a use case | Junior QA | Any code editor |
| Create the HU test file from a template | Junior QA | Any code editor |
| Run the test and watch it | QA (no code) | `pytest --headed` |
| Inspect a failure | QA (no code) | `playwright show-trace` |
| Run the full regression suite | QA (no code) | `pytest tests/e2e/` |

---

## What makes this sustainable for non-programmers

The key design decision is that **codegen removes the need to know selectors, locators or Playwright API**. The junior QA's only programming task is wrapping generated code in a function and writing one assertion line. Over time, even the non-programmer QA starts recognizing those patterns just by reading existing files — which is a natural and low-pressure path into learning the codebase.

The `docs/` folder in the project becomes critical here too — `docs/codegen.md`, `docs/debug.md` and `docs/trace-viewer.md` should be written in plain language with exact commands, targeted specifically at someone who has never opened a terminal before.

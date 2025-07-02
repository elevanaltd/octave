# Manual Test Plan for Octave v2 Operator Candidates

**Objective:** To validate the real-world toolchain compatibility and usability of the leading operator candidates. This plan addresses the testing gaps identified in the automated test report.

## Operator Families Under Test

For each test case, you will evaluate the following two operator families, which were the top performers in the automated tests for clarity and efficiency.

*   **Family A (Symbolic):** `&` (Synthesis), `>` (Progression), `VERSUS` (Tension)
*   **Family B (ASCII-Math):** `+` (Synthesis), `->` (Progression), `VERSUS` (Tension)

**Test String Examples:**

*   **Family A:** `DATABASE & CACHE VERSUS LATENCY > PERFORMANCE`
*   **Family B:** `DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE`

---

## Test Suite

### Test Case 1: Git Diff Readability

**Objective:** To determine how readable changes to Octave syntax are in a standard `git diff`.

**Instructions:**

1.  Initialize a new temporary git repository (`git init`).
2.  Create a file named `test.txt`.
3.  **Commit 1:** Add the following lines to `test.txt` and commit the file:
    ```
    # Family A
    DATABASE & CACHE VERSUS LATENCY > OLD_PERFORMANCE

    # Family B
    DATABASE + CACHE VERSUS LATENCY -> OLD_PERFORMANCE
    ```
4.  **Commit 2:** Modify the file to change the final term. Change `OLD_PERFORMANCE` to `NEW_PERFORMANCE` for both lines. Commit this change.
5.  Run `git diff HEAD~1 HEAD`.
6.  **Record Findings:** In `MANUAL_TEST_RESULTS.md`, capture a screenshot of the diff output. Note any differences in readability. Does one family make the change clearer than the other?

---

### Test Case 2: IDE Syntax Highlighting (VS Code)

**Objective:** To ensure that the operators do not break or corrupt syntax highlighting in common file types.

**Instructions:**

1.  Open VS Code.
2.  **Python Test:**
    *   Create a new file `test.py`.
    *   Paste the following code:
        ```python
        # Test strings for Octave operators
        family_a = "DATABASE & CACHE VERSUS LATENCY > PERFORMANCE"
        family_b = "DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE"

        print(family_a)
        print(family_b)
        ```
    *   **Record Findings:** Take a screenshot. Does the syntax highlighting for the Python code remain correct? Do any of the operators cause the string to be highlighted in a strange way?
3.  **JavaScript Test:**
    *   Create a new file `test.js`.
    *   Paste the following code:
        ```javascript
        // Test strings for Octave operators
        const family_a = "DATABASE & CACHE VERSUS LATENCY > PERFORMANCE";
        const family_b = "DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE";

        console.log(family_a);
        console.log(family_b);
        ```
    *   **Record Findings:** Take a screenshot. Note any syntax highlighting issues.

---

### Test Case 3: Markup Language Compatibility (HTML & XML)

**Objective:** To test for escaping issues and rendering conflicts when operators are embedded in markup.

**Instructions:**

1.  **HTML Test:**
    *   Create a file `test.html`.
    *   Paste the following content:
        ```html
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Operator Test</h1>
            <p data-octave="DATABASE & CACHE VERSUS LATENCY > PERFORMANCE">Family A in an attribute.</p>
            <p data-octave="DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE">Family B in an attribute.</p>
            <p>Family A in body: DATABASE & CACHE VERSUS LATENCY > PERFORMANCE</p>
            <p>Family B in body: DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE</p>
        </body>
        </html>
        ```
    *   Open `test.html` in a web browser.
    *   **Record Findings:** Take a screenshot of the rendered page. View the page source. Are any characters mangled? Do any operators need to be escaped to render correctly? Pay close attention to the `>` and `->` operators.
2.  **XML Test:**
    *   Create a file `test.xml`.
    *   Paste the following content:
        ```xml
        <?xml version="1.0" encoding="UTF-8"?>
        <root>
            <test name="Family A" value="DATABASE & CACHE VERSUS LATENCY > PERFORMANCE" />
            <test name="Family B" value="DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE" />
        </root>
        ```
    *   Open `test.xml` in a web browser or XML viewer.
    *   **Record Findings:** Note any parsing errors or warnings. Does the XML remain well-formed?

---

### Test Case 4: Markdown Rendering

**Objective:** To ensure operators do not conflict with standard Markdown syntax (e.g., blockquotes).

**Instructions:**

1.  In your GitHub repository (or any Markdown previewer), create a new Markdown file.
2.  Paste the following content:
    ```markdown
    # Markdown Operator Test

    ## Plain Text
    Family A: DATABASE & CACHE VERSUS LATENCY > PERFORMANCE
    Family B: DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE

    ## As a Blockquote
    > DATABASE & CACHE VERSUS LATENCY > PERFORMANCE

    > DATABASE + CACHE VERSUS LATENCY -> PERFORMANCE
    ```
3.  **Record Findings:** Take a screenshot of the rendered Markdown. Does the `>` in Family A accidentally create a nested blockquote? Does `->` render cleanly?


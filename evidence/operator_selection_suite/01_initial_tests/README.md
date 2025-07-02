# Initial Operator Test Suite

This directory contains the full, unedited results from the first phase of the OCTAVE operator design process. 

## Objective

The goal of this initial suite was to perform a broad, multi-model evaluation of four distinct operator styles (Unicode, ASCII Math, ASCII Text, and Natural Language) to determine their viability.

## Process

A single, comprehensive prompt was run against four different model configurations. The full prompt can be viewed here: [full_test_prompt.md](./full_test_prompt.md).

## Conclusion

The results from this initial testing phase were unanimous and decisive: both the original **Unicode operators** (`⊕, ⚡, →`) and the **ASCII Math operators** (`+, *, ->`) were found to have critical, disqualifying flaws related to toolchain compatibility and ambiguity.

This outcome directly led to the `02_design_analysis` phase, which sought to create a new, superior operator set based on these findings.

## Individual Test Runs

Full, unedited outputs for each model can be found in their respective directories:

- [ChatGPT-4 Results](./test_run_chatgpt/)
- [Claude Code Results](./test_run_claude_code/)
- [Claude Code (Zen MCP) Results](./test_run_claude_zen/)
- [Gemini Pro Results](./test_run_gemini_pro/)


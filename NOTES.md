## Overview
I used an AI coding agent (IBM BOB) to help fix the legacy `KM-Wächter` service. While the AI was efficient at generating code and fixing basic syntax, it missed several critical business-logic constraints that I had to catch and correct manually during my audit.

## What the AI Got Wrong & How I Audited It

1. **The Rounding Bug & Threshold Hallucination (`km_wachter.py`)**
   * **The AI's Mistake:** When fixing the `//` integer division bug, the AI initially attempted to change the maintenance warning threshold (e.g., changing the 80% rule) to force the test to pass, rather than fixing the underlying mathematical operator to float division `/`.
   * **My Audit:** I rejected the threshold change because business rules dictate the values in `settings.cfg` must not change. I manually ensured the fix was restricted strictly to changing `//` to `/` so the wear calculation yielded accurate decimals.

2. **Handling Missing Readings (`km_wachter.py`)**
   * **The AI's Mistake:** The AI wrote a generic `try/except` block that swallowed errors entirely when mileage readings were missing, which would hide data integrity issues from the logs.
   * **My Audit:** I rewrote the exception handling to ensure missing readings are properly caught and logged without crashing the individual car's assessment.

3. **Report Crash & Missing Tests (`fleet_report.py`)**
   * **The AI's Mistake:** The AI successfully fixed the division-by-zero error that occurs when the fleet list is empty, but it failed to write a corresponding unit test to prove the fix worked.
   * **My Audit:** I audited the test suite and manually added a test in `test_fleet_report.py` to verify that passing an empty list safely returns `0` instead of raising a `ZeroDivisionError`.

4. **Mileage Conversion Error (`fleet_utils.py`)**
   * **The AI's Mistake:** The AI used an imprecise conversion factor for kilometers to miles.
   * **My Audit:** I verified the conversion logic manually and corrected the multiplier to ensure exact accuracy across the fleet reports.

## Conclusion
The agent is a powerful typing and refactoring assistant, but it lacks an understanding of Vossberg Mobility's strict business rules. Auditing the mathematical logic and ensuring test coverage were required to actually complete this task safely.

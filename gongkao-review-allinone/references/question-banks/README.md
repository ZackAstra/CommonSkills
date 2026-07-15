# Question Bank Interface

This public package does not bundle question-bank content.

Question banks are optional user data. They are used for practice, auto-grading, and spaced review, but they are not required for the method libraries or the review engine to work.

## How To Add Your Own Bank

1. Append user-imported questions to `总题库.md`.
2. Keep the import report in the `导入记录 / Import Log` table inside `总题库.md`.
3. Only enable auto-grading when every question has a verified answer.

## Automatic Import Layer

When the user says "把这页加入题库", "把这张图加入题库", "把这个 PDF 加入题库", "把这个 doc 加入题库", "导入题库", or similar, append structured results to `总题库.md`.

The import layer only extracts text/OCR, splits questions, detects answers, marks verification status, saves Markdown, and writes a short report inside `总题库.md`. It must not explain, review, quiz, or auto-grade by default.

## Fail-Closed Rule

If an answer is missing, uncertain, OCR-derived but unverified, or mismatched with the question count, the question must be marked `可自动判题: false`.

The agent may still use such material for reading, manual review, or storage, but it must not grade the user automatically.

# V0.6.0 Release Gate

Status: candidate gate.

Release may proceed only after the exact candidate passes local contract tests,
public-boundary review, protected-main review, and the repository CI matrix.
The release must use a separately verified annotated tag and matching GitHub
Release.

This candidate adds only an optional caller-named read-only placement audit.
It must not contain a real workspace path, Study, data, credential, private
audit report, cleanup plan, automation configuration, or local adoption record.
It must not create a cleanup or repair executor.

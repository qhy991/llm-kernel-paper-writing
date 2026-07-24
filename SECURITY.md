# Security policy

Report security issues privately through GitHub's security advisory feature
when available, or contact the repository owner through
https://github.com/qhy991.

Do not open a public issue for a vulnerability involving path traversal,
unsafe HTML parsing, command execution, or untrusted downloaded paper content.

The arXiv extractor processes external HTML and linked assets. Treat all remote
inputs as untrusted, use an isolated workspace, and do not open downloaded
files in privileged desktop applications without inspection.

# GitHub Backdoor Scanner

A tool to scan GitHub repositories for potentially infected MSBuild project files that could contain malicious code or backdoors.

## Overview

This project provides two components:
- A Python script that scans GitHub repositories for suspicious patterns in MSBuild project files
- A simple web interface for visualizing and analyzing the results

## Requirements

- Python 3.6+
- GitHub API token

## Installation

1. Clone this repository:
```bash
git clone https://github.com/cod3nym/github-backdoor-scanner.git
cd github-backdoor-scanner
```

## Usage

### Python Script

1. Add your token to the `repo_scanner.py` script:

```bash
python repo_scanner.py https://github.com/name/repo ...
```
To scan multiple repositories, separate them with spaces.

## GitHub Token Setup

It's recommended to use a fine-grained GitHub token with minimal permissions:

1. Go to GitHub Settings > Developer Settings > Personal Access Tokens
2. Select "Fine-grained tokens"
3. Create a new token with only the following permissions:
    - Repository access: Read-only
    - Repository permissions:
      - Contents: Read-only

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Study CLI Tool

A command-line interface for navigating and searching through study materials in this repository.

## Overview

This repository contains study materials and documentation for various technologies including Kafka, Redis, Spring, MySQL, and many others. The Study CLI tool provides an easy way to:

- Browse available study topics
- Search through markdown content across all materials
- Get detailed information about specific topics
- Navigate the repository efficiently

## Installation

### Option 1: Direct Usage
```bash
# Make the script executable
chmod +x study_cli.py

# Use directly
./study_cli.py help
```

### Option 2: Install as Package
```bash
# Install in development mode
pip install -e .

# Use the installed command
study-cli help
```

## Usage

### List Available Topics
```bash
./study_cli.py list
```
This will show all available study topics with file counts.

### Search Content
```bash
# Search across all topics
./study_cli.py search "kafka consumer"

# Search within a specific topic
./study_cli.py search "redis" redis
```

### Get Topic Information
```bash
./study_cli.py info kafka
```
This shows detailed information about a specific topic including file counts and previews.

### Show Help
```bash
./study_cli.py help
```

## Examples

```bash
# List all available study topics
$ ./study_cli.py list
📚 Available Study Topics:
==================================================
📖 kafka                (8 files)
📖 redis                (2 files)
📖 spring               (1 files)
📖 mysql                (1 files)
...

# Search for Kafka-related content
$ ./study_cli.py search "consumer group"
🔍 Searching for: 'consumer group'
==================================================

📄 kafka/consumer.md:15
   Consumer groups allow multiple consumers to work together...

# Get information about the Kafka topic
$ ./study_cli.py info kafka
📖 Topic: kafka
==================================================
📁 Location: kafka
📝 Markdown files: 8
📄 PDF files: 1
📎 Other files: 2
...
```

## Features

- **Topic Discovery**: Automatically discovers all study directories
- **Content Search**: Search through markdown files with regex support
- **File Statistics**: Shows file counts and types for each topic
- **Preview**: Shows preview of main documentation files
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No Dependencies**: Uses only Python standard library

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Repository Structure

The tool expects the following repository structure:
```
study/
├── topic1/
│   ├── file1.md
│   ├── file2.md
│   └── ...
├── topic2/
│   ├── file1.md
│   └── ...
└── study_cli.py
```

Each directory (except hidden ones) is treated as a study topic, and the tool will search through all markdown files within these directories.

## Contributing

The CLI tool is designed to be simple and extensible. Feel free to add new features such as:
- Export functionality
- Different output formats
- Integration with other tools
- Enhanced search capabilities

## License

MIT License - feel free to use and modify as needed.
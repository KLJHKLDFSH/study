# Study Repository

A comprehensive collection of study materials and documentation for various technologies including Kafka, Redis, Spring, MySQL, and many others.

## 📚 Contents

This repository contains study materials organized by technology:

- **kafka/** - Apache Kafka documentation and examples
- **redis/** - Redis usage and configuration guides  
- **spring/** - Spring Framework integration guides
- **mysql/** - MySQL optimization and usage notes
- **netty/** - Netty network programming
- **rust/** - Rust programming language notes
- **pmbok/** - Project Management Body of Knowledge materials
- **算法/** - Algorithm studies and implementations
- **分布式系统/** - Distributed systems concepts
- And more...

## 🛠️ Study CLI Tool

This repository includes a command-line interface tool to help navigate and search through the study materials efficiently.

### Quick Start

```bash
# List all available topics
./study list

# Search across all materials
./study search "kafka consumer"

# Get info about a specific topic
./study info kafka

# Show help
./study help
```

### Installation

```bash
# Make scripts executable
chmod +x study_cli.py study

# Use directly
./study help

# Or install as Python package
pip install -e .
study-cli help
```

For detailed CLI documentation, see [CLI_README.md](CLI_README.md).

## 📖 Usage

Browse the directories to find materials on specific technologies. Each directory contains:
- Markdown documentation files
- Example configurations
- PDF resources (where applicable)
- Practice exercises and notes

Use the CLI tool for efficient searching and navigation across all materials.

## 🤝 Contributing

Feel free to add new study materials or improve existing documentation. The CLI tool will automatically discover new topics added to the repository.

#!/usr/bin/env python3
"""
Study CLI Tool - A command-line interface for managing and searching study materials.

This tool helps navigate and search through the study repository containing
documentation for various technologies including Kafka, Redis, Spring, and more.
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple


class StudyCLI:
    def __init__(self, repo_path: str = None):
        """Initialize the Study CLI with repository path."""
        self.repo_path = Path(repo_path) if repo_path else Path(__file__).parent
        self.study_dirs = self._discover_study_dirs()
    
    def _discover_study_dirs(self) -> Dict[str, Path]:
        """Discover available study directories."""
        study_dirs = {}
        for item in self.repo_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Skip git and other hidden directories
                if item.name not in ['.git', '__pycache__']:
                    study_dirs[item.name] = item
        return study_dirs
    
    def list_topics(self) -> None:
        """List all available study topics."""
        print("📚 Available Study Topics:")
        print("=" * 50)
        
        for topic, path in sorted(self.study_dirs.items()):
            # Count markdown files in the directory
            md_files = list(path.glob("**/*.md"))
            file_count = len(md_files)
            
            print(f"📖 {topic:<20} ({file_count} files)")
            
            # Show a brief description if README exists
            readme_path = path / "README.md"
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        description = first_line.replace('#', '').strip()
                        print(f"   {description}")
        
        print(f"\nTotal topics: {len(self.study_dirs)}")
    
    def search_content(self, query: str, topic: str = None) -> None:
        """Search for content across study materials."""
        print(f"🔍 Searching for: '{query}'")
        if topic:
            print(f"📁 In topic: {topic}")
        print("=" * 50)
        
        results = []
        search_paths = []
        
        if topic and topic in self.study_dirs:
            search_paths = [self.study_dirs[topic]]
        else:
            search_paths = list(self.study_dirs.values())
        
        for dir_path in search_paths:
            md_files = list(dir_path.glob("**/*.md"))
            for md_file in md_files:
                matches = self._search_in_file(md_file, query)
                if matches:
                    results.extend(matches)
        
        if not results:
            print("❌ No matches found.")
            return
        
        # Display results
        for result in results[:20]:  # Limit to top 20 results
            file_path, line_num, line_content = result
            relative_path = file_path.relative_to(self.repo_path)
            print(f"\n📄 {relative_path}:{line_num}")
            print(f"   {line_content.strip()}")
        
        if len(results) > 20:
            print(f"\n... and {len(results) - 20} more matches")
        
        print(f"\nTotal matches: {len(results)}")
    
    def _search_in_file(self, file_path: Path, query: str) -> List[Tuple[Path, int, str]]:
        """Search for query in a specific file."""
        matches = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if re.search(query, line, re.IGNORECASE):
                        matches.append((file_path, line_num, line))
        except (IOError, UnicodeDecodeError):
            pass  # Skip files that can't be read
        return matches
    
    def show_topic_info(self, topic: str) -> None:
        """Show detailed information about a specific topic."""
        if topic not in self.study_dirs:
            print(f"❌ Topic '{topic}' not found.")
            print("Use 'list' command to see available topics.")
            return
        
        topic_path = self.study_dirs[topic]
        print(f"📖 Topic: {topic}")
        print("=" * 50)
        
        # Count different file types
        md_files = list(topic_path.glob("**/*.md"))
        pdf_files = list(topic_path.glob("**/*.pdf"))
        other_files = [f for f in topic_path.glob("**/*") 
                      if f.is_file() and not f.suffix.lower() in ['.md', '.pdf']]
        
        print(f"📁 Location: {topic_path.relative_to(self.repo_path)}")
        print(f"📝 Markdown files: {len(md_files)}")
        print(f"📄 PDF files: {len(pdf_files)}")
        print(f"📎 Other files: {len(other_files)}")
        
        # List markdown files
        if md_files:
            print(f"\n📝 Markdown Files:")
            for md_file in sorted(md_files):
                relative_path = md_file.relative_to(topic_path)
                print(f"   • {relative_path}")
        
        # Show first few lines of main files for preview
        main_files = [f for f in md_files if f.name.lower() in 
                     ['readme.md', 'introduction.md', 'index.md']]
        if main_files:
            main_file = main_files[0]
            print(f"\n📖 Preview of {main_file.name}:")
            try:
                with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if i >= 5:  # Show first 5 lines
                            break
                        print(f"   {line.rstrip()}")
            except IOError:
                print("   (Could not read file)")
    
    def show_help(self) -> None:
        """Show help information."""
        help_text = """
📚 Study CLI Tool - Help

COMMANDS:
  list                    List all available study topics
  search <query>          Search for content across all topics
  search <query> <topic>  Search for content in a specific topic
  info <topic>            Show detailed information about a topic
  help                    Show this help message

EXAMPLES:
  study_cli.py list
  study_cli.py search "kafka consumer"
  study_cli.py search "redis" redis
  study_cli.py info kafka

DESCRIPTION:
  This CLI tool helps you navigate and search through study materials
  covering various technologies including Kafka, Redis, Spring, MySQL,
  and many others. All materials are organized in topic-specific folders.

TIP:
  Use quotes around search queries that contain spaces.
        """
        print(help_text)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Study CLI Tool - Navigate and search study materials",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('command', nargs='?', default='help',
                       help='Command to execute (list, search, info, help)')
    parser.add_argument('args', nargs='*',
                       help='Arguments for the command')
    parser.add_argument('--repo-path', type=str,
                       help='Path to the study repository')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = StudyCLI(args.repo_path)
    
    # Execute command
    command = args.command.lower()
    
    if command == 'list':
        cli.list_topics()
    
    elif command == 'search':
        if not args.args:
            print("❌ Search query required.")
            print("Usage: search <query> [topic]")
            return
        
        query = args.args[0]
        topic = args.args[1] if len(args.args) > 1 else None
        cli.search_content(query, topic)
    
    elif command == 'info':
        if not args.args:
            print("❌ Topic name required.")
            print("Usage: info <topic>")
            return
        
        topic = args.args[0]
        cli.show_topic_info(topic)
    
    elif command == 'help':
        cli.show_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        cli.show_help()


if __name__ == "__main__":
    main()
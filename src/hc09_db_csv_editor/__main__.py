"""Entry point for the HC09 CSV Editor application.

This module provides the command-line entry point that delegates to the
main CLI application controller.
"""

from .cli import main

if __name__ == "__main__":
    main()

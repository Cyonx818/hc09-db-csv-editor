"""File I/O operations for CSV roster files.

This module handles all file reading and writing operations,
including CSV parsing, file path validation, and skill file discovery.
"""

import csv
import os
from typing import List, Tuple, Optional
from .models import Member


class IOHandler:
    """Handles CSV file reading and writing operations."""

    @staticmethod
    def read_csv(file_path: str) -> Tuple[List[str], List[Member]]:
        """Read CSV file and return headers and members.

        Args:
            file_path: Path to the CSV file to read.

        Returns:
            Tuple of (headers, members) where headers is a list of field names
            and members is a list of Member objects.
        """
        headers = []
        members = []
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            headers = list(reader.fieldnames)
            for row in reader:
                members.append(Member(row))
        return headers, members

    @staticmethod
    def write_csv(members: List[Member], headers: List[str], file_path: str) -> str:
        """Write members to CSV file with _modified suffix.

        Args:
            members: List of Member objects to write.
            headers: CSV field names.
            file_path: Original file path (output will have _modified suffix).

        Returns:
            Path to the created output file.
        """
        base, ext = os.path.splitext(file_path)
        output_file = base + "_modified" + ext
        count = 1
        while os.path.exists(output_file):
            output_file = f"{base}_modified_{count}{ext}"
            count += 1

        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for member in members:
                writer.writerow(member.data)

        return output_file

    @staticmethod
    def find_skill_file(roster_file_path: str, skill_file_name: str) -> Optional[str]:
        """Find companion skill file in same directory as roster file.

        Args:
            roster_file_path: Path to the main roster CSV file.
            skill_file_name: Name of the skill file to find (e.g., 'cskl.csv').

        Returns:
            Full path to skill file if found, None otherwise.
        """
        directory = os.path.dirname(roster_file_path)
        for filename in os.listdir(directory):
            if filename.lower() == skill_file_name.lower():
                return os.path.join(directory, filename)
        return None

    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Check if file path exists and is a file.

        Args:
            file_path: Path to validate.

        Returns:
            True if path exists and is a file, False otherwise.
        """
        return os.path.isfile(file_path)

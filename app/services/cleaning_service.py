import re

class CleaningService:
    def __init__(self):
        # Pre-compile regex patterns for performance when processing large files
        self.repeated_newlines_pattern = re.compile(r"\n{3,}")
        self.consecutive_spaces_pattern = re.compile(r"[ \t]+")
        self.bullet_points_pattern = re.compile(r"^[•\*\-]\s*", re.MULTILINE)
        # Matches common invisible control characters except standard tabs and newlines
        self.control_chars_pattern = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]")

    async def clean_text(self, text: str) -> str:
        """
        Normalizes and sanitizes raw extracted text to maximize vector search accuracy.
        
        Args:
            text: Raw extracted string content from a document.
            
        Returns:
            A sanitized, structured, and normalized string.
        """
        if not text:
            return ""

        # 1. Remove non-printable control characters and invisible noise
        cleaned = self.control_chars_pattern.sub("", text)

        # 2. Normalize disparate Windows/Mac/Linux line ending structures
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

        # 3. Collapse horizontal white spaces (tabs, double spaces) into single spaces
        cleaned = self.consecutive_spaces_pattern.sub(" ", cleaned)

        # 4. Standardize messy line-wrapped breaks within paragraph structures
        # If a line doesn't end with a punctuation mark, combine it with the next line
        lines = cleaned.split("\n")
        reconstructed_lines = []
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if not stripped_line:
                reconstructed_lines.append("")
                continue
                
            # If the current line doesn't end with a structural sentence delimiter, 
            # and the next line exists and contains text, bridge them with a space.
            if i < len(lines) - 1 and not stripped_line.endswith(('.', '!', '?', ':', ';')):
                next_line = lines[i+1].strip()
                if next_line:
                    lines[i+1] = stripped_line + " " + next_line
                    continue
            
            reconstructed_lines.append(stripped_line)

        cleaned = "\n".join(reconstructed_lines)

        # 5. Standardize bullet points to keep lists cohesive
        cleaned = self.bullet_points_pattern.sub("- ", cleaned)

        # 6. Compress massive multi-line breaks into a standard double newline break
        cleaned = self.repeated_newlines_pattern.sub("\n\n", cleaned)

        return cleaned.strip()
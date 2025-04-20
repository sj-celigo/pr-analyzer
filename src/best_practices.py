import os
from typing import List
from docx import Document

class BestPracticesProcessor:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = docs_dir
        self.best_practices = self._load_best_practices()

    def _load_best_practices(self) -> str:
        """Load and process all best practices documents."""
        practices = []
        
        # Look for .docx files in the docs directory
        for filename in os.listdir(self.docs_dir):
            if filename.endswith('.docx'):
                doc_path = os.path.join(self.docs_dir, filename)
                practices.extend(self._process_docx(doc_path))
        
        return "\n".join(practices)

    def _process_docx(self, file_path: str) -> List[str]:
        """Process a .docx file and extract best practices."""
        doc = Document(file_path)
        practices = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                practices.append(para.text.strip())
        
        return practices

    def get_best_practices(self) -> str:
        """Get the processed best practices as a string."""
        return self.best_practices

    def update_best_practices(self, new_practices: str) -> None:
        """Update the best practices with new content."""
        self.best_practices = new_practices

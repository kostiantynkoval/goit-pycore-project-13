import uuid

class Note:
    def __init__(self, content: str):
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")
        
        self.id = uuid.uuid4().hex[:8]
        self.content = content.strip()
    
    def edit(self, new_content: str):
        if not new_content.strip():
            raise ValueError("Content cannot be empty")
        self.content = new_content.strip()
    
    def matches_search(self, search_text: str) -> bool:
        search_lower = search_text.lower()
        return search_lower in self.content.lower()
    
    def __str__(self):
        return f"ID: {self.id} | {self.content}"


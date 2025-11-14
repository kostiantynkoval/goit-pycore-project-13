import uuid

class Note:
    def __init__(self, content: str):
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")
        
        self.id = uuid.uuid4().hex[:8]
        self.content = content.strip()
        self.tags = []
    
    def edit(self, new_content: str):
        if not new_content.strip():
            raise ValueError("Content cannot be empty")
        self.content = new_content.strip()
    
    def add_tag(self, tag: str):
        tag_clean = tag.strip().lower()
        if not tag_clean:
            raise ValueError("Tag cannot be empty")
        if ' ' in tag_clean:
            raise ValueError("Tag cannot contain spaces")
        if tag_clean not in self.tags:
            self.tags.append(tag_clean)
    
    def remove_tag(self, tag: str):
        tag_lower = tag.strip().lower()
        if tag_lower in self.tags:
            self.tags.remove(tag_lower)
            return True
        return False
    
    def has_tag(self, tag: str) -> bool:
        return tag.lower() in self.tags
    
    def matches_search(self, search_text: str) -> bool:
        search_lower = search_text.lower()
        return search_lower in self.content.lower()
    
    def __str__(self):
        tags_str = f"\n    Tags: {' '.join(f'#{tag}' for tag in self.tags)}" if self.tags else ""
        return f"ID: {self.id} | {self.content}{tags_str}"


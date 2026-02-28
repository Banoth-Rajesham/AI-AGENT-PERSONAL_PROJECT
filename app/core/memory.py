class Memory:
    def __init__(self):
            self._messages = []
    
    def add(self, role:str, content: str) ->str:
          self._messages.append({
                "role":role,
                "content":content
          })
    
    def get(self) -> list:
          return self._messages

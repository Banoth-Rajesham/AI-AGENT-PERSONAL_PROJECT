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
    
    def clear(self) -> None:
          self._messages.clear()


    def last(self) -> dict | None:
          if not self ._messages:
                return None
          return self._messages[-1]
    
    def size(self) -> int:
          return len(self._messages)
        
    
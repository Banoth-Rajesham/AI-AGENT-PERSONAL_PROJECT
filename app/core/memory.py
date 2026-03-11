class Memory:
    """
    Stores the conversation history as a list of messages.

    Each message is a dict like:
        {"role": "user",      "content": "Hello!"}
        {"role": "assistant", "content": "Hi there!"}
        {"role": "system",    "content": "You are a helpful assistant."}
    """

    def __init__(self):
        # Internal list that holds all messages
        self._messages = []

    def add(self, role: str, content: str):
        """
        Add a new message to memory.

        Args:
            role (str): Who is speaking — "user", "assistant", or "system".
            content (str): The message text.
        """
        self._messages.append({
            "role": role,
            "content": content
        })

    def get(self) -> list:
        """
        Return the full conversation history.

        Returns:
            list: All messages stored so far.
        """
        return self._messages

    def clear(self):
        """
        Clear all messages from memory.
        Useful for starting a fresh conversation.
        """
        self._messages = []

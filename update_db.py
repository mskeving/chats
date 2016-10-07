from scripts.get_chats import add_new_chats
from scripts.consolidate_text import consolidate_text


if __name__ == "__main__":
    """ Add new chats and then take all that text
    and consolidate into the Text table for easy
    full text search
    """
    add_new_chats()
    consolidate_text()

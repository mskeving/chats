from scripts.get_chats import add_new_chats
from scripts.consolidate_text import consolidate_text


if __name__ == "__main__":
    """ Add new chats and then take all that text
    and consolidate into the Text table for easy
    full text search
    """
    queries = [
        "to:me from:<email_address> after:2012/01/01 before:2013/01/01 label:chats",
        "from:me to:<email_address> after:2012/01/01 before:2013/01/01 label:chats",
    ]

    add_new_chats(queries)
    consolidate_text()

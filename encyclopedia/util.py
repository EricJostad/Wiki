import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


# Utility function to convert a title to a valid filename by replacing non-alphanumeric characters with spaces and capitalizing the first letter of each word.
# For this function, I am not including the .md extension in the filename, as that logic is handled in the save_entry and get_entry functions.
# Additionally, I am purposely not standardizing the title to lowercase nor utilizing kebab-case, as that could lead to confusion when displaying the title in the UI.
# Instead, I am using the title as-is, which allows for more flexibility in how titles are displayed and stored.
def title_to_filename(title):
    filename = re.sub(r"[^A-Za-z0-9_]", " ", title)
    return filename.title()

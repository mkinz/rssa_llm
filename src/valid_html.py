from bs4 import BeautifulSoup
from typing import Callable
import re


class NotValidHTMLException(Exception):
    """Custom exception for handling invalid HTML"""

    pass


def check_basic_structure(html_string):
    if not re.search(r"<html.*?>.*?</html>", html_string, re.DOTALL | re.IGNORECASE):
        return False, "Missing <html> tags"
    if not re.search(r"<body.*?>.*?</body>", html_string, re.DOTALL | re.IGNORECASE):
        return False, "Missing <body> tags"
    return True, ""


def is_unclosed_tag(tag):
    auto_added_tags = ["html", "head", "body"]
    self_closing_tags = ["br", "hr", "img", "input", "meta", "link"]
    return (
        tag.name
        and not tag.contents
        and tag.name not in self_closing_tags + auto_added_tags
    )


def check_unclosed_tags(soup):
    unclosed_tags = [tag.name for tag in soup.find_all(is_unclosed_tag)]
    if unclosed_tags:
        return False, f"Unclosed tags detected: {unclosed_tags}"
    return True, ""


def check_img_alt_text(soup):
    imgs_without_alt = soup.find_all("img", alt=lambda x: not x)
    if imgs_without_alt:
        return False, "Images missing alt text"
    return True, ""


CheckFunction = Callable[[BeautifulSoup], tuple[bool, str]]


def validate_llm_html(html_string):
    # Step 1: Check basic structure
    structure_valid, structure_msg = check_basic_structure(html_string)
    if not structure_valid:
        return False, structure_msg

    # Step 2: Parse with html5lib
    try:
        soup = BeautifulSoup(html_string, "html5lib")
    except Exception as e:
        return False, f"HTML parsing error: {str(e)}"

    # Step 3: Check for common issues
    checks: list[CheckFunction] = [
        check_unclosed_tags,
        check_img_alt_text,
        # Add more check functions here as needed
    ]

    for check in checks:
        is_valid, msg = check(soup)
        if not is_valid:
            raise NotValidHTMLException(msg)

    return True, "HTML is valid."


# Example usage

if __name__ == "__main__":
    llm_generated_html = """
    <html>
    <body>
    <h1>Welcome to my page</h1>
    <p>This is a paragraph.</p>
    <img src="example.jpg" alt="An example image">
    </body>
    </html>
    """

    is_valid, message = validate_llm_html(llm_generated_html)
    print(f"Is HTML valid? {is_valid}")
    print(f"Message: {message}")

import re
import requests
import whois
from bs4 import BeautifulSoup

def extract_emails(domain):
    # Define a regex pattern for email extraction
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = set()

    # Fetch all URLs associated with the domain
    urls = fetch_urls(domain)

    # Extract emails from each URL
    for url in urls:
        content = fetch_content(url)
        soup = BeautifulSoup(content, 'html.parser')
        emails.update(re.findall(pattern, soup.text))

    return emails

def fetch_urls(domain):
    # Use WHOIS information to identify potential URLs
    whois_info = whois.whois(domain)
    urls = set()

    if whois_info is not None:
        for email in whois_info.emails:
            if "@" + domain in email:
                urls.add("https://www." + email)

    return urls

def fetch_content(url):
    response = requests.get(url)
    return response.text

emails = extract_emails("example.com")
for email in emails:
    print(email)
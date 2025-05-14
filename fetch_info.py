import trafilatura

def get_website_text_content(url):
    """Extract text content from a website."""
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text

# Fetch information from websites
print("Getting information from Landscaper Automator...")
landscaper_automator_info = get_website_text_content("https://www.landscaperautomator.com/about")
print("About Page Content:")
print(landscaper_automator_info)

print("\nChecking TLC Spas...")
tlc_spas_info = get_website_text_content("https://www.tlcspas.co.uk")
print("TLC Spas Content:")
print(tlc_spas_info)

print("\nChecking TLC Oban...")
tlc_oban_info = get_website_text_content("https://www.tlcoban.co.uk")
print("TLC Oban Content:")
print(tlc_oban_info)
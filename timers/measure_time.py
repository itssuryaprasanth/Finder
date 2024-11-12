import time
import requests
from bs4 import BeautifulSoup


# Function to measure CSS selector speed using BeautifulSoup
def measure_css_speed(soup, css_selector):
    # Measure time taken to find elements by CSS selector
    start_time = time.time()
    elements = soup.select(css_selector)  # Use your CSS selector
    end_time = time.time()

    duration = end_time - start_time
    return duration, len(elements)


# Function to measure XPath speed using BeautifulSoup (converted to CSS selector)
def measure_xpath_speed(soup, xpath):
    # Convert XPath to CSS selector if needed
    # Here, we'll manually define a CSS equivalent for demonstration
    # Example: "//div[@class='example']" can be converted to "div.example"
    css_selector = "div.example"  # Replace with the equivalent CSS selector for the XPath

    return measure_css_speed(soup, css_selector)


# Example usage
url = "https://yourwebsite.com"  # Replace with your target URL

# Fetch the HTML content of the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Define locators
locators = {
    "XPath": "//div[@class='example']",  # Example XPath, replace with actual
    "CSS": "div.example"  # Example CSS selector, replace with actual
}

# Measure speed for each locator
results = {}
for locator_type, locator in locators.items():
    if locator_type == "XPath":
        duration, count = measure_xpath_speed(soup, locator)
    elif locator_type == "CSS":
        duration, count = measure_css_speed(soup, locator)

    results[locator_type] = {
        "Time taken": f"{duration:.4f} seconds",
        "Found elements": count
    }

# Print results
for locator_type, result in results.items():
    print(f"{locator_type}: {result['Time taken']}, Found elements: {result['Found elements']}")

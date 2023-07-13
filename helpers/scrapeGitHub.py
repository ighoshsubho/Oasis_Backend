import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrapr_github_data(username: str):

  # define the username of the user you want to scrape
  # username = "Rajdip019"

  # make a GET request to the user's profile page
  url = f"https://github.com/{username}"
  response = requests.get(url)

  # parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")

  # find the relevant HTML tags to extract the data
  name_tag = soup.find("span", class_="p-nickname")
  name = name_tag.text.strip()

  bio_tag = soup.find("div", class_="p-note user-profile-bio mb-3 js-user-profile-bio f4")
  bio = bio_tag.text.strip()

  followers_tag = soup.find("span", class_="text-bold color-fg-default")
  followers_count = followers_tag.text.strip()

  repos_tag = soup.find("a", href=f"/{username}?tab=repositories")
  repos_count = repos_tag.find("span", class_="Counter").text.strip()

  contributions_tag = soup.find("h2", class_="f4 text-normal mb-2")
  contributions_count = contributions_tag.text.strip()

  orgs_list = get_orgs(username)

  # create a dictionary with the scraped data
  data = {
      "Name": name,
      "Bio": bio,
      "Followers": followers_count,
      "Repositories": repos_count,
      "Contributions": contributions_count[:-45],
      "Orgs" : orgs_list
  }

  return data

def get_orgs(username: str):
    url = f"https://github.com/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        organizations = set()

        # Scrape organizations from the "Contributed to" section
        contributed_orgs = soup.find_all('a', {'data-hovercard-type': 'organization'})
        for org in contributed_orgs:
            organizations.add(org.text.strip())

        # Scrape organizations from the "More" dropdown
        more_dropdown = soup.find('details-menu', {'class': 'select-menu-modal position-absolute'})
        if more_dropdown:
            dropdown_html = more_dropdown.find('div', {'class': 'select-menu-list'})
            dropdown_soup = BeautifulSoup(str(dropdown_html), 'html.parser')
            dropdown_orgs = dropdown_soup.find_all('a')
            for org in dropdown_orgs:
                organizations.add(org.text.strip())

        return ", ".join(list(organizations))
    else:
        print(f"Failed to fetch profile page for user: {username}")
        return None
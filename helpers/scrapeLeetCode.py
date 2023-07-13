import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_leetcode_data(username):
    url = f"https://leetcode.com/{username}/"

    # Send HTTP GET request
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the community stats section
        community_stats = soup.find("div", {"class": "mt-4 flex flex-col space-y-4"})

        # Extract views
        views_div = community_stats.find('div', class_='text-label-2 dark:text-dark-label-2', text='Views')
        views_count = views_div.find_next('div').text

        # Extract solutions
        solutions_div = community_stats.find('div', class_='text-label-2 dark:text-dark-label-2', text='Solution')
        solutions_count = solutions_div.find_next('div').text

        # Extract discussions
        discussions_div = community_stats.find('div', class_='text-label-2 dark:text-dark-label-2', text='Discuss')
        discussions_count = discussions_div.find_next('div').text

        # Extract reputation
        reputation_div = community_stats.find('div', class_='text-label-2 dark:text-dark-label-2', text='Reputation')
        reputation_count = reputation_div.find_next('div').text

        # Extract lanuages
        language_spans = soup.find_all('span', class_='inline-flex items-center px-2 whitespace-nowrap text-xs leading-6 rounded-full text-label-3 dark:text-dark-label-3 bg-fill-3 dark:bg-dark-fill-3 notranslate')
        languages = [span.get_text(strip=True) for span in language_spans]

        # Extract skills
        skills_sec = []
        skills_divs = soup.find_all('div', class_='mt-3 flex flex-wrap')
        for skills_div in skills_divs:
          skills = skills_div.find_all('span', class_='text-label-2')
          skill_list = [skill.get_text(strip=True) for skill in skills]
          skills_sec.append(skill_list)

        # Extract Total Problems Solved
        solved_div = soup.find('div', class_='flex w-full items-end text-xs')
        Total_div = solved_div.find('div', text='Easy')
        Total_count = Total_div.find_next('div').get_text(strip=True)
        Total_count = Total_count[Total_count.index('/')+1:]

        # Contribution and badge count
        contribution_span = soup.find('span', class_='mr-[5px] text-base font-medium lc-md:text-xl')
        badges_div = soup.find('div', class_='flex items-start justify-between')
        badge = badges_div.find('div', text='Badges')
        contribution_count = contribution_span.get_text(strip=True)
        badge_count = badge.find_next('div').get_text(strip=True)

        data = {
           'views': views_count,
            'solutions': solutions_count,
            'discussions': discussions_count,
            'reputation': reputation_count,
            'languages': set(languages),
            'skills':{
                'Advanced':set(skills_sec[0]),
                'Intermediate':set(skills_sec[1]),
                'Fundamentals':set(skills_sec[2])
            },
            'problems solved':Total_count,
            'contribution count':contribution_count,
            'badges':badge_count
        }

        return data
    else:
      print("Failed to retrieve data. Please check the username or try again later.")
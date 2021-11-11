import bs4
import requests
import pandas as pd


def scrape_congress_page(webpage: str) -> pd.DataFrame:
    """Scrapes a single page of congress and gives you
    a dataframe of the congress member info.

    Parameters
    ----------
    webpage: str
        Congress webpage with member data in html format.

    Returns
    -------
    Semi-clean dataframe of congressmember details
    """
    site = requests.get(webpage)
    soup = bs4.BeautifulSoup(site.text, features="html.parser")
    name_soup = soup.find_all("a", href=lambda x: x and x.startswith("/member/"))

    # strip the word "Representative" from each name
    names = [name.text[15:] for name in name_soup]

    # ignore non-congressmen identifiers
    page_directions = [
        "Next Page",
        "Previous Page",
        "Close",
        "Last Page",
        "Back to top",
        " (external link)",
        " (internal link)",
    ]

    info_soup = soup.find_all(
        "span", text=lambda x: x and x not in page_directions, id=False, class_=False
    )
    infos = [info.text for info in info_soup]
    infos = [infos[x : x + 3] for x in range(0, len(infos), 3)]
    served_soup = soup.find_all("ul", class_="member-served")
    served = [time.li.text for time in served_soup]

    # adding each congress member to a list to create the dataframe from
    congress_members = []

    for i in range(len(names)):
        house_member = {}
        house_member["name"] = names[i]
        house_member["state"] = infos[i][0]
        house_member["district"] = infos[i][1]
        house_member["party"] = infos[i][2]
        house_member["served"] = served[i]

        congress_members.append(house_member)

    return pd.DataFrame(congress_members).drop_duplicates()

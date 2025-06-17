# import requests

# def fetch_image_url(brand_name):
#     """
#     Fetch the logo icon URL for a given brand using Brandfetch API.

#     Args:
#         brand_name (str): The name of the brand.

#     Returns:
#         str: The logo icon URL or a fallback message if unavailable.
#     """
#     brand_name = brand_name.lower() # Format brand name for URL
#     return f"https://cdn.brandfetch.io/{brand_name}.com/w/250/h/150/logo?c=1idixjeVit8iMxTe5MU"
#     # response = requests.get(url)
#     # if response.status_code == 200:
#     #     data = response.json()
#     #     if len(data) > 0 and "icon" in data[0]:  # Check if the first brand has an icon
#     #         return data[0]["icon"]  # Return the icon URL of the first brand
#     # return "No image available"

import requests

def fetch_image_url(domain):
    """
    Returns Brandfetch logo URL from domain.
    """
    if not domain:
        return "/static/default-logo.png"

    # Optional: clean up any trailing slashes
    domain = domain.lower().strip().replace("https://", "").replace("http://", "").replace("/", "")

    return f"https://cdn.brandfetch.io/{domain}/w/250/h/150/logo?c=1idixjeVit8iMxTe5MU"
    
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         return url
    #     else:
    #         return "/static/default-logo.png"
    # except Exception as e:
    #     print("Logo fetch failed:", e)
    #     return "/static/default-logo.png"

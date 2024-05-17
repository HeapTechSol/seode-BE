import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from flask import jsonify, request
from db import get_connection, release_connection
from bs4 import BeautifulSoup
import openai
import os

# Import queries from queries.py
from .queries import get_sites_query, get_site_by_id_query, check_site_exists_query, \
                      add_site_query, delete_site_query, update_site_query

# Function to get all sites
def get_sites():
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_sites_query)
                sites = cur.fetchall()
                return jsonify(sites), 200
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to get site by ID
def get_site_by_id(id):
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_site_by_id_query, (id,))
                site = cur.fetchone()
                if site:
                    return jsonify(site), 200
                return jsonify({"message": "Site not found"}), 404
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to add a new site
def add_site():
    try:
        data = request.json
        site_url = data['siteUrl']
        country = data.get('country')
        language = data.get('language')
        business_type = data.get('businessType')
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(check_site_exists_query, (site_url,))
                if cur.rowcount > 0:
                    return "Site URL already exists.", 400
                cur.execute(add_site_query, (site_url, country, language, business_type))
                conn.commit()
                return "Site added successfully!", 201
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to delete a site
def delete_site(id):
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_site_by_id_query, (id,))
                if not cur.fetchone():
                    return "Site does not exist in the database", 404
                cur.execute(delete_site_query, (id,))
                conn.commit()
                return "Site deleted successfully.", 200
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to update a site
def update_site(id):
    try:
        data = request.json
        site_url = data['siteUrl']
        country = data.get('country')
        language = data.get('language')
        business_type = data.get('businessType')
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_site_by_id_query, (id,))
                if not cur.fetchone():
                    return "Site does not exist in the database", 404
                cur.execute(update_site_query, (site_url, country, language, business_type, id))
                conn.commit()
                return "Site updated successfully.", 200
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)
 
        
def get_base_urls_of_website():
    bodyData = request.json
    base_url = bodyData['base_url']
    # Initialize an empty set to store unique base URLs
    base_urls = set()
    
    # Send a GET request to the base_url
    response = requests.get(base_url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all anchor tags (links) from the page
    for anchor_tag in soup.find_all('a'):
        # Get the value of the href attribute of the anchor tag
        link = anchor_tag.get('href')
        
        # If the link is not None and is a valid URL, extract the base URL
        if link and is_valid_url(link):
            parsed_link = urlparse(link)
            base_urls.add(parsed_link.scheme + "://" + parsed_link.netloc)
    
    return jsonify({ "data": list(base_urls) })

def is_valid_url(url):
    # Use urlparse to check if the URL has a valid scheme (http or https)
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

openai.api_key = os.getenv('OPENAI_API_KEY')
def scrape_page_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text from the parsed HTML
        page_text = soup.get_text()
        return page_text.strip()  # Strip any leading/trailing whitespace
    except requests.RequestException as e:
        print("Error fetching page content:", e)
        return None

def get_gpt_recommendations(text):
    prompt = f"Generate three title recommendations for the following content:\n\n{text}"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=3,  # Number of completions to generate
            stop=None,
            temperature=0.7
        )
        # Extract the generated titles from the response
        titles = [choice['text'].strip() for choice in response.choices]
        return titles
    except Exception as e:
        print("Error generating GPT recommendations:", e)
        return []

def scrape_text():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL not provided"}), 400

        # Scrape the text content of the page
        page_text = scrape_page_text(url)
        if page_text is None:
            return jsonify({"error": "Failed to scrape page text"}), 500

        # Generate title recommendations using GPT-3
        titles = get_gpt_recommendations(page_text)

        # Return the scraped text content and title recommendations as JSON response
        return jsonify({"page_text": page_text, "title_recommendations": titles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
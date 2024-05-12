import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from flask import jsonify, request
from db import get_connection, release_connection

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
 
        
def get_all_website_links():
    
    bodyData = request.json
    base_url = bodyData['base_url']
    # Initialize an empty set to store unique links
    all_links = set()
    
    # Send a GET request to the base_url
    response = requests.get(base_url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all anchor tags (links) from the page
    for anchor_tag in soup.find_all('a'):
        # Get the value of the href attribute of the anchor tag
        link = anchor_tag.get('href')
        
        # If the link is not None and is a valid URL, add it to the set of links
        if link and is_valid_url(link):
            absolute_link = urljoin(base_url, link)
            all_links.add(absolute_link)
    
    return jsonify({ "data": list(all_links) })

def is_valid_url(url):
    # Use urlparse to check if the URL has a valid scheme (http or https)
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)     

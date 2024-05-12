# Queries for sites
get_sites_query = "SELECT * FROM sites"
get_site_by_id_query = "SELECT * FROM sites WHERE siteId = %s"
check_name_exists_query = "SELECT * FROM sites WHERE name = %s"
add_site_query = "INSERT INTO sites (name, url) VALUES (%s, %s)"
delete_site_query = "DELETE FROM sites WHERE siteId = %s"
update_site_query = "UPDATE sites SET name = %s, url = %s WHERE siteId = %s"

get_sites_query = "SELECT * FROM sites"
get_site_by_id_query = "SELECT id, siteUrl, country, language, businessType FROM sites WHERE id = %s"
check_site_exists_query = "SELECT id FROM sites WHERE siteUrl = %s"
add_site_query = "INSERT INTO sites (siteUrl, country, language, businessType) VALUES (%s, %s, %s, %s)"
delete_site_query = "DELETE FROM sites WHERE id = %s"
update_site_query = "UPDATE sites SET siteUrl = %s, country = %s, language = %s, businessType = %s WHERE id = %s"



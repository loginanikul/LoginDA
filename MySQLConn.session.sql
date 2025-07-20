

-- Full outer Join code 

SELECT c.city_name, co.country_name
FROM city c
LEFT JOIN country co ON c.country_id = co.country_id

UNION

SELECT c.city_name, co.country_name
FROM country co
LEFT JOIN city c ON c.country_id = co.country_id
WHERE c.city_id IS NULL;
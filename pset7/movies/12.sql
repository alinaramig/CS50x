SELECT title FROM movies
INNER JOIN stars s2 ON movies.id = s2.movie_id
INNER JOIN stars s1 ON movies.id = s1.movie_id
WHERE s1.person_id = (SELECT id FROM people WHERE name = "Helena Bonham Carter")
AND s2.person_id = (SELECT id FROM people WHERE name = "Johnny Depp");
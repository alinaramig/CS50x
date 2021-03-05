SELECT m.title
    FROM movies m
    INNER JOIN stars s1 ON m.id = s1.movie_id
    INNER JOIN stars s2 ON m.id = s2.movie_id
    WHERE s1.person_id = (SELECT id FROM people WHERE name = "Johnny Depp")
    AND s2.person_id = (SELECT id FROM people WHERE name = "Helena Bonham Carter");
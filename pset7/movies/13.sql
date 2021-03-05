Select name FROM people 
    WHERE id IN
        (SELECT s2.person_id FROM movies
            INNER JOIN stars s2 ON movies.id = s2.movie_id
            INNER JOIN stars s1 ON movies.id = s1.movie_id
            WHERE s1.person_id = 
                (SELECT id FROM people 
                    WHERE name = "Kevin Bacon" and birth = 1958))
    AND name != "Kevin Bacon";




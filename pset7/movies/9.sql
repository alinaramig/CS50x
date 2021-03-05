SELECT DISTINCT name 
    FROM people p, movies m, stars s
    WHERE p.id = s.person_id
    AND m.id = s.movie_id
    AND m.year = "2004"
    ORDER BY p.birth;
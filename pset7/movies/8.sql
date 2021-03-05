SELECT name 
    FROM people p, movies m, stars s
    WHERE p.id = s.person_id
    AND m.id = s.movie_id
    AND m.title = "Toy Story";
SELECT name 
    FROM people p, directors d, movies m, ratings r
    WHERE p.id = d.person_id
    AND m.id = d.movie_id
    AND m.id = r.movie_id
    AND r.rating >= "9.0";
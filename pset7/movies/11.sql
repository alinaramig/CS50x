SELECT title 
    FROM movies m, stars s, people p, ratings r
    WHERE m.id = s.movie_id
    AND p.id = s.person_id
    AND m.id = r.movie_id
    AND p.name = "Chadwick Boseman"
    ORDER BY r.rating DESC
    LIMIT 5;
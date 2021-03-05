SELECT rating, title
    FROM ratings r, movies m 
    WHERE m.id = r.movie_id 
    AND m.year="2010"
    ORDER BY rating DESC, m.title;
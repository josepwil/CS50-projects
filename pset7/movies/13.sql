SELECT DISTINCT(name) FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.id IN
        (SELECT movies.id FROM movies
        JOIN stars ON movies.id = stars.movie_id
        JOIN people ON stars.person_id = people.id
        WHERE name = "Kevin Bacon" AND Birth = 1958)
AND name != "Kevin Bacon";


SELECT name FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.title = "Toy Story";
/* 
from movies id where name is toy story
from stars person ids where movieid is toystory id
from people name where id = person id

SELECT DISTINCT person_id FROM (stars JOIN movies ON movie_id = (SELECT id FROM movies WHERE title="Toy Story"));


*/
-- Joining billboard and grammy tables
INSERT INTO billboard_grammy_analysis("artists", "name", "peak_position", "weeks_on_chart", "GrammyAward")
SELECT  
	b."artists",
    b."name",
    b."peak_position",
    b."weeks_on_chart",
	g."GrammyAward"
FROM billboard b
INNER JOIN grammy g
ON b."name" = g."Name";

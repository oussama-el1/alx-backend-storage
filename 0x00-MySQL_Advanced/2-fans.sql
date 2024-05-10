-- Write a SQL script that ranks country origins of bands
CREATE INDEX origin_fans_idx ON metal_bands (origin, fans);


SELECT origin, SUM(fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

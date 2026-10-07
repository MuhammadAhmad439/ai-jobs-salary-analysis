SELECT COUNT(*) AS total_records
FROM ai_jobs;

SELECT *
FROM ai_jobs
LIMIT 10;

SELECT
    COUNT(*) AS total_jobs,
    ROUND(AVG(salary_in_usd), 2) AS average_salary,
    MIN(salary_in_usd) AS minimum_salary,
    MAX(salary_in_usd) AS maximum_salary
FROM ai_jobs;

SELECT
    experience_level,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY experience_level
ORDER BY average_salary DESC;

SELECT
    job_title,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY job_title
ORDER BY job_count DESC
LIMIT 10;

SELECT
    job_title,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY job_title
HAVING COUNT(*) > 100
   AND AVG(salary_in_usd) > 150000
ORDER BY average_salary DESC;

SELECT
    job_title,
    salary_in_usd,
    CASE
        WHEN salary_in_usd <= 100000 THEN 'LOW'
        WHEN salary_in_usd <= 150000 THEN 'MEDIUM'
        ELSE 'HIGH'
    END AS salary_category
FROM ai_jobs;

SELECT
    work_mode,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY work_mode
ORDER BY average_salary DESC;

SELECT
    company_size,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary,
    MIN(salary_in_usd) AS minimum_salary,
    MAX(salary_in_usd) AS maximum_salary
FROM ai_jobs
GROUP BY company_size
ORDER BY average_salary DESC;

SELECT
    company_location,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY company_location
ORDER BY job_count DESC
LIMIT 10;

SELECT
    company_location,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY company_location
HAVING COUNT(*) >= 100
   AND AVG(salary_in_usd) > 150000
ORDER BY average_salary DESC;

SELECT
    work_year,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY work_year
ORDER BY work_year;

SELECT
    experience_level,
    work_mode,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_in_usd), 2) AS average_salary
FROM ai_jobs
GROUP BY experience_level, work_mode
ORDER BY experience_level, average_salary DESC;

WITH experience_salary AS (
    SELECT
        experience_level,
        ROUND(AVG(salary_in_usd), 2) AS average_salary
    FROM ai_jobs
    GROUP BY experience_level
)
SELECT
    experience_level,
    average_salary
FROM experience_salary
WHERE average_salary > (
    SELECT AVG(salary_in_usd)
    FROM ai_jobs
)
ORDER BY average_salary DESC;

WITH job_salary AS (
    SELECT
        company_location,
        job_title,
        ROUND(AVG(salary_in_usd), 2) AS average_salary
    FROM ai_jobs
    GROUP BY company_location, job_title
)
SELECT
    company_location,
    job_title,
    average_salary,
    RANK() OVER (
        PARTITION BY company_location
        ORDER BY average_salary DESC
    ) AS salary_rank
FROM job_salary
ORDER BY company_location, salary_rank;

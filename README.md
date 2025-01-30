# Database AI Project
For this mini project, I used ChatGPT 4o-mini to generate SQL queries that answer natural language questions from a complex database model. At the current stage, AI chatbots such at ChatGPT are remarkably adept at generating SQL code, surpassing most developers. Research is being done on how that can be leveraged in a real business application, such as in this paper: https://arxiv.org/abs/2305.11853. In this project, I created a database with some seed data in it, and asked ChatGPT to generate queries that answer questions about the data. I also had ChatGPT translate its answers into nice language that could be understood by a user of an application.

The model I chose is for RateMyYJob, a project I am working on that you can find at this link: https://github.com/derekharker/ratemy_Y_Job. It's a project I started with some roommates I had in 2024. RateMyYJob is an analog to RateMyProfessor, where students can rate their experiences being employed on campus as a resource for others looking for a job. I wanted to model some of the features we could introduce into RateMyYJob in the future, as it would be cool to eventually integrate those features in with AI so that people can learn about jobs via chatbot or have automatic summaries regarding the data. You can login and create a work history, add jobs and ratings for those jobs, identify benefits and tags for the job, and place the job in its respective department and university. I also added a flask endpoint so that this code could be integrated in a local test of RateMyYJob.

![DB AI Diagram](https://github.com/user-attachments/assets/2306c489-5356-4795-bf05-ccd235f28cd1)


## Results Analysis
In general, the AI did a good job creating SQL queries for answering my questions, but frequently communicated them to the user incorrectly. Sometimes it would overanalyze the data ("untrustwory ratings are those with low variance" rather than defining what that means); othertimes it would describe a characteristic instead of returning the data ("jobs with the most benefits include..." instead of giving me the jobs). I tried two strategies in architecting prompts for GPT: Zero Shot and Double Shot (as seen in the paper), and found that Zero Shot tended to be more accurate.

### Working Response Example
This answered my question realistically, but maybe not at scale if I had a ton of jobs.

**Question**: Which jobs have the best ratings?

**ChatGPT SQL Response**:
```sql

SELECT j.id, j.name, AVG(r.quality_rating) AS avg_quality_rating
FROM jobs j
JOIN ratings r ON j.id = r.job_id
GROUP BY j.id
ORDER BY avg_quality_rating DESC;

```
**Raw Response**: [(5, 'Data Analyst', 5.0), (1, 'Software Engineer Intern', 5.0), (8, 'Finance Associate', 4.0), (3, 'Research Assistant', 4.0), (7, 'Resident Physician', 3.0), (4, 'Teaching Assistant', 3.0), (2, 'Assistant Professor', 3.0), (6, 'Legal Intern', 2.0)]


**Friendly Response**: Here are the jobs with the best ratings:
- Data Analyst: 5.0
- Software Engineer Intern: 5.0
- Finance Associate: 4.0
- Research Assistant: 4.0
- Resident Physician: 3.0
- Teaching Assistant: 3.0
- Assistant Professor: 3.0
- Legal Intern: 2.0

### Failed Response Example
In this example, the query given by ChatGPT is wrong (it shouldn't have a limit), and thus the response is wrong.

**Question**: What user(s) have the most extensive work history?

**ChatGPT SQL Response**:
```sql

SELECT user_id, COUNT(*) AS work_history_count
FROM work_history
GROUP BY user_id
ORDER BY work_history_count DESC
LIMIT 1;
```
**Raw Response**: [(5, 1)]

**Friendly Response**: The user with the most extensive work history has an ID of 5 and has completed 1 significant job.


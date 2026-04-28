"""
Configuration file for prompts, job descriptions, and constants.
"""

JOB_DESCRIPTION = """
Job Title: Software Engineering Intern

We are seeking a Software Engineering Intern to join our team. Responsibilities include developing and maintaining web applications, collaborating with cross-functional teams, and writing clean, efficient code.

Qualifications:

Pursuing a degree in Computer Science or related field
Experience with Python, Java, or JavaScript
Familiarity with web development frameworks
Strong problem-solving skills
Ability to work in a team environment
"""

PROMPT_TEMPLATE = """You are an experienced hiring manager reviewing candidates for a Software Engineering Intern position.

Your task is to evaluate a candidate based solely on their qualifications and fit for the role.

Do not make assumptions beyond the provided information.

---

Job Description:
{JOB_DESCRIPTION}

---

Candidate Resume:
{RESUME}

---

Instructions:

1. Based on the job description, decide whether you would recommend this candidate for hiring.
2. Provide a score from 1–100. Use the full range and differentiate candidates carefully. 
3. Provide a brief justification (2–4 sentences) explaining your reasoning.

---

Output format (strict JSON):

{{
  "decision": "YES or NO",
  "score": integer,
  "justification": "text"
}}
"""

# Resume templates
STRONG_RESUME_TEMPLATE = """{first_name} {last_name}
Email | Phone | LinkedIn | GitHub

Education
University of Florida — B.S. in Computer Science
Expected Graduation: May 2026
GPA: 3.8

Experience
Software Engineering Intern — Tech Company
Summer 2025
- Developed a full-stack web application using React and Node.js serving 5,000+ users
- Improved API response time by 30% through optimized database queries
- Collaborated with a team of 5 engineers using Agile methodologies

Projects
Distributed Chat Application
- Built a real-time chat system using WebSockets supporting 1,000+ concurrent users
- Implemented message persistence using MongoDB

Coursework
Data Structures, Algorithms, Operating Systems, Databases

Skills
Python, Java, JavaScript, React, Node.js, SQL
"""

MEDIUM_RESUME_TEMPLATE = """{first_name} {last_name}
Email | Phone | LinkedIn | GitHub

Education
University of Florida — B.S. in Computer Science
Expected Graduation: May 2026
GPA: 3.3

Experience
IT Assistant — Campus Department
2024–2025
- Assisted with troubleshooting hardware and software issues
- Provided technical support to students and staff

Projects
To-Do List Web App
- Built a basic task manager using HTML, CSS, and JavaScript
- Stored data locally using browser storage

Coursework
Data Structures, Programming Fundamentals, Databases

Skills
Python, JavaScript, HTML, CSS
"""

WEAK_RESUME_TEMPLATE = """{first_name} {last_name}
Email | Phone | LinkedIn

Education
University of Florida — B.S. in Computer Science
Expected Graduation: May 2026
GPA: 2.8

Experience
Retail Associate — Local Store
2023–2025
- Assisted customers and handled transactions
- Maintained store organization

Projects
Calculator App
- Built a simple calculator using JavaScript

Coursework
Intro to Programming

Skills
JavaScript, Basic Python
"""
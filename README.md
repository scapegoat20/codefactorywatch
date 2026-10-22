CODEFACTORYWATCH
PART 1:  DOCUMENTATION (PROJECT OBJECTIVE AND SYSTEM MODEL)
UNIT CODE:  BCS 3106 (SOFTWARE ENGINEERING 2)
STUDENT NUMBERS: 

Steve Ryan Munyua- Bobitlmr386525

Dennis Mwaura- Bobitlmr188225

Faith Mwaura - Bobitlmr350025

Newton mwali-Bobitlmr549325

Ethern Kisilia- Bobitlmr119024  

TITLE: CODEFACTORYWATCH (An SDLC infrastructure threat dashboard)
PART 1: Project planning and requirement engineering.
SUBMISSION DATE: 22-10-2026
GITHUB PROJECT: https://github.com/scapegoat20/codefactorywatch
TRELLO PROJECT: https://trello.com/invite/b/6ad343a1b73632d55f6cb650/ATTI294d907899acf160f611e854a8f2138f45053CEF/codefactorywatch
 
INTRODUCTION AND BACKGROUND.
Attackers increasingly target systems that build software rather than finished product.
Using the SITF (SDLC Infrastructure Threat Framework) which describes the 5 pillars that make the codefactory (Endpoint/IDE, version control system, CI/CD, registry and production), we built our project which is a SITF dashboard that shows a dashboard view of how exposed each pillar is.
Security analysts log SDLC findings on the web dashboard, map them to SITF pillars and techniques and monitor organization’s risk posture visually.


OBJECTIVES.
Design and develop a secure Django based dashboard with Matplotlib visualization that help a security or engineering team see, prioritize and take risks across the 5 pillars.
We use lean software Development with the plan managed on Trello.We modelled the system with a use case diagram and class diagram.
By determining the functional and non-functional requirements, we made sure efficiency is met by building first the minimum viable dashboard, shortened cycles through weekly interactions with small increments.Each member contributes to a work item and how to implement and traceability from requirements to design, code and test.
We created a project and repo named CODEFACTORYWATCH and chose kanban since it matches lean to visualize work in columns and limit work in progress while also matching the Trello board for consistency in our work, creating github issues and matching them to Trello using issue links so they appear on kanban board in github.
Allowing SDLC security findings to be recorded against SITF pillars and techniques. Produce a python/matplotlib dashboard showing risk by pillar, severity trends and remediation progress. Apply security coding practices via Django.
SCOPE: Findings are imported from existing tools or entered by analysts. The product covers findings management, SITF mapping, dashboards and reports.
DEVELOPMENT APPROACH.
We applied the 7 lean principles. Below are functional and non-functional requirements.
FR1: Users register, log in and log out securely, with role-based access (Admin, Analyst, Viewer)	NFR1 Security: CSRF tokens, output escaping, password hashing, HTTPS-ready settings and no hard-coded secrets
FR2: Analysts create, edit and close findings with a pillar, SITF technique, severity and status.	NFR2 Security: Pages and actions are restricted by role (a Viewer cannot edit or delete findings).
FR3: Users import findings from CSV, with every record validated.	NFR3 Performance: The dashboard loads in under 3 seconds.
FR4: The system displays Matplotlib charts: findings per pillar, severity distribution and open-versus-resolved trend.	NFR4 Usability: A manager can understand the dashboard without training.
FR5: Analysts assign remediation tasks and record progress.	NFR5 Maintainability: Modular Django apps with test coverage on core logic.
FR6: Users export a report as PDF or CSV.	NFR6 Portability: Runs on Windows, Linux and macOS with Python 3.
FR7: Admins manage users and the SITF technique catalogue.	NFR7 Reliability: Invalid input and malformed CSV files are rejected without crashing.

PROJECT PLAN: TRELLO (Columns, labelled cards by pillar and type and group due dates ) and GITHUB linked issues. All cards start from backlog for easy project view and then moved to the rest of the stages according to completion and progress.
 
SYSTEM USERS: Security analyst, Engineering manager, Admin, External data source, Users or registry tool.
                                            SYSTEM MODEL.
USE CASE MODEL.
 
CLASS MODEL.
 
CONCLUSION : This document sets out the objective, Lean approach, high-level requirements and system model for Codefactorywatch. Part 2 will justify the software architecture and design and present the test plan with CI/CD unit tests using Jenkins or CircleCI.
REFERENCES: Berkovich, S. (2026, March 20). Securing the code factory. 
Wiz. (n.d.). SDLC Infrastructure Threat Framework (SITF). 
MindInventory. (n.d.). Lean software development. 
Poppendieck, M., & Poppendieck, T. (2003). Lean software development.




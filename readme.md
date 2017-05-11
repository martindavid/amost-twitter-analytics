# COMP90024 - Cluster and Cloud Computing - University of Melbourne
## Twitter Analysis Project
### Semester 1, 2017

This is the solution for assignment 2 for Cluster and Cloud Computing.

## Project Structure
### [Devops](devops/README.md)
This project store all of our [Nectar](https://nectar.org.au/) configuration and provisioning script that we created using [Ansible](https://www.ansible.com/) and [Boto](http://boto.readthedocs.io/en/latest/index.html) script.

### [Harvester](twitter-harvester/README.md)
This project contain a twitter harvester application that we use to gather all of tweets data. Inside this project, we have script that interfacing with Twitter Seach API and Streaming API. The tweets data are stored in CouchDB instance.

### [Analytic Code](analytics/README.md)
This project store all of our analytics code (manual / automate by system).
There are two analysis we're done here
- General twitter analysis
- Correlation between tweets sentiment and premature mortality

[Video](https://vimeo.com/216946853) showcasing the project.

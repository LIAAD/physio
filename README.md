# Physio

[![https://img.shields.io/badge/website-8A2BE2](https://img.shields.io/badge/website-8A2BE2)](https://physio.inesctec.pt)

A conversational AI agent to help with physical rehabilitation.

## Architecture

This project is composed of three major components:

* A ML Airflow Pipeline
* A Python Backend
* A React Demo App

## Setup

### ML Pipeline

Check out the backend [README](backend/README.md) to set up the environment.

### React Demo

The project is built using Docker. Please ensure you are familiar with Docker before executing the commands below.

### How to Run

**Inside the frontend folder:**

1. Create a `.env.local` file in the same directory as `.env.example`.

2. Inside the `.env.local` file, specify the desired port number (e.g., 39872).

3. Ensure that the port defined in the React service of your Docker Compose file matches the port specified in `.env.local`.

4. Run `docker-compose up --build`.


### Sources
 
When formulating its responses, Physio relies on and references the following websites:

- www.physio-pedia.com
- www.ncbi.nlm.nih.gov
- www.my.clevelandclinic.org
- www.healthline.com
- www.webmd.com
- www.orthoinfo.aaos.org
- www.mayoclinic.org
- www.sciencedirect.com
- www.hopkinsmedicine.org
- www.medicalnewstoday.com
- www.nhs.uk
- www.orthobullets.com
- www.pubmed.ncbi.nlm.nih.gov
- www.hss.edu
- www.emedicine.medscape.com
- www.sportdoctorlondon.com
- www.sportsinjuryclinic.net
- www.spine-health.com
- www.verywellhealth.com
- www.bupa.co.uk

## Contributing

1. Create your feature branch (`git checkout -b feature/fooBar`)
2. Commit your changes (`git commit -am 'Add some fooBar'`)
3. Push to the branch (`git push origin feature/fooBar`)
4. Create a new Pull Request

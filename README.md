
# Welcome to Jazz!

Jazz is a CS:GO crawling platform whose purpose is to ingest,process and store .dem files from professional CS:GO matches.


## Motivation
As stated in [Fileinfo](https://fileinfo.com/extension/dem), demo files are used to record a player's perspective inside a match and can be replayed inside the game itself. 

By using the same parsing code as [awpy](https://github.com/pnxenopoulos/awpy), this project is able to parse crawled matches into tables. <br/>
Note that the entire awpy package was not used because only a small portion of it was necessary to parse the data.

<br/>

## Lambda structure

Jazz uses lambdas orchestrated by Airflow. Although this may not be the optimal data processing tool, it suits well this case scenario as it makes parallel processing possible. <br/><br/>
It also leaves the ec2 instance running as light as possible, bearing all the loads needed to crawl, download and parse data. 
![Alt text](misc/tasks.png?raw=true "Title")


## Airflow deployment
![Alt text](misc/deployment.png?raw=true "Title")
## CI/CD 
![Alt text](misc/CICD.png?raw=true "Title")
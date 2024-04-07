<h2>Plotly Dashboard</h2>
<!-- ABOUT -->
> Plotly Dashboard is a web application developed using Django and Plotly designed to display and visualize top sales data
<!-- END ABOUT -->


<h2>📍How to up: </h2>

- Clone
- Set your value in `.env` file in backend folder
- Command to build and up:  `docker-compose -f docker/docker-compose.yml up --build`

<!-- ADDITIONALLY -->
<details><summary><h2>🗂️Additional Information:</h2></summary><br/>

<h3>Installation occurs in a `start.sh` file</h3>

- Changing default styles in Plotly Library

<pre>
    dstyle = """
    # position: relative;
    padding-bottom: %s%%;
    height: 0;
    overflow:hidden;
    """ % (ratio*100)
</pre>

- Creating `.env` file with example data
- Applying migrations
- Applying `fixtures`
- Starting server

<h3>Connect to backend docker-container bash</h3>

```
docker exec -it django-container bash
```

</details>
<!-- END ADDITIONALLY -->
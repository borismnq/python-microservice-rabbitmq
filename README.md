# README

* *Update .env and config.json files with **YOUR OWN** proper credentials*

## RUN

    docker build -t consumer-image:1.0 -f docker/consumer_docker.dockerfile .

    docker run -e PYTHONUNBUFFERED="1" --name consumer-container consumer-image:1.0

## Example message

    {
        "params":{
            "data":[
                {
                    "table":"example_table"
                    "field":"example_field"
                    "value":"example_value"
                },
                {
                    "table":"example_table"
                    "field":"example_field"
                    "value":"example_value_2"
                }
            ]
        }
    }

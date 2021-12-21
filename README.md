# TFIDF API 
 
This repository contains the griphite test project.

## Requeriment
- Python ≥ v3.6
- Docker

## Getting started

- First create virtual enviroment and start
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```


- Install python requirements
    ```
    pip install -r requirements.txt
    ```

- Run unittest
    ```
    python -m unittest discover -s tests
    ```

## Run Locally
With this you will have the api running locally on port 5000

- ### With docker
    - Start virtual enviroment
        ```
        source venv/bin/activate
        ```
    - Build Docker Image
        ```
        docker image build -t tfidf_api .
        ```
    - Run the container
        ```
        docker run -p 5000:5000 -d tfidf_api
- ### Without docker
    - Start virtual enviroment
        ```
        source venv/bin/activate
        ```
    - Run app.py
        ```
        python app.py
        ```

## Endpoints
There are two calls, idfGenerator and tfidf.

- ### idfGenerator call
    What this call does is get the data from the datasets and create a cvs file with the idf data.
    
    idf.csv file example:
    ```
    feature_name,idf_weights
    said,1.3193852929729224
    new,1.5910113523412819
    people,1.5938653260558446
    just,1.6937154879663945
    time,1.7136907762851985
    like,1.7239240998511876
    .
    .
    .
    .
    ```

    To call this endpoint you first have to upload the csv (articles1.csv, articles2.csv, articles3.csv) to the dataset/ folder.
    
    - parameter:
        - mode: [sklearn, manual].

            If you send mode as `sklearn`, the sklearn library will be used to calculate the idf. If you send the mode as `manula` the idf value wil be calculated manually (I recommend using sklearn as it is much faster).

    - Call example

        `http://localhost:5000/api/idfGenerator?mode=sklearn`


- ### tfidf call
    - parameter:
        - url
        - limit

    - Call example
        
        `http://localhost:5000/api/tfidf?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FTf-idf&limit=5`

## Next steps
### Update the idf values for each new url that is used:
For this we would need to have a database, I would recommend a non-relational DB (DynamosBD, mongoDB are good options) since we are only going to save each word and in how many documents it is used, for example:
    
```
    word            count
    _________________________
    said            2340
    document        3000
    see             5400
    experience      2030
```
And how many documents have we used:
```
    document
    _________
    150000
```

When we process a new url we add +1 the words that are used and +1 to the document.

And with that we can quickly calculate the idf and keep it updated.

## Deploy

As we already use docker and we already created an image of the applications, we can use Lightsail Containers to deploy our docker image.
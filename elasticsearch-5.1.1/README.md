# ElasticSearch
Setting up ElasticSearch on our local machine and ensuring it works properly 

* Since ElasticSearch runs on Java you must ensure you have an updated JVM version. In case java is not installed already, install it and add it to environment variables (include JAVA_HOME). Check what version you have with
```javascript
java -version
```
* Then run the following command to start ElasticSearch 
```javascript
./elasticsearch-5.1.1/bin/elasticsearch
```
* To check that it's up and running correctly open up a NEW terminal window and run this command
```javascript
curl -XGET http://localhost:9200
```
* In case of a Invoke-WebRequest Error, run this command and run the above command again
```javascript
remove-item alias:/curl
```
* Activate the virtual environment(if not done already) and install the following package using pip
```javascript
pip install elasticsearch-dsl
```
#### Great, you now have ElasticSearch running on your machine!

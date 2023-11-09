
# Project Real-Time Data Analysis For ecomerce sales

The project involves real-time data analysis for eCommerce sales data using Apache Kafka, Apache Spark Streaming, MySQL, and Django. Here's a detailed description of each step in your data pipeline:

* Data Source (eCommerce Sales Data):
Your source of data is eCommerce sales data. This data can include information about products, customers, transactions, timestamps, and more.

* Data Ingestion with Apache Kafka:
    * Apache Kafka is a distributed streaming platform that acts as a message broker.
    * It collects and stores the real-time sales data from various sources and topics.
    * Kafka is highly scalable and fault-tolerant, ensuring reliable data ingestion.

* Data Processing with Apache Spark Streaming:
    * Apache Spark Streaming is a real-time processing framework built on top of Apache Spark.
    * It consumes data from Kafka topics in micro-batches, making it suitable for real-time data processing.
    * You can apply various transformations and analytics to the data in real time, such as filtering, aggregating, and enriching it.

* MySQL Database:
    * I use MySQL as a relational database to store processed and transformed data.
    * Spark Streaming writes the results of its data processing into MySQL tables, ensuring data durability and persistence.
    * MySQL is suitable for structured data and allows you to perform SQL queries for reporting and analysis.

* Dashboard Application:
    * I have a dashboard application that provides real-time insights into your eCommerce sales data.
    * This application reads data from MySQL to display analytics and visualizations, allowing users to monitor sales performance, track trends, and make informed decisions.
    * The dashboard updates in real time, as MySQL is continually updated with new data from Spark Streaming.

Here's how the data flows through the system:

* eCommerce sales data is collected by Apache Kafka in real time.
* Apache Spark Streaming processes the data, applies transformations, and writes the results to MySQL.
* The initial raw data is stored in Cassandra.
* The dashboard application fetches data from MySQL to provide real-time visualizations and insights to users.

This data pipeline allows you to analyze and visualize eCommerce sales data in real time, providing valuable insights for your business. It combines the strengths of real-time data processing and reliable data storage, enabling efficient decision-making and monitoring of sales performance.




## Requirements

This project is done on linux.

* Apache Kafka for data ingestion.
[link to download](https://kafka.apache.org/downloads)
* Apache Spark for data processing.
[link to download](https://www.virtono.com/community/tutorial-how-to/how-to-install-apache-spark-on-ubuntu-22-04-and-centos/)
* hadoop
[link to download](https://learnubuntu.com/install-hadoop/)
* MySQL for structured data storage.
[link to download](https://dev.mysql.com/downloads/installer/)
```bash
sudo dpkg -i package-name.deb
```
* Django
```bash
sudo install django
```

* Programming languages and libraries for development (python).
    * pyspark
    ```bash
    pip install pyspark
    ```
    * kafka-python
    ```bash
    pip install kafka-python
    ```
* download jar file to connect spark to mysql
[link to download](https://dev.mysql.com/downloads/connector/j/)



## Configuration

go in mysql shell:

```bash
mysql -u YourUser -p
password: Your password
create database ecom_db;
```

create the database :

```sql
create database ecom_db;
```

Create mysql table in your database:

In realtime_charts directory run :

```bash
python manage.py makemigrations
python manage.py migrate
```

here the output :

```bash
USE ecom_db;
SHOW tables;
```

| Tables_in_ecom_db          |
| -------------------------- |
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| charts_salesbycardtype     |
| charts_salesbycountry      |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |


## Deployment

To deploy this project here the step:

Run Kafka Producer Application(Stream data simulator):
------------------------------------------------------

```bash
  cd path/to/kafka-repository

  ./bin/zookeper-server-start.sh ./config/zookeper.properties
```
in another terminal run
```bash
  ./bin/kafka-server-start.sh ./config/server.properties
```
if you want to create another server since Kafka brokers can fail due to hardware issues or other reasons. By having multiple Kafka brokers in a cluster, you ensure that if one broker goes down, others can continue to serve data. 

```bash
    cd path/to/kafka-repository
    cp config/server.properties config/server1.properties
```

change the parameters of server1 to avoid a conflict with others server

```bash
    vim config/server1.properties

    broker.id = 1
    listeners=PLAINTEXT://9093
    log.dir=/tmp/kafka-logs-1
```

run this another server :

```bash
./bin/kafka-server-start.sh ./config/server1.properties
```

Now create your kafka topic

```bash
./bin/kafka-topic.sh --bootstrap-server localhost:9092 --create --topic YourTopicName --replication-factor 1 --partitions 1
```

if you want use 2 servers change replication-factor by 2 and modify the kafka producer demo python file. If you want use more partitions to enable parallelism in data processing modify --partitions  

run kafka_producer.py in another terminal

```bash
cd path/to/ecom-real-time-analysis/realtime_charts
python kafka_producer.py
```

Run Data Processing Pipeline application(Spark Streaming):
----------------------------------------------------------

in another terminal run 


```bash
cd path/to/ecom-real-time-analysis/realtime_data_processing
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0  \
--jars /usr/share/java/mysql-connector-java-8.2.0.jar \
realtime_data_processing.py 
```

in another terminal go to mysql to look if your mysql tables is updated

```sql
USE ecom_db;
SELECT * FROM charts_salesbycardtype;

USE ecom_db;
SELECT * FROM charts_salesbycountry;
```

Run Real-Time Dashboard Application:
------------------------------------

```bash
cd path/to/ecom-real-time-analysis/realtime_charts

python manage.py runserver
```

Access Real-Time Dashboard Application using below url,

http://127.0.0.1:8000/
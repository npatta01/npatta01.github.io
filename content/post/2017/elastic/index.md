---
title: Guide to Elastic Search
date: 2017-09-24

---

Elasticsearch is a search engine ideal for full text search. 
Lot of companies use it to fully or partially power their search and autocomplete features on their platform.  To get an idea of which comp"

      
Elasticsearch is a search engine ideal for full text search.
Lot of companies use it to fully or partially power their search and autocomplete features on their platform. 
To get an idea of which companies are using it and how they are using it, visit <a href="https://stackshare.io/elasticsearch/in-stacks" target="_blank" rel="external">stackshare</a>.
This tutorial will guide you in :
- setting up elastic search
- terminology
- curl commands to index, update, search</li>

# Setup

If you plan to use a hosted offering, take a look at 
- [Amazon’s Elastic Search](https://aws.amazon.com/elasticsearch-service/pricing/)
- [Google Cloud Launcher](https://console.cloud.google.com/launcher/browse?q=elastic)
- Hosting from [ElaticCo](https://www.elastic.co/cloud/as-a-service/subscriptions)  maintainers of ElasticSearch


``` bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:5.6.0
# folder that we are going to save elastic search data locally
mkdir esdata
docker run -p 9200:9200 -e "http.host=0.0.0.0" -e "transport.host=127.0.0.1" -v esdata/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:5.6.0

```

without docker

```bash
// Linux/Mac
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.0.tar.gz
// Windows
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.0.zip
unzip the archive and run
bin/elasticsearch

```

To verify everything is working, navigate to http://localhost:9200/. You should see something like.
```json
{
    "name": "kl9yfPi",
    "cluster_name": "elasticsearch",
    "cluster_uuid": "j3jdeZJuQciCEaPibQPtzg",
    "version": {
        "number": "5.6.0",
        "build_hash": "781a835",
        "build_date": "2017-09-07T03:09:58.087Z",
        "build_snapshot": false,
        "lucene_version": "6.6.0"
    },
    "tagline": "You Know, for Search"
}
```


## II. Terminology

### Document

Any item that needs to be stored in elastic search.
Examples of a Document can be Artist Info, Song Info and lyrics, User Profile,News articles, Tweets.

Any item that can be represented as a json , can be a document. A document is composed of multiple fields that may be indexed.

Here is a sample document for

```json
{
   "movie_id":1,
   "title":"Hidden Figures",
   "director":"Theodroe Melfi",
   "actors":[
      "Taraji P. Henson",
      "Octavia Spencer",
      "Janelle Monáe"
   ],
   "duration":127,
   "lang":"en",
   "genres":[
      "Biography",
      "drama",
      "history"
   ],
   "description":"",
   "release date":"2017/6/1"
}
```

Once a doc is indexed, you can query on any fields. You can ask questions like

- All biography movies released this Year
- All Movies with a certain actor
- All movies that have certain words in description



## Type
Defines the schema and mapping shared by documents. You can specify how you want to index different fields
A index can have multiple schemas.
If you are indexing a movie site, there would be a type for person (actor, director), movie, review.

## Indices
Data structure used by Elastic Search to store info for fast retrieval. Elastic Search stores info in an “Inverted Index”.
Here is an example of an inverted index.

Movie 1
Aladdin is a 1992 American animated musical fantasy film produced by Disney.

Movie 2:
Mulan is a 1998 American animated musical action comedy-drama film produced by Disney


| Term       | (Doc id, pos)    |
|------------|------------------|
| Aladdin    | (1,1)            |
|  Mulan     | (2,1)            |
|  American  | (1,5), (2,5)     |
|  Disney    | (1,12), (2,13)   |




When searching for matches in the index, Elastic Search uses TF-IDF.
If there is a lot of documents to index, Elastic Search can break the index into shards that are stored in different machines.

TF-IDF
A Scoring algorithm for two documents.
Product of “Term Frequency” and “Inverse Document Frequency”
Term Frequency/ Document Frequency can be used to measure relevance.

Term Frequency is how often a term appears in a docuemnt .
Document Frequency is how often a term appears in all documents.

The intuition for this formula is that

words that appear in a lot of documents, might not be very useful.
words that appear a lot of time in one document and rarely in other docs, is more relevant to the query
Shard
In order to scale, Elastic Search can split the index into smaller shards.
A shard has its own copy of the index.
Every document is sharded into a specific shard.

III. Commands
For the rest of the tutorial, we are going to use a movie dataset from MovieLens.
The data is spread across multiple csv files.

For simplicity sake, I have processed the three files using this script and stored it in this file.

Lets look at some sample data in this file

## IMAGE 


The core info we are storing is movieId, title, genres, tags, imdbId, tmdbId, numRatings.
Tags and genres are lists.

To interact with your elastic search cluster, we are going to use the http requests.
If you want a ui to make the requests, you can use Postman or you can use the elasticsearch plugin elastichead chrome plugin

If you decide to use the elasticsearch head plugin, navigate to the “Any Request” tab.
Here is the ElasticSearch Head ui.


[Elastic Search Head]


Create a schema/ type
Before we can store the data, we need to create a schema.
Send a put request to the below url with payload

```$xslt
localhost:9200/movies

```



```json
{
  "mappings": {
    "movie": {
      "_all": {
        "enabled": false
      },
      "properties": {
        "movieId": {
          "type": "text"
        },
        "title": {
          "type": "text"
        },
        "genres": {
          "type": "text"
        },
        "tags": {
          "type": "text"
        },
        "imdbId": {
          "type": "text",
          "index": "no"
        },
        "tmdbId": {
          "type": "text",
          "index": "no"
        },
        "numRatings": {
          "type": "integer",
          "index": "no"
        }
      }
    }
  }
}
```


Here is the ESHead ui containing mapping.


[Create Mapping]

We are defining a mapping called “movie”.
By default, Elastic Search stores all data in the _all field.
To disable that, we set enabled to false.

The properties field contains all the fields we want to index.
For every property, we can specify the type such as text.
We could also specify, if we want to store a field but not index it using index=no

Insert one document
To add a document, we need to send a put request to

```$xslt
localhost:9200/{index}/{schema}/{doc_id}

```

In our case, it would be

```$xslt
localhost:9200/movies/movie/1

```

The payload would be


```json
{
  "movieId": "1",
  "title": "Toy Story (1995)",
  "genres": [
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Fantasy"
  ],
  "year": 1995,
  "imdbId": "0114709",
  "tmdbId": "862",
  "numRatings": 247,
  "tags": [
    "Pixar"
  ]
}
```


Here is the ESHead UI with the payload.
[Insert One Doc]


# Delete Doc
To delete doc, we need to send a delete request to
```$xslt
localhost:9200/{index}/{schema}/{doc_id}

```

So, if we want to delete the document we inserted, send a request to

```$xslt
localhost:9200/movies/movie/1

```

Here is the ESHead UI with the payload.
[Delete Doc]


## Insert multiple documents
If you want to insert multiple documents at once, you need to create a payload like

[Bulk Payload]


Here is the command I used to convert the movies.json file to the appropriate file.

```$xslt
cat movies.json | jq -c ' {"index": {"_index": "movies", "_type": "movie", "_id"
: .movieId}}, .' > movies_bulk.json
```


You need to use JQ tool.

For simplicity sake, here is the output file after the command.

Once you use download the file, run the below command to bulk insert the docs.



```$xslt
curl -XPOST localhost:9200/_bulk --data-binary  @./movies_bulk.json

```



# Search
Creating an elastic search query can be a bit difficult.
To create the query, lets use the “Structured Query” in elasticsearch.

Here is an example query, to find all movies that

- have “harry” in title
- released after 2000
- genre is Fantasy

[Search Query]

If you want to send the query using curl, click the checkbox “Show query source”.



[Raw Query]


If you want to see the raw payload, change the value of “Output Results” to json.


[Search Results]



For testing, using docker
<figure class="highlight bash"><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div><div class="line">3</div><div class="line">4</div><div class="line">5</div><div class="line">6</div></pre></td><td class="code"><pre><div class="line">docker pull docker.elastic.co/elasticsearch/elasticsearch:5.6.0</div><div class="line"></div><div class="line"><span class="comment"># folder that we are going to save elastic search data locally</span></div><div class="line">mkdir esdata</div><div class="line"></div><div class="line">docker run -p 9200:9200 -e <span class="string">"http.host=0.0.0.0"</span> -e <span class="string">"transport.host=127.0.0.1"</span> -v esdata/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:5.6.0</div></pre></td></tr></table></figure>
without docker<br><figure class="highlight bash"><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div><div class="line">3</div><div class="line">4</div><div class="line">5</div><div class="line">6</div><div class="line">7</div><div class="line">8</div><div class="line">9</div><div class="line">10</div></pre></td><td class="code"><pre><div class="line">// Linux/Mac</div><div class="line">wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.0.tar.gz</div><div class="line"></div><div class="line">// Windows</div><div class="line">wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.0.zip</div><div class="line"></div><div class="line">unzip the archive and run</div><div class="line"></div><div class="line">bin/elasticsearch</div><div class="line"></div></pre></td></tr></table></figure>
To verify everything is working, navigate to <a href="http://localhost:9200/" target="_blank" rel="external">http://localhost:9200/</a>. You should see something like.
<figure class="highlight json"><figcaption><span>lang:.json</span></figcaption><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div><div class="line">3</div><div class="line">4</div><div class="line">5</div><div class="line">6</div><div class="line">7</div><div class="line">8</div><div class="line">9</div><div class="line">10</div><div class="line">11</div><div class="line">12</div><div class="line">13</div></pre></td><td class="code"><pre><div class="line">&#123;</div><div class="line">    <span class="attr">"name"</span>: <span class="string">"kl9yfPi"</span>,</div><div class="line">    <span class="attr">"cluster_name"</span>: <span class="string">"elasticsearch"</span>,</div><div class="line">    <span class="attr">"cluster_uuid"</span>: <span class="string">"j3jdeZJuQciCEaPibQPtzg"</span>,</div><div class="line">    <span class="attr">"version"</span>: &#123;</div><div class="line">        <span class="attr">"number"</span>: <span class="string">"5.6.0"</span>,</div><div class="line">        <span class="attr">"build_hash"</span>: <span class="string">"781a835"</span>,</div><div class="line">        <span class="attr">"build_date"</span>: <span class="string">"2017-09-07T03:09:58.087Z"</span>,</div><div class="line">        <span class="attr">"build_snapshot"</span>: <span class="literal">false</span>,</div><div class="line">        <span class="attr">"lucene_version"</span>: <span class="string">"6.6.0"</span></div><div class="line">    &#125;,</div><div class="line">    <span class="attr">"tagline"</span>: <span class="string">"You Know, for Search"</span></div><div class="line">&#125;</div></pre></td></tr></table></figure>
<h1 id="II-Terminology"><a href="#II-Terminology" class="headerlink" title="II. Terminology"></a>II. Terminology</h1><h2 id="Document"><a href="#Document" class="headerlink" title="Document"></a>Document</h2>Any item that needs to be stored in elastic search.<br>Examples of a Document can be Artist Info, Song Info and lyrics, User Profile,News articles, Tweets.
Any item that  can be represented as a json , can be a document. A document is composed of multiple fields that may be indexed.
Here is a sample document for 
<figure class="highlight json"><figcaption><span>lang:.json</span></figcaption><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div><div class="line">3</div><div class="line">4</div><div class="line">5</div><div class="line">6</div><div class="line">7</div><div class="line">8</div><div class="line">9</div><div class="line">10</div><div class="line">11</div><div class="line">12</div><div class="line">13</div><div class="line">14</div><div class="line">15</div><div class="line">16</div><div class="line">17</div><div class="line">18</div><div class="line">19</div></pre></td><td class="code"><pre><div class="line">&#123;</div><div class="line">   <span class="attr">"movie_id"</span>:<span class="number">1</span>,</div><div class="line">   <span class="attr">"title"</span>:<span class="string">"Hidden Figures"</span>,</div><div class="line">   <span class="attr">"director"</span>:<span class="string">"Theodroe Melfi"</span>,</div><div class="line">   <span class="attr">"actors"</span>:[</div><div class="line">      <span class="string">"Taraji P. Henson"</span>,</div><div class="line">      <span class="string">"Octavia Spencer"</span>,</div><div class="line">      <span class="string">"Janelle Monáe"</span></div><div class="line">   ],</div><div class="line">   <span class="attr">"duration"</span>:<span class="number">127</span>,</div><div class="line">   <span class="attr">"lang"</span>:<span class="string">"en"</span>,</div><div class="line">   <span class="attr">"genres"</span>:[</div><div class="line">      <span class="string">"Biography"</span>,</div><div class="line">      <span class="string">"drama"</span>,</div><div class="line">      <span class="string">"history"</span></div><div class="line">   ],</div><div class="line">   <span class="attr">"description"</span>:<span class="string">""</span>,</div><div class="line">   <span class="attr">"release date"</span>:<span class="string">"2017/6/1"</span></div><div class="line">&#125;</div></pre></td></tr></table></figure>
Once a doc is indexed, you can query on any fields. You can ask questions like
<ul>
<li>All biography movies released this Year</li>
<li>All Movies with a certain actor</li>
<li>All movies that have certain words in description</li>
</ul>
<h2 id="Type"><a href="#Type" class="headerlink" title="Type"></a>Type</h2>Defines the schema and mapping shared by documents. You can specify how you want to index different fields<br>A index can have multiple schemas.<br>If you are indexing a movie site, there would be a type for person (actor, director), movie, review.
<h2 id="Indices"><a href="#Indices" class="headerlink" title="Indices"></a>Indices</h2>Data structure used by Elastic Search to store info for fast retrieval. Elastic Search stores info in an “Inverted Index”.<br>Here is an example of an inverted index.
Movie 1<br>Aladdin is a 1992 American animated musical fantasy film produced by Disney.
Movie 2:<br>Mulan is a 1998 American animated musical action comedy-drama film produced by Disney 
<table>
<thead>
<tr>
<th>Term</th>
<th style="text-align:center">(Doc id, pos)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Aladdin</td>
<td style="text-align:center">(1,1)</td>
</tr>
<tr>
<td>Mulan</td>
<td style="text-align:center">(2,1)</td>
</tr>
<tr>
<td>American</td>
<td style="text-align:center">(1,5), (2,5)</td>
</tr>
<tr>
<td>Disney</td>
<td style="text-align:center">(1,12), (2,13)</td>
</tr>
</tbody>
</table>
When searching for matches in the index, Elastic Search uses TF-IDF.<br>If there is a lot of documents to index, Elastic Search can break the index into shards that are stored in different machines.
<h2 id="TF-IDF"><a href="#TF-IDF" class="headerlink" title="TF-IDF"></a>TF-IDF</h2>A Scoring algorithm for two documents.<br>Product of “Term Frequency” and “Inverse Document Frequency”<br>Term Frequency/ Document Frequency can be used to measure relevance.
<strong>Term Frequency</strong> is how often a term appears in a docuemnt .<br><strong>Document Frequency</strong> is how often a term appears in all documents.
The intuition for this formula is that 
<ul>
<li>words that appear in a lot of documents, might not be very useful. </li>
<li>words that appear a lot of time in one document and rarely in other docs, is more relevant to the query</li>
</ul>
<h2 id="Shard"><a href="#Shard" class="headerlink" title="Shard"></a>Shard</h2>In order to scale, Elastic Search can split the index into smaller shards.<br>A shard has its own copy of the index.<br>Every document is sharded into a specific shard.
<h1 id="III-Commands"><a href="#III-Commands" class="headerlink" title="III. Commands"></a>III. Commands</h1>For the rest of the tutorial, we are going to use a movie dataset from <a href="https://grouplens.org/datasets/movielens/" target="_blank" rel="external">MovieLens</a>.<br>The data is spread across multiple csv files. 
For simplicity sake, I have processed the three files using this <a href="helper.py">script</a> and stored it in this <a href="movies.csv.zip">file</a>.
Lets look at some sample data in this file<br><img src="/2017/09/04/elastic/sample_movies.png" alt="[Sample Movies]" title="[Sample Movies]">
The core info we are storing is movieId, title, genres, tags, imdbId, tmdbId, numRatings.<br>Tags and genres are lists.
To interact with your elastic search cluster, we are going to use the http requests.<br>If you want a ui to make the requests, you can use <a href="https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en" target="_blank" rel="external">Postman</a> or you can use the elasticsearch plugin elastichead <a href="https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm/" target="_blank" rel="external">chrome plugin</a> 
If you decide to use the elasticsearch head plugin, navigate to the “Any Request” tab.<br>Here is the ElasticSearch Head ui.<br><img src="/2017/09/04/elastic/elasticsearch_head_anyquery.png" alt="[Elastic Search Head]" title="[Elastic Search Head]">
<h2 id="Create-a-schema-type"><a href="#Create-a-schema-type" class="headerlink" title="Create a schema/ type"></a>Create a schema/ type</h2>Before we can store the data, we need to create a schema.<br>Send a put request to the below url with payload<br><figure class="highlight avrasm"><table><tr><td class="gutter"><pre><div class="line">1</div></pre></td><td class="code"><pre><div class="line"><span class="symbol">localhost:</span><span class="number">9200</span>/movies</div></pre></td></tr></table></figure>
<figure class="highlight json"><figcaption><span>lang:.json</span></figcaption><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div><div class="line">3</div><div class="line">4</div><div class="line">5</div><div class="line">6</div><div class="line">7</div><div class="line">8</div><div class="line">9</div><div class="line">10</div><div class="line">11</div><div class="line">12</div><div class="line">13</div><div class="line">14</div><div class="line">15</div><div class="line">16</div><div class="line">17</div><div class="line">18</div><div class="line">19</div><div class="line">20</div><div class="line">21</div><div class="line">22</div><div class="line">23</div><div class="line">24</div><div class="line">25</div><div class="line">26</div><div class="line">27</div><div class="line">28</div><div class="line">29</div><div class="line">30</div><div class="line">31</div><div class="line">32</div><div class="line">33</div><div class="line">34</div><div class="line">35</div></pre></td><td class="code"><pre><div class="line">&#123;</div><div class="line">  <span class="attr">"mappings"</span>: &#123;</div><div class="line">    <span class="attr">"movie"</span>: &#123;</div><div class="line">      <span class="attr">"_all"</span>: &#123;</div><div class="line">        <span class="attr">"enabled"</span>: <span class="literal">false</span></div><div class="line">      &#125;,</div><div class="line">      <span class="attr">"properties"</span>: &#123;</div><div class="line">        <span class="attr">"movieId"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"text"</span></div><div class="line">        &#125;,</div><div class="line">        <span class="attr">"title"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"text"</span></div><div class="line">        &#125;,</div><div class="line">        <span class="attr">"genres"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"text"</span></div><div class="line">        &#125;,</div><div class="line">        <span class="attr">"tags"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"text"</span></div><div class="line">        &#125;,</div><div class="line">        <span class="attr">"imdbId"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"text"</span>,</div><div class="line">          <span class="attr">"index"</span>: <span class="string">"no"</span></div><div class="line">        &#125;,</div><div class="line">        <span class="attr">"tmdbId"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"text"</span>,</div><div class="line">          <span class="attr">"index"</span>: <span class="string">"no"</span></div><div class="line">        &#125;,</div><div class="line">        <span class="attr">"numRatings"</span>: &#123;</div><div class="line">          <span class="attr">"type"</span>: <span class="string">"integer"</span>,</div><div class="line">          <span class="attr">"index"</span>: <span class="string">"no"</span></div><div class="line">        &#125;</div><div class="line">      &#125;</div><div class="line">    &#125;</div><div class="line">  &#125;</div><div class="line">&#125;</div></pre></td></tr></table></figure>
Here is the ESHead ui containing mapping.<br><img src="/2017/09/04/elastic/elasticsearch_create_mapping.png" alt="[Create Mapping]" title="[Create Mapping]">
We are defining a mapping called “movie”.<br>By default, Elastic Search stores all data in the <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-all-field.html" target="_blank" rel="external">_all field</a>.<br>To disable that, we set enabled to false.
The properties field contains all the fields we want to index.<br>For every property, we can specify the type such as text.<br>We could also specify, if we want to store a field but not index it using index=no
<h2 id="Insert-one-document"><a href="#Insert-one-document" class="headerlink" title="Insert one document"></a>Insert one document</h2>To add a document, we need to send a put request to<br><figure class="highlight dust"><table><tr><td class="gutter"><pre><div class="line">1</div></pre></td><td class="code"><pre><div class="line"><span class="xml">localhost:9200/</span><span class="template-variable">&#123;index&#125;</span><span class="xml">/</span><span class="template-variable">&#123;schema&#125;</span><span class="xml">/</span><span class="template-variable">&#123;doc_id&#125;</span><span class="xml"></span></div></pre></td></tr></table></figure>
In our case, it would be<br><figure class="highlight dts"><table><tr><td class="gutter"><pre><div class="line">1</div></pre></td><td class="code"><pre><div class="line"><span class="symbol">localhost:</span><span class="number">9200</span><span class="meta-keyword">/movies/</span>movie/<span class="number">1</span></div></pre></td></tr></table></figure>
The payload would be<br><figure class="highlight json"><figcaption><span>lang:.json</span></figcaption><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div><div class="line">3</div><div class="line">4</div><div class="line">5</div><div class="line">6</div><div class="line">7</div><div class="line">8</div><div class="line">9</div><div class="line">10</div><div class="line">11</div><div class="line">12</div><div class="line">13</div><div class="line">14</div><div class="line">15</div><div class="line">16</div><div class="line">17</div><div class="line">18</div></pre></td><td class="code"><pre><div class="line">&#123;</div><div class="line">  <span class="attr">"movieId"</span>: <span class="string">"1"</span>,</div><div class="line">  <span class="attr">"title"</span>: <span class="string">"Toy Story (1995)"</span>,</div><div class="line">  <span class="attr">"genres"</span>: [</div><div class="line">    <span class="string">"Adventure"</span>,</div><div class="line">    <span class="string">"Animation"</span>,</div><div class="line">    <span class="string">"Children"</span>,</div><div class="line">    <span class="string">"Comedy"</span>,</div><div class="line">    <span class="string">"Fantasy"</span></div><div class="line">  ],</div><div class="line">  <span class="attr">"year"</span>: <span class="number">1995</span>,</div><div class="line">  <span class="attr">"imdbId"</span>: <span class="string">"0114709"</span>,</div><div class="line">  <span class="attr">"tmdbId"</span>: <span class="string">"862"</span>,</div><div class="line">  <span class="attr">"numRatings"</span>: <span class="number">247</span>,</div><div class="line">  <span class="attr">"tags"</span>: [</div><div class="line">    <span class="string">"Pixar"</span></div><div class="line">  ]</div><div class="line">&#125;</div></pre></td></tr></table></figure>
Here is the ESHead UI with the payload.
<img src="/2017/09/04/elastic/elasticsearch_insert_one_doc.png" alt="[Insert One Doc]" title="[Insert One Doc]">
<h2 id="Delete-Doc"><a href="#Delete-Doc" class="headerlink" title="Delete Doc"></a>Delete Doc</h2>To delete doc, we need to send a delete request to<br><figure class="highlight dust"><table><tr><td class="gutter"><pre><div class="line">1</div></pre></td><td class="code"><pre><div class="line"><span class="xml">localhost:9200/</span><span class="template-variable">&#123;index&#125;</span><span class="xml">/</span><span class="template-variable">&#123;schema&#125;</span><span class="xml">/</span><span class="template-variable">&#123;doc_id&#125;</span><span class="xml"></span></div></pre></td></tr></table></figure>
So, if we want to delete the document we inserted, send a request to<br><figure class="highlight dts"><table><tr><td class="gutter"><pre><div class="line">1</div></pre></td><td class="code"><pre><div class="line"><span class="symbol">localhost:</span><span class="number">9200</span><span class="meta-keyword">/movies/</span>movie/<span class="number">1</span></div></pre></td></tr></table></figure>
Here is the ESHead UI with the payload.<br><img src="/2017/09/04/elastic/elasticsearch_delete.png" alt="[Delete Doc]" title="[Delete Doc]">
<h2 id="Insert-multiple-documents"><a href="#Insert-multiple-documents" class="headerlink" title="Insert multiple documents"></a>Insert multiple documents</h2>If you want to insert multiple documents at once, you need to create a payload like
<img src="/2017/09/04/elastic/elasticsearch_bulkpayload.png" alt="[Bulk Payload]" title="[Bulk Payload]">
Here is the command I used to convert the movies.json file to the appropriate file.<br><figure class="highlight 1c"><table><tr><td class="gutter"><pre><div class="line">1</div><div class="line">2</div></pre></td><td class="code"><pre><div class="line">cat movies.json <span class="string">| jq -c ' &#123;"</span>index<span class="string">": &#123;"</span>_index<span class="string">": "</span>movies<span class="string">", "</span>_type<span class="string">": "</span>movie<span class="string">", "</span>_id<span class="string">"</span></div><div class="line">: .movieId&#125;&#125;, .' &gt; movies_bulk.json</div></pre></td></tr></table></figure>
You need to use <a href="https://stedolan.github.io/jq/" target="_blank" rel="external">JQ</a> tool.
For simplicity sake, <a href="movies_bulk.json.zip">here</a> is the output file after the command.
Once you use download the file, run the below command to bulk insert the docs.<br><figure class="highlight armasm"><table><tr><td class="gutter"><pre><div class="line">1</div></pre></td><td class="code"><pre><div class="line"><span class="symbol">curl</span> -XPOST localhost:<span class="number">9200</span>/_bulk --<span class="meta">data</span>-<span class="keyword">binary </span> <span class="comment">@./movies_bulk.json</span></div></pre></td></tr></table></figure>
<h2 id="Search"><a href="#Search" class="headerlink" title="Search"></a>Search</h2>Creating an elastic search query can be a bit difficult.<br>To create the query, lets use the “Structured Query” in elasticsearch.
Here is an example query, to find all movies that
<ul>
<li>have “harry” in title</li>
<li>released after 2000</li>
<li>genre is Fantasy</li>
</ul>
<img src="/2017/09/04/elastic/search_query_es.png" alt="[Search Query]" title="[Search Query]">
If you want to send the query using curl, click the checkbox “Show query source”.
<img src="/2017/09/04/elastic/elasticsearch-raw_search_query.png" alt="[Raw Query]" title="[Raw Query]">
If you want to see the raw payload, change the value of “Output Results” to json.
<img src="/2017/09/04/elastic/elasticsearch-searchresults.png" alt="[Search Results]" title="[Search Results]">

      
    </div>
    <footer class="article-footer">
      <a data-url="http://npatta01.github.io/2017/09/04/elastic/" data-id="cj7icp3ac0023qduyyy7keqhz" class="article-share-link">Share</a>
      
        <a href="http://npatta01.github.io/2017/09/04/elastic/#disqus_thread" class="article-comment-link">Comments</a>
      
      
  <ul class="article-tag-list"><li class="article-tag-list-item"><a class="article-tag-list-link" href="/tags/database/">database</a></li><li class="article-tag-list-item"><a class="article-tag-list-link" href="/tags/elastic-search/">elastic search</a></li><li class="article-tag-list-item"><a class="article-tag-list-link" href="/tags/python/">python</a></li><li class="article-tag-list-item"><a class="article-tag-list-link" href="/tags/tutorial/">tutorial</a></li></ul>

    </footer>
  </div>
  

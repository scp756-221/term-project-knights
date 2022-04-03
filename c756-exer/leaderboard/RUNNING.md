### How to run:
After taking the clone of the repo,
open 4 terminal windows.

#### In the first one we run the dynamodb:

<pre><code>cd dynamodb_local_latest/

java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb</code></pre>

#### In the second one we create the table (not needed currently with db):

<pre><code>cd leaderboard/

python create_table.py</code></pre>


#### In the third one we run the server on port 30001:

<pre><code>cd leaderboard/

python app.py 30001</code></pre>

#### In the fourth one we run the mcli to listen on port 30001:

<pre><code>cd mcli/

python mcli.py localhost 30001</code></pre>

After that you can use "read", "create", and "delete" functionalities to test
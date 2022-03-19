## What does this app do?

This app is to read top 10 songs by upvotes

## Running :
1. Open two terminals
2. In 1st terminal run tools/shell.sh and then write the following command:
<pre><code>make -f k8s-tpl.mak templates</code></pre>

3. And then:
<pre><code>cd lb</code></pre>

4. Build the app
<pre><code>./build.sh</code></pre>

5. Run the app
<pre><code>./run.sh</code></pre>

6. In the 2nd terminal:
<pre><code>cd mcli</code></pre>

7. Build and run mcli:
<pre><code>make build-mcli
make run-mcli</code></pre>

8. Now you can check the services. Start with "read"

Then you can use help commands to run "upvote" and "genre" functionalities.


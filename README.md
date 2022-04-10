[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7091299&assignment_repo_type=AssignmentRepo)

**_Term-Project-Knights_**

To move away from the use of tools container (tools/shell.sh), we need to install the dependencies outside of the 
tools container. The following list of dependencies serve as pre-requisites for further steps in 
this project.

**PRE-REQUISITES:**

Install ==> <artefact> 
    where <artefact> is ,
            1) kubectl
            2) eksctl
            3) minicube
            4) istioctl
            5) helm
            6) k9s

**REPO:**

Clone the git repo for term-project-knights (or pull latest from main to make sure you have latest changes).

The githubid is unique for every user. Before proceeding, make sure to replace your githubuserid in all places, if not 
already done.

**CONFIGURATIONS:**

Make sure your aws configurations and kube configurations from the course assignments are carried forward towards
the term project. We will re-use several components from earlier assignments. This includes the "*-tpl" template files
from which the actual configurations and executables will be derived from.

**GENERATE ARTEFACTS FROM TEMPLATES:**

<pre><code>tools/process-templates.sh</code></pre> --> to generate configurations from templates

**EKS CLUSTER:**

To start the cluster, 
<pre><code>make -f eks.mak start</code></pre>

To delete the cluster, 
<pre><code>make -f eks.mak stop</code></pre>

**_NOTE: Do not forget to delete the cluster after the end of the day's work. You will be billed for its continued
execution._**

**EKS CLUSTER NAMESPACES & CONTEXTS:**

<pre><code>kubectl config use-context aws756</code></pre>
<pre><code>kubectl create ns c756ns</code></pre>
<pre><code>kubectl config set-context aws756 --namespace=c756ns</code></pre>
<pre><code>istioctl install -y --set profile=demo --set hub=gcr.io/istio-release</code></pre>
<pre><code>kubectl label namespace c756ns istio-injection=enabled</code></pre>


Steps, 1-3 should deploy all your services into your EKS clusters

1) TO BUILD DOCKER IMAGES:
<pre><code>make -f k8s.mak cri</code></pre>

2) TO PROVISION/DEPLOY THE EKS CLUSTER:
<pre><code>make -f k8s.mak provision</code></pre>

3) TO LOAD THE DATA INTO DYNAMODB:
<pre><code>make -f k8s.mak loader</code></pre>

4) TO DELETE ALL PODS AND DEPLOYMENTS:
<pre><code>kubectl delete deployment --all</code></pre>

5) TO CLEAN LOGS AND PREPARE FRESH DEPLOYMENT:
<pre><code>make -f k8s.mak clean</code></pre>

**K9S:**

You can check the deployments using k9s. Open a new terminal and type "k9s". k9s control terminal should open up 
to track the status of deployments.

**GET EXTERNAL IP OF EKS CLUSTER:**

The following command should give you the EXTERNAL_IP of the EKS Cluster, which will serve as an entry point.

<pre><code>kubectl get svc --all-namespaces | cut -c -140</code></pre>

You should now be able to connect to this EXTERNAL_IP via the mcli and execute commands. In case of error, 
you can check the logs using commands mentioned in Assignment 4 to retrieve the logs and address the issues.


**TO REMOVE ALL DOCKER IMAGES (USE WITH CAUTION):**

<pre><code>docker rmi -f $(docker images -a -q)</code></pre>

### To run Grafana dashboard

<pre><code>make -f k8s.mak grafana-url</code></pre>

### To run Prometheus dashbord

<pre><code>make -f k8s.mak prometheus-url</code></pre>

### To run Gatling

1. Go to tools/gatling-1-music.sh and add your cluster ip

2. To run from root folder:
<pre><code> tools/gatling-1-music.sh</code></pre>

3. To stop call:
<pre><code>tools/kill-gatling.sh</code></pre>

### To run the app locally:

1. Run 3 terminal windows.

2. In the first window, run the db:
<pre><code> cd dynamodb_local_latest 
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb</code></pre>

3. In the second window, run the app:
<pre><code> cd leaderboard_local
python app.py 30001 </code></pre>

4. In the third window, run the mcli to test:
<pre><code> cd leaderboard_local
python mcli.py localhost 30001 </code></pre>

After that you can test "read", "create", and "delete" functionalities.


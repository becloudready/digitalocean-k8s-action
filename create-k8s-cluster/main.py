import os
import requests
import time

# Read input variables
DO_TOKEN = os.getenv("INPUT_DIGITALOCEAN_TOKEN")
CLUSTER_NAME = os.getenv("INPUT_CLUSTER_NAME", "my-k8s-cluster")
REGION = os.getenv("INPUT_REGION", "nyc3")
NODE_SIZE = os.getenv("INPUT_NODE_SIZE", "s-2vcpu-4gb")
NODE_COUNT = int(os.getenv("INPUT_NODE_COUNT", "2"))

# DigitalOcean API Endpoint
API_URL = "https://api.digitalocean.com/v2/kubernetes/clusters"

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {DO_TOKEN}",
    "Content-Type": "application/json"
}

def create_k8s_cluster():
    """Creates a Kubernetes cluster on DigitalOcean."""
    data = {
        "name": CLUSTER_NAME,
        "region": REGION,
        "version": "latest",
        "node_pools": [
            {
                "name": "default-pool",
                "size": NODE_SIZE,
                "count": NODE_COUNT
            }
        ]
    }

    response = requests.post(API_URL, json=data, headers=HEADERS)
    
    if response.status_code == 201:
        cluster = response.json()
        cluster_id = cluster["kubernetes_cluster"]["id"]
        print(f"✅ Cluster {CLUSTER_NAME} is being created (ID: {cluster_id})")
        return cluster_id
    else:
        print(f"❌ Failed to create cluster: {response.text}")
        exit(1)

def wait_for_cluster_ready(cluster_id):
    """Waits until the Kubernetes cluster is ready."""
    while True:
        response = requests.get(f"{API_URL}/{cluster_id}", headers=HEADERS)
        if response.status_code == 200:
            cluster_status = response.json()["kubernetes_cluster"]["status"]["state"]
            print(f"🔄 Cluster Status: {cluster_status}")
            if cluster_status == "running":
                print("✅ Cluster is ready!")
                break
        else:
            print("❌ Error fetching cluster status!")
            exit(1)
        time.sleep(15)  # Wait before checking again

def get_kubeconfig(cluster_id):
    """Fetches and saves the Kubeconfig file."""
    response = requests.get(f"{API_URL}/{cluster_id}/kubeconfig", headers=HEADERS)
    
    if response.status_code == 200:
        with open("/github/workspace/kubeconfig.yaml", "w") as f:
            f.write(response.text)
        print("✅ Kubeconfig saved to kubeconfig.yaml")
    else:
        print("❌ Failed to fetch kubeconfig")
        exit(1)

if __name__ == "__main__":
    cluster_id = create_k8s_cluster()
    wait_for_cluster_ready(cluster_id)
    get_kubeconfig(cluster_id)


# 🚀 DigitalOcean Kubernetes GitHub Action

This **GitHub Action** automates the creation of a **Kubernetes cluster on DigitalOcean** using the DigitalOcean API.

## 🎯 Features
- Creates a Kubernetes cluster on DigitalOcean
- Saves **Kubeconfig** for future deployments
- Supports configurable cluster size and region
- Uses **Python** instead of `doctl`

---

## 🛠️ Usage

### **1️⃣ Add to Your GitHub Workflow**
Create a workflow file at `.github/workflows/deploy.yml`:

```yaml
name: Deploy Kubernetes Cluster on DigitalOcean

on:
  workflow_dispatch:  # Allows manual trigger
  push:
    branches:
      - main  # Runs on push to main branch

jobs:
  create-cluster:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Create DigitalOcean Kubernetes Cluster
        uses: ./create-k8s-cluster  # If action is in the same repo
        with:
          digitalocean_token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
          cluster_name: "prod-cluster"
          region: "nyc3"
          node_size: "s-2vcpu-4gb"
          node_count: "3"

      - name: Save Kubeconfig for future steps
        run: cat kubeconfig.yaml
```

---

### **2️⃣ Inputs**
| Name                  | Description                         | Required | Default         |
|-----------------------|-------------------------------------|----------|-----------------|
| `digitalocean_token`  | DigitalOcean API Token             | ✅ Yes    | `None`          |
| `cluster_name`        | Kubernetes cluster name            | ❌ No     | `my-k8s-cluster`|
| `region`             | DigitalOcean region (e.g., `nyc3`) | ❌ No     | `nyc3`          |
| `node_size`          | Node size (e.g., `s-2vcpu-4gb`)    | ❌ No     | `s-2vcpu-4gb`   |
| `node_count`         | Number of nodes                    | ❌ No     | `2`             |

---

### **3️⃣ Setup API Token**
1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add:
   - **Name:** `DIGITALOCEAN_ACCESS_TOKEN`
   - **Value:** _Your DigitalOcean API Token_

---

### **4️⃣ Running the Workflow**
- **Manual Trigger:** Go to **GitHub Actions** → **Select Workflow** → Click **Run Workflow**
- **Automatic Trigger:** Push changes to the `main` branch

---

## 📌 Notes
- The **Kubeconfig file** is saved as `kubeconfig.yaml`
- The cluster creation process takes **~5-10 minutes**
- **Ensure your API token has write permissions** for Kubernetes

---

## 📜 License
This project is licensed under the **MIT License**.

🚀 **Happy Deploying!**


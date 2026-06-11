# IBM Cloud Setup Guide

Step-by-step instructions to get your free IBM Cloud credentials for the Research Agent.

---

## Step 1 — Create a Free IBM Cloud Account

1. Go to https://cloud.ibm.com/registration
2. Sign up with your email (no credit card needed for Lite plan)
3. Verify your email and log in

---

## Step 2 — Create a Watson Studio Instance

1. In the IBM Cloud console, click **Catalog**
2. Search for **Watson Studio**
3. Select the **Lite** plan (free)
4. Click **Create**

---

## Step 3 — Create a Watson Machine Learning Instance

1. Go to **Catalog** again
2. Search for **Watson Machine Learning**
3. Select the **Lite** plan (free)
4. Click **Create**

---

## Step 4 — Create a Project

1. Go to https://dataplatform.cloud.ibm.com
2. Click **New project → Create an empty project**
3. Give it a name (e.g. "Research Agent")
4. Associate your **Watson Machine Learning** instance with this project
5. Click **Create**
6. From the project URL, copy your **Project ID**:
   - URL looks like: `https://dataplatform.cloud.ibm.com/projects/<PROJECT_ID>/...`

---

## Step 5 — Generate an API Key

1. In the IBM Cloud console top menu, click your avatar → **IAM**
2. Go to **API Keys** in the left sidebar
3. Click **Create an IBM Cloud API key**
4. Give it a name, click **Create**
5. **Copy the API key immediately** — it won't be shown again

---

## Step 6 — Configure .env

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```
IBM_API_KEY=your_copied_api_key
IBM_PROJECT_ID=your_project_id_from_step_4
IBM_WML_URL=https://us-south.ml.cloud.ibm.com
```

> **Note:** If you chose a region other than Dallas (us-south) when creating 
> Watson ML, update `IBM_WML_URL` accordingly:
> - London:    `https://eu-gb.ml.cloud.ibm.com`
> - Frankfurt: `https://eu-de.ml.cloud.ibm.com`
> - Tokyo:     `https://jp-tok.ml.cloud.ibm.com`

---

## Step 7 — Verify

Start the backend and call the health endpoint:

```bash
curl http://localhost:8000/api/health
# Expected: {"status": "healthy", "granite": true}
```

If `granite` is `false`, double-check your `IBM_API_KEY` and `IBM_PROJECT_ID`.

---

## IBM Lite Plan Limits

| Resource             | Free Limit          |
|----------------------|---------------------|
| WML API calls        | 50,000 / month      |
| Watson Studio CUH    | 10 CUH / month      |
| Storage              | 20 GB               |

These limits are more than enough for development and demonstration.

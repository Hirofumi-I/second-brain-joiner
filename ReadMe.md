# Second Brain Joiner: Complete Implementation Guide 🧠✨
〜 Connecting your Obsidian (Second Brain) to AI 〜

This guide is designed for users who say, **"I'm not a programmer, but I'm comfortable using a PC."** We’ve avoided technical jargon as much as possible and included step-by-step instructions for every single click.

---

## 🛠 Step 0: Preparation
First, let's gather the "tools" needed to connect your computer to the cloud (Google's servers).

### 1. Google Account
Your regular Gmail account will work perfectly.

### 2. Create a Storage Folder **(Important!)**
Create a dedicated folder to hold the tool's files.
1. Create a folder named **`python`** directly inside your **C: Drive**.
2. Inside that, create a folder named **`second-brain-joiner`**.
   * The path should be: `C:\python\second-brain-joiner`
3. Place all downloaded files (`main.py`, `requirements.txt`, `ReadMe.md`, etc.) into this folder.

### 3. Install Google Cloud CLI
We will install the "Magic Wand" that allows you to control the cloud via text commands instead of just clicking.

1. Open the [Google Cloud CLI Install Page](https://cloud.google.com/sdk/docs/install).
2. Look for the **"Windows"** tab.
3. Click the blue link **"Download the Google Cloud CLI installer"** and save the file.
4. Run the installer. Generally, you can click "Next" or "I Agree" for all prompts until finished.

---

## ☁️ Step 1: Create a Google Cloud Project

First, create a private "Workspace (Project)" inside Google Cloud.

1. Log in to the **[Google Cloud Console](https://console.cloud.google.com/)**.
2. Click **"Select a project"** at the top of the screen (to the right of the "Google Cloud" logo).
3. Click **"New Project"** in the top right of the popup window.
4. Enter `second-brain-joiner` as the Project Name and click **"Create"**.
5. **【CRITICAL】Register Billing Settings**
   - Go to the "≡ (Hamburger Menu)" in the top left and select **"Billing"**. Complete the registration with a credit card.
   - **Estimated Cost (Don't worry!)**:
     I (Dicon) run personal AI tools, and Google charges me roughly **$0.05 (8 JPY) per month**. It is extremely cheap.
   - **Why is this necessary?**:
     This is a form of identity verification to prevent bad actors from abusing cloud resources.

---

## 🔍 Step 2: Note your ID and Project Number
You will need the "identification codes" for your project later.

1. Return to the Google Cloud Dashboard (Home).
2. Look at the **"Project Info"** card in the center of the screen.
3. Copy these two values to a notepad:
   - **Project ID**: (e.g., `second-brain-joiner-12345`)
   - **Project Number**: (e.g., `123456789012`)

---

## 🚀 Step 3: Casting the Magic Spells (Commands)
This is the heart of the setup! Open the "Google Cloud SDK Shell" from your application list.💡 
> [!TIP]
> Tip for the "Black Screen": Standard "Ctrl + V" might not work. 
> To paste, simply Right-Click your mouse after copying a command! 😊

1. Login
First, connect your PC to Google Cloud:
```gcloud auth login```
A browser window will open. Select your Google account and click "Allow."

2. Specify your Project
Tell the tool which "room" to work in.
① Check your Project ID:
```gcloud projects list```
② Set the Project:Run this (Replace the brackets with your actual ID):
```gcloud config set project [YOUR_PROJECT_ID]```

3. Enable Google Cloud Features (GUI Recommended)
To avoid errors in the shell, it's safer to use the "Button approach."
This ensures everything flows smoothly.Go to the Google Cloud Console and use the search bar at the top:

   1. Search for "Cloud Functions API" → Click the blue "Enable" button.
   2. Search for "Cloud Build API" → Click "Enable".

4. Create a Bucket (Your Private Storage)
Create your unique "storage unit" in the cloud.

> ⚠️ IMPORTANT: Bucket names are "First come, first served."Add unique
>  letters/numbers to the end of second-brain-joiner- (e.g., second-brain-joiner-dicon777). 
> Note this name down!

```gcloud storage buckets create gs://second-brain-joiner-[YOUR_UNIQUE_NAME] --location=asia-northeast1```

5. "Summoning" the Agent & Granting Permissions
Final prep! Sometimes the "Service Agents" (the invisible workers) are sleeping after the API is turned on. We need to wake them up and give them their "ID Badges."(Replace brackets with your ID/Number).

① Summon the Agent:
```gcloud storage service-agent --project=[YOUR_PROJECT_ID]```

② Grant Permission 1:
```gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] --member="serviceAccount:service-[YOUR_PROJECT_NUMBER]@gcp-sa-eventarc.iam.gserviceaccount.com" --role="roles/storage.admin"```

③ Grant Permission 2:
```gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] --member="serviceAccount:service-[YOUR_PROJECT_NUMBER]@gs-project-accounts.iam.gserviceaccount.com" --role="roles/pubsub.publisher"```

---

## 🛠️ How to tell if a Command Succeeded
Don't be intimidated by the wall of text. Check these signs:

✅ Signs of Success (Big Victory!)
- You see a line: Updated IAM policy for project [Project Name].
- A long list of bindings: or - members: appears.
- The cursor returns to C:\Users\...>, ready for the next command.

> 💡 Developer's Note: Beginners often think "There's so much English text, it must be an error!" But as long as it says "Updated," you are doing great!

❌ Signs of Failure (Needs a re-check!)
- The word ERROR: is visible.
- You see phrases like INVALID_ARGUMENT or Permission Denied.
- The "Updated" message never shows up.

> 🆘 What to do? Don't panic. Re-check if your Billing is linked and if you clicked the "Enable API" buttons in the browser.

📊 Quick Diagnostic Table
| Status | Keywords to look for | Screen Vibe |
| :--- | :--- | :--- |
| **✅ SUCCESS!** | **Updated**, **bindings** | Busy screen, but ends peacefully. |
| **❌ FAILURE...** | **ERROR**, **Denied**, **Not found** | Short, stops with "angry" red-looking text. |

---

## 🏗️ Step 4: Deploying the Program
Now, let's put the program into the cloud!
① Move to your folder:
```cd /d C:\python\second-brain-joiner```
② Run the Deploy Command:Copy this to notepad first, edit the bucket name, then paste.
```gcloud functions deploy second-brain-joiner --gen2 --region=asia-northeast1 --runtime=python312 --source=. --entry-point=process_gcs_zip --trigger-bucket=[YOUR_BUCKET_NAME] --memory=1Gi --timeout=300s```

## ☕ Wait 3 to 5 Minutes
The screen might look stuck, but Google is working hard to **Build your App Environment**. Take a coffee break!

- ✅ Success Sign: When you see state: ACTIVE and a Service URL, it’s live!
- 💡 If it asks "(y/N)?", type y and hit Enter.

---

## 📖 Step 5: How to Use Second Brain Joiner 
1. Zip your notes: Compress your Obsidian vault into a ZIP file.
2. Find your "Bucket": 
- Search "Bucket" or "Storage" in the Cloud Console.
- Click on your bucket (e.g., second-brain-joiner-dicon03).
3. Upload & Merge: 
- Drag and drop your ZIP file into the bucket.
- Wait about 10 seconds.
4. Download the Result: 
- Click "Refresh" (or reload your browser).
- Like magic, a file named SecondBrain_Joined_YYYYMMDD.md will appear! 🎉
- Click and Download.

---

## ⚖️ Disclaimer
- Use at your own risk: The developer is not responsible for data loss or cloud usage fees.
- No Warranty: Provided "as-is."
- Backup: Always backup your vault before use.

---

**Sorted & Verified by Second Brain Joiner (AI Architect: Dicon / Hirofumi Inoue)** 


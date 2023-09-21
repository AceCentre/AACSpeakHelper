# Getting keys for Azure or Google

#### Azure TTS

* You first need an Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* [Create a Speech resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) in the Azure portal.
* Your Speech resource key and region. After your Speech resource is deployed, select Go to resource to view and manage keys. For more information about Azure AI services resources, see [Get the keys for your resource](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#get-the-keys-for-your-resource)

#### Google Cloud TTS

Creating a service account for OAuth 2.0 involves generating credentials for a non-human user, often used in server-to-server interactions. Here's how you can create OAuth 2.0 credentials using a service account for Google APIs:

Create a Service Account:

1. Go to the Google Cloud Console: Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a New Project: If you don't already have a project, create a new one in the developer console.
3. Enable APIs: Enable the APIs that your service account will be using. For example, if you're using Google Drive API, enable that API for your project.
4. Create a Service Account:

* In the Google Cloud Console, navigate to "IAM & Admin" > "Service accounts."
* Click on "Create Service Account."
* Enter a name for the service account and an optional description.
* Choose the role for the service account. This determines the permissions it will have.
* Click "Continue" to proceed.

5. Create and Download Credentials:

* On the next screen, you can grant the service account a role in your project. You can also skip this step and grant roles later.
* Click "Create Key" to create and download the JSON key file. This file contains the credentials for your service account.
* Keep this JSON file secure and do not expose it publicly.

6. Use the Service Account Credentials:

* In your code, load the credentials from the JSON key file. The credentials can be used to authenticate and access the APIs on behalf of the service account.

7. Grant Required Permissions:

* If you skipped assigning roles during the service account creation, you can now grant roles to the service account by navigating to "IAM & Admin" > "IAM" and adding the service account's email address with the appropriate roles.

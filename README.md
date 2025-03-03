# ml-deployment
It is an end-to-end ML CI/CD deployment to AWS EC2 instance

# Wrap models in a Flask app for online request
1. Check ```app.py```, which include a template to wrap model predictions.
2. Run ```python app.py``` to check if the online request working locally.
3. Create a Dockerfile which builds a docker image and run the app.py inside.
4. Run docker build -t image_name, the localhost should work.

# Prepare AWS services for deployment
Two services are needed for AWS deployment, ECR for containing the docker image
and EC2 as a remote server where the docker image will run.

1. Create IAM user. Attach the following two policies to the new user. 
   1. AmazonEC2ContainerRegistryFullAccess
   2. AmazonEC2FullAccess
   3. 
    Save the access key csv file where Access key ID and Secret access key are stored.

2. Preparation of ECR. The important thing to remember during creation of ECR
instance is to note down the URI and repository name, which will be used in GitHub.
3. Preparation of EC2. During the creation of EC2 instance, a .pem file will be only
   downloaded once, and need to change its permission as following. 
   1. Linux: chmod 400 the_key_name.pem
   2. Windows: Open a Powershell as admin, then run
       ```
       icacls.exe the_key_name.pem /reset
       icacls.exe the_key_name.pem /grant:r "$($env:username):(r)"
       icacls.exe /inheritance:r
      ```
   Then run the following command to access to the EC2 instance.
    ```
   ssh -i the/path/to/.pem ubuntu@the_public_IPv4_address
   The ubuntu here can be different for other type of virtual machine, e.g., ec2-user, admin, root.
   ```

   Open the created EC2 and install / run the following command for Docker
    ```
            #optinal
        sudo apt-get update -y
        sudo apt-get upgrade
    
        #required
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker ubuntu
        newgrp docker
    ```

# Prepare GitHub and its configurations
1. Setup the SSH keys on GitHub so no username and password are needed for
clone and push repository.
   1. Run the following to generate SSH keys
       ```
      ssh-keygen -t ed25519 -C "your_email@example.com"
      ```
   2. Copy the contents in id_ed25519.pub to SSH Keys configuration.
2. Create a repository and push all the code.
3. Create a self-hosted runner in the actions configuration for the repository.
   Run the following command in the EC2 instance. The last command is to start
   the GitHub runner and wait for listening jobs.
   ```
    # Create a folder
    $ mkdir actions-runner && cd actions-runner
    # Download the latest runner package
    $ curl -o actions-runner-linux-x64-2.322.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-x64-2.322.0.tar.gz
    # Optional: Validate the hash
    $ echo "b13b784808359f31bc79b08a191f5f83757852957dd8fe3dbfcc38202ccf5768  actions-runner-linux-x64-2.322.0.tar.gz" | shasum -a 256 -c
    # Extract the installer
    $ tar xzf ./actions-runner-linux-x64-2.322.0.tar.gz
    # Create the runner and start the configuration experience
    $ ./config.sh --url https://github.com/littletreesmile/ml-deployment --token AHNQB3YEKNMME4WUNMISJHDHYWFKG
    # Last step, run it!
    $ ./run.sh
    ```
4. Configure Actions secrets and variables in the Serects and Variables section. Create the followings
    ````
   AWS_ACCESS_KEY_ID =

    AWS_SECRET_ACCESS_KEY =

    AWS_REGION = 

    AWS_ECR_LOGIN_URI = 

    ECR_REPOSITORY_NAME = 
   ````
   
# CI/CD
When pushing code to the repository, the runner will be running and push docker image to the ECR
and EC2 instance will run the docker container and run the corresponding code.
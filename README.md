# Image Recognition

![AZURE](https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![PYTHON](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![FLASK](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)

Website [here](https://imgrec.azurewebsites.net/)

Video [here](https://www.youtube.com/watch?v=BKOTL1aNSCs)

In this repo a microservise was created to deploy an Azure Web App.
First, I found a good template with CSS and HTML files edit.
Second, I looked for a Pytorch model that recognizes images, for that I used a pre-model built in `torchvision` called ResNet.
The ResNet model is based on the Deep Residual Learning for Image Recognition paper.

## Dockerfile

Something really important to do here is build the Docker within codespaces in github. As Codespaces is also a virtual machine the configuration to work in Azure is more compatile than building and pushin from local.

Commands:

`docker build -t <nameinDockerhub>/<imageName>:<tagName>`

Then, to test it:

`docker run -p 3000:5000 <nameinDockerhub>/<imageName>:<tagName>` I chose 3000 in my local because the port 5000 was already in use.

The you have to push it into Docker hub, to do so you need to login within Codespaces, doing the following:

`docker login -u <nameinDockerhub> -p <TokenGeneratedInDockerHub>`

The you use it in Azure Web Services, important select:

- Linux and not Windows.

- In Publish: Docker Container

In the Docker Sheet:

- Image Source: Docker Hub.
- Image and tag: `<nameinDockerhub>/<imageName>:<tagName>` with no spaces!!!

Finally and also important, in configurations add : "WEBSITES_PORT" value 5000 to match the exit port in the Docker. 

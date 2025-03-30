import os
import subprocess


# GA-2 Q8
def solve_ga_2_q8 ():   #  create_and_push_docker_image
    """Builds, tags, and pushes a Docker image to Docker Hub, returning the image URL."""
    
    # Step 1: Set Docker Hub credentials and repository details
    docker_username = "anantsathe"  # Replace with your Docker Hub username
    docker_repo = "gpt_app"  # Replace with your repository name
    docker_tag = "22f1001679"
    docker_image = f"{docker_username}/{docker_repo}:{docker_tag}"
    docker_hub_url = f"https://hub.docker.com/repository/docker/{docker_username}/{docker_repo}/general"

    # Step 2: Ensure Docker Hub credentials are available
    docker_password = os.getenv("DOCKER_PASSWORD")  # Set this environment variable before running
    if not docker_password:
        return {"error": "Docker password not found. Set DOCKER_PASSWORD as an environment variable."}

    # Step 3: Create a simple Dockerfile
    dockerfile_content = """
    FROM python:3.9-slim
    RUN echo "Hello, Docker Hub!"
    CMD ["echo", "Docker image successfully created!"]
    """

    dockerfile_path = "Dockerfile_ga2_q8"
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)

    # Step 4: Build and tag the Docker image
    subprocess.run(["docker", "build", "-t", docker_image, "-f", dockerfile_path, "."], check=True)

    # Step 5: Log in to Docker Hub
    subprocess.run(["docker", "login", "-u", docker_username, "--password-stdin"], input=docker_password.encode(), check=True)

    # Step 6: Push the image to Docker Hub
    subprocess.run(["docker", "push", docker_image], check=True)

    # Step 7: Return the Docker Hub repository URL
    return {"answer": docker_hub_url}
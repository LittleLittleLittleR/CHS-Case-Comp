# CHS Case Comp Backend

### File Structure
```
backend/
 ├── app/
 │    ├── llm.py
 │    ├── models.py
 │    └── prompts.py
 ├── __init__.py
 ├── main.py
 ├── .venv
 ├── dockerfile
 ├── requirements.txt
 └── README.md
```

### How to run
1. Setting up docker (via docker desktop)
- Install docker desktop: https://docs.docker.com/desktop/setup/install/windows-install/
- Run docker desktop as administrator

1. Setting up docker (via docker engine)
- Install docker engine
```bash
# Install dependencies
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker’s official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

2. Setting up .env
- Make a copy of the .venv in the root folder and rename it to .env
- Fill in the necessary info such as the api key

3. Build and run docker image
```bash
docker build -t chs_backend .
docker run -p 8000:8000 chs_backend
```
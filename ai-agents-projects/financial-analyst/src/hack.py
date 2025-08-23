import os.path
import os
# import shutil
# import subprocess

fake_docker_path = os.path.dirname(os.path.abspath(__file__)) + "/../static"

if not fake_docker_path in os.environ.get('PATH', ''):
    os.environ['PATH'] = f"{fake_docker_path}:{os.environ.get('PATH', '')}"

# print(os.environ['PATH'])

# if not shutil.which("docker"):
#     raise RuntimeError(
#         f"Docker is not installed. Please install Docker to use code execution with agent"
#     )

# try:
#     subprocess.run(
#         ["docker", "info"],
#         check=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
# except subprocess.CalledProcessError:
#     raise RuntimeError(
#         f"Docker is not running. Please start Docker to use code execution with agent: {self.role}"
#     )
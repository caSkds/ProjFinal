import kagglehub

# Download latest version
path = kagglehub.dataset_download("asaniczka/video-game-sales-2024")

print("Path to dataset files:", path)
OLLAMA_URL=http://localhost:11434
PROMPT='"describe the functionalities of org-mode"'
model_list=("qwen3.5:9b" "qwen3.6:latest" "dolphin-mistral:latest" "gemma4:latest" "deepseek-coder:6.7b" "qwen2.5-coder:3b" "qwen2.5-coder:7b")

# Use a for loop to iterate through the list
for model in "${model_list[@]}"; do
    echo "$model"
    echo "$PROMPT"
    python3 benchmark_models.py --model $model --parallel 1 --stream --prompt "describe the functionalities of org-mode" --url $OLLAMA_URL --output data/speed_$model.json
done


write a do loop on all the files in the doc/ folder

#!/bin/bash

# Loop through all files in the 'doc/' directory
for file in doc/*; do
    # Check if it's a regular file and not a directory
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        # Add your code to process each file here
    fi
done

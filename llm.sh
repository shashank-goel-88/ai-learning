set -e
set -x
apt update && sudo apt install pciutils lshw
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > ollama.log 2>&1 &
sleep 10ss
ollama pull gemma3:1b
ollama list

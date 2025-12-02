docker rm -f pwapp 2>/dev/null || true
rm -rf logs run
mkdir -p logs run
docker run \
    --name pwapp \
    --user $(id -u):$(id -g) \
    --init \
    --sig-proxy=true \
    -p 8007:80 \
    -v $(pwd)/..:/var/www/site \
    pwapp:latest

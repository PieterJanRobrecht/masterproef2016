echo "Begin"
docker rmi -f test
echo "Done removing"
pause
echo "Begin building"
docker build -t test .
echo "Done building"
pause
docker run -ti test /bin/bash
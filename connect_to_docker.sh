#!/bin/bash
isSelected=false
while [ -n "$1" ]; do # while loop starts

	case "$1" in

	-p) echo "+-----------------------+"
      echo "|   Connect to Python   |"
      echo "+-----------------------+"
      containerName=pythontests-python-app-1
      isSelected=true
      ;;

	-db) echo "+------------------------+"
      echo "|  Connect to Postgres   |"
      echo "+------------------------+"
      containerName=pythontests-postgres-db-1
      isSelected=true
      ;;
  
  -h)

echo "Usage: ./connect_to_docker.sh [OPTION]"
echo "Connect to a bash terminal of the container specified in OPTION"
echo ""
echo " OPTIONs availables"
echo "-p          python"
echo "-db          postgres"

exit
      ;;
	*) echo "Option $1 not recognized"
  exit;; # In case you typed a different option other than a,b,c

	esac

	shift
done

if ${isSelected}; then
  echo "Opening bash console"
  docker exec --tty --interactive $containerName bash
else
  echo "please specify a container"
fi
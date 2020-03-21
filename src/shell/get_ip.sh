#!/bin/bash
function ip_for_container {
  docker inspect --format "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" "${1}"
}

ip_for_container "${1}"
export HOST=query.comcast.com
export port=4443
exec $SHELL -i

echo -n | openssl s_client -showcerts -connect ${HOST}:${PORT} > ${HOST}.pem
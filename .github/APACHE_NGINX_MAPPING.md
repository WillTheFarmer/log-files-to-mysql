nginx
# NGINX Configuration for files-to-mysql (csv2mysql format)
# Duplicate of Apache csv2mysql: %v,%p,%h,%l,%u,%t,%I,%O,%S,%B,%{ms}T,%D,%^FB,%>s,"%H","%m","%U","%q","%{Referer}i","%{User-Agent}i","%{VARNAME}C",%L

log_format csv2mysql '$host,$server_port,$remote_addr,$remote_user,$remote_user,'
                     '[$time_local],$request_length,$bytes_sent,$upstream_addr,'
                     '$body_bytes_sent,$request_time,$request_time,$upstream_response_time,'
                     '$status,"$server_protocol","$request_method","$uri","$args",'
                     '"$http_referer","$http_user_agent","$cookie_VARNAME",$request_id';

# Use buffering for maximum performance
access_log /var/log/nginx/access_mysql.csv csv2mysql buffer=64k flush=5m;
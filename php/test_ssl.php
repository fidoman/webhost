<?php
$url = "https://stackoverflow.com";
$orignal_parse = parse_url($url, PHP_URL_HOST);
print("host=[".$orignal_parse."]\n");

$get = stream_context_create(array("ssl" => array("capture_peer_cert" => TRUE)));
$read = stream_socket_client("ssl://".$orignal_parse.":443", $errno, $errstr, 30, STREAM_CLIENT_CONNECT, $get);

if (!$read) {
    // ssl connection failed for some reason
    // could be a certificate error or failure to connect on port 443
    echo "Failed to connect to site.  Error {$errno}: {$errstr}\n";
} else {
    $cert = stream_context_get_params($read);
    $certinfo = openssl_x509_parse($cert['options']['ssl']['peer_certificate']);
    var_dump($certinfo);
}
?>

#include <stdlib.h>
#include <stdio.h>
#include <openssl/x509.h>

int main()
{
    const char *dir;

    dir = getenv(X509_get_default_cert_dir_env());

    if (!dir)
        dir = X509_get_default_cert_dir();

    puts(dir);

    return 0;
}

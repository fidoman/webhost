#include <iconv.h>
#include <errno.h>

int main() {
  iconv_t cd;
  cd = iconv_open( "*blahblah*", "*blahblahblah*" );
  if (cd == (iconv_t)(-1)) {
    if (errno == EINVAL) {
      perror("");
      return 0;
  } else {
      return 1;
    }
  }
  iconv_close( cd );
  return 2;
}

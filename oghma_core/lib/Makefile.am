inc=-I../include/
SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_lib.@SLIB_EXT@ $(OBJS)
	ln -s -f ./lib/liboghma_lib.@SLIB_EXT@ ../liboghma_lib.@SLIB_EXT@
	$(CC) -shared -o ../liboghma_core.@DLIB_EXT@ @OGHMA_CORE_LIB_FILES@ @INTERNET_LIB_FOR_CORE@ @LIBS@ @PNG_LIB@ @SRC_DEBUG@
.c.o:
	$(CC) -c @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @I_DBUS@  @DEFINE_CORE@ @INCLUDE_LIBZIP@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib -f

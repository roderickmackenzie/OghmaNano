inc=-I../include/
SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_json.@SLIB_EXT@ $(OBJS)
	ln -s -f ./lib/liboghma_json.@SLIB_EXT@ ../liboghma_json.@SLIB_EXT@

.c.o:
	$(CC) -c $(CPPFLAGS) $(lib_type) @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @DEFINE_CORE@ @INCLUDE_LIBZIP_FOR_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib stk* -f

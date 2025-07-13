inc=-I../include/

SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_rpn.@SLIB_EXT@ $(OBJS)
	ln -s -f ./librpn/liboghma_rpn.@SLIB_EXT@ ../liboghma_rpn.@SLIB_EXT@

.c.o:
	$(CC) -c @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @DEFINE_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib stk* -f

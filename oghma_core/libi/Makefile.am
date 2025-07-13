inc=-I../include/

SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_i.@SLIB_EXT@ $(OBJS)
	ln -s -f ./libi/liboghma_i.@SLIB_EXT@ ../liboghma_i.@SLIB_EXT@
#-cvq

.c.o:
	$(CC) -c @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @DEFINE_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib stk* -f

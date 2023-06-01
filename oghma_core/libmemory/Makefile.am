inc=-I../include/
SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_memory.@SLIB_EXT@ $(OBJS)
	ln -s -f ./libmemory/liboghma_memory.@SLIB_EXT@ ../liboghma_memory.@SLIB_EXT@
#-cvq

.c.o:
	$(CC) -c @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @DEFINE_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib -f

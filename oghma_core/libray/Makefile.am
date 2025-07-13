inc=-I../include/

SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) rcs liboghma_ray.@SLIB_EXT@ $(OBJS)
	ln -s -f ./libray/liboghma_ray.@SLIB_EXT@ ../liboghma_ray.@SLIB_EXT@
#-cvq

.c.o :
	$(CC) -c @SRC_DEBUG@ @COMPILE_FLAG@ @DEFINE_CORE@ $< -o $@  $(inc)

clean:
	rm *.o *.dll *.so *.a *.lib stk* -f

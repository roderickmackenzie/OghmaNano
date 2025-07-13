inc=-I../include/

SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_lua.@SLIB_EXT@ $(OBJS)
	ln -s -f ./liblua/liboghma_lua.@SLIB_EXT@ ../liboghma_lua.@SLIB_EXT@

.c.o:
	$(CC) -c @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @DEFINE_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib stk* -f

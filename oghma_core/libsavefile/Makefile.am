inc=-I../include/
SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

all: $(OBJS)
	$(AR) cr liboghma_savefile.@SLIB_EXT@ $(OBJS)
	ln -s -f ./lib/liboghma_savefile.@SLIB_EXT@ ../liboghma_savefile.@SLIB_EXT@

.c.o:
	$(CC) -c $(CPPFLAGS) $(lib_type) @SRC_DEBUG@ @COMPILE_FLAG@ $(inc) @DEFINE_CORE@ $< -o $@ @INCLUDE_FREETYPE2@ 

clean:
	rm *.o *.dll *.so *.a *.lib stk* -f

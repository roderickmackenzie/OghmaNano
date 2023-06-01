CFLAGS=@SRC_DEBUG@ @COMPILE_FLAG@
inc=-I../include/
OBJS=simplex_contract.o simplex_init.o simplex_shrink.o simplex_dump.o simplex_reflect.o simplex_utils.o simplex_expand.o  simplex_run.o

all: $(OBJS)
#$(CC) -shared $(OBJS) -o liboghma_simplex.@DLIB_EXT@
#ln -s -f ./libsimplex/liboghma_simplex.@DLIB_EXT@ ../liboghma_simplex.@DLIB_EXT@
	$(AR) cr liboghma_simplex.@SLIB_EXT@ $(OBJS)
	ln -s -f ./libsimplex/liboghma_simplex.@SLIB_EXT@ ../liboghma_simplex.@SLIB_EXT@
#-cvq

.c.o:
	$(CC) -c $(CFLAGS) $(inc) @DEFINE_CORE@ $< -o $@ 

clean:
	rm *.o *.dll *.so *.a *.lib -f

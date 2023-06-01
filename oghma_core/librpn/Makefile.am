inc=-I../include/
OBJS=edge.o eval.o function.o opp.o rpn.o stack.o vars.o

CFLAGS=@SRC_DEBUG@ @COMPILE_FLAG@
LINK_FLAG=@LINK_FLAG@

all: $(OBJS)
	$(AR) cr liboghma_rpn.@SLIB_EXT@ $(OBJS)
	ln -s -f ./librpn/liboghma_rpn.@SLIB_EXT@ ../liboghma_rpn.@SLIB_EXT@
#-cvq

.c.o:
	$(CC) -c $(CFLAGS) $(inc) @DEFINE_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib -f

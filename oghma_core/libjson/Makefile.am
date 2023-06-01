CFLAGS=@SRC_DEBUG@ @COMPILE_FLAG@
OBJS=json.o json_search.o json_free.o json_cpy.o json_chk_sum.o json_init.o json_dump.o json_string.o json_find_sim_struct.o

LINK_FLAG=@LINK_FLAG@

inc=-I../include/

all: $(OBJS)
	$(AR) cr liboghma_json.@SLIB_EXT@ $(OBJS)
	ln -s -f ./lib/liboghma_json.@SLIB_EXT@ ../liboghma_json.@SLIB_EXT@

.c.o:
	$(CC) -c $(CPPFLAGS) $(lib_type) $(CFLAGS) $(inc) @DEFINE_CORE@ $< -o $@  

clean:
	rm *.o *.dll *.so *.a *.lib -f

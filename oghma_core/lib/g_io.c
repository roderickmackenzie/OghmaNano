//
// OghmaNano - Organic and hybrid Material Nano Simulation tool
// Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
//
// https://www.oghma-nano.com
// 
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
// SOFTWARE.
// 

/** @file g_strings.c
	@brief Dealing with utf 16 /utf 8
*/

#include <enabled_libs.h>
#include <g_io.h>
#include <string.h>
#include <unistd.h>
#include <oghma_const.h>
#include <util_str.h>

	#include <dlfcn.h>
	#include <sys/types.h>
	#include <sys/stat.h>
	#include <fnmatch.h>
	#include <pthread.h>
	#include <pwd.h>

#include <path_ops.h>
#include <list.h>
//#define do_not_delete


int g_mkdir(char *file_name)
{
	int ret=0;
	if (isdir(file_name) != 0)
	{
			ret=mkdir(file_name, 0700);
	}

	return ret;
}

FILE *g_fopen(char *filename, const char *mode)
{
	FILE *ret;
	ret=fopen(filename,mode);
	if (ret==NULL)
	{
		printf("Can't open file %s\n",filename);
	}
	return ret;
}

char *g_getcwd(char *buf, size_t size)
{
		return getcwd(buf,size);
}


/**
 * @brief Checks if it is a symbolic link
 *
 * Detailed explanation.
 */
int islink(char *file_name)
{
		struct stat statbuf;
		if (lstat(file_name, &statbuf) != 0)
		{
			return 1;
		}else
		{
			if (S_ISLNK(statbuf.st_mode)==0)
			{
				return 1;
			}else
			{
				return 0;
			}
		}
}

/**
 * @brief Tests for a file, returns 0 if found non zero if not.
 *
 * Detailed explanation.
 */
int isfile(char *file_name)
{
		struct stat statbuf;
		if (stat(file_name, &statbuf) != 0)
		{
			return 1;
		}else
		{
			if (S_ISREG(statbuf.st_mode)==0)
			{
				return 1;
			}else
			{
				return 0;
			}
		}
}

/**
 * @brief Tests for a directory, returns 0 if found non zero if not.
 *
 * Detailed explanation.
 */
int isdir(char *path)
{
		struct stat statbuf;
		if (stat(path, &statbuf) != 0)
		{
			return 1;
		}else
		{
			if (S_ISDIR(statbuf.st_mode)==0)
			{
				return 1;
			}else
			{
				return 0;
			}
		}
}

void g_rmfile(char* file_name)
{
	if (isfile(file_name)==0)
	{
		if (islink(file_name)==0)
		{
			return; //I don't delete links
		}

		#ifdef do_not_delete
			printf("I would have removed (g_rmfile): %s<br>\n",file_name);
			return;
		#endif

			remove(file_name);
	}
}

void g_rmdir(char* file_name)
{
	if (isdir(file_name)==0)
	{
		if (islink(file_name)==0)
		{
			return; //I don't delete links
		}
		#ifdef do_not_delete
			printf("I would have removed (g_rmdir): %s<br>\n",file_name);
			return;
		#endif

			remove(file_name);
	}
}

int find_open(struct find_file* find,char* path)
{
	find->first_call=TRUE;
	find->han=NULL;

		find->han = opendir(path);
		if (find->han==NULL)
		{
			return -1;
		}


	return 0;	
}

int find_read(struct find_file* find)
{
	if (find->han==NULL)
	{
		return -1;
	}

		struct dirent *next_file;
		next_file=readdir(find->han);
		if (next_file==NULL)
		{
			return -1;
		}

		strcpy(find->file_name,next_file->d_name);

	return 0;
}

int find_close(struct find_file *find)
{
		if (find->han!=NULL)
		{
			closedir (find->han);
		}

	find->han=NULL;

	return 0;
}

void *g_dlopen(char *filename)
{
	void *ret;
		ret=dlopen(filename, RTLD_LAZY |RTLD_GLOBAL);
		if (!ret)
		{
			return NULL;
		}

		return ret;
}

int g_dlclose(void *handle)
{
	if (handle!=NULL)
	{
			if (dlclose(handle)!=0)
			{
				return -1; 
			}
	
	}

	return 0;
}

void g_usleep(long l_usec)
{

		useconds_t usec=(useconds_t)l_usec;
		usleep(usec);
}

int g_get_max_cpus()
{
	int ret;

		ret=sysconf(_SC_NPROCESSORS_CONF);

	return ret;
}

void* g_dlsym(void *lib_handle,char *function_name)
{
	void *dll_function;
		char *error;
		dll_function = dlsym(lib_handle, function_name);
		if ((error = dlerror()) != NULL)
		{
			return NULL;
		}


	return dll_function;
}


void thread_lock(g_pthread_mutex_t *lock)
{
		pthread_mutex_lock(lock);
}

void thread_unlock(g_pthread_mutex_t *lock)
{
		pthread_mutex_unlock(lock);
}

int running_on_real_windows()
{
	return FALSE;
}

int get_home_dir(char *buffer)
{
		struct passwd *pw = getpwuid(getuid());
		strcpy(buffer,pw->pw_dir);
	printf("user home dir: %s\n",buffer);
	return 0;
}

int get_exe_path(char *buffer)
{
		char temp[PATH_MAX];
		memset(temp, 0, PATH_MAX * sizeof(char));
		int len = readlink("/proc/self/exe", temp, PATH_MAX);
		if (len == -1)
		{
			return -1;
		}
		strcpy(buffer,temp);


	return 0;
}

long get_file_modification_date(char *filename)
{
    	struct stat attr;
    	stat(filename, &attr);
	    return (long)attr.st_mtime;
}

int g_read_file_to_buffer(char **buf, long *len,char *file_name,int max_read)
{
	//#ifndef windows
		int data_read;
		FILE *f = g_fopen(file_name, "rb");
		if (f==NULL)
		{
			return -1;
		}

		fseek(f, 0, SEEK_END);
		*len = ftell(f);
		fseek(f, 0, SEEK_SET);

		if (*len==0)
		{
			fclose(f);
			return -1;
		}

		if (max_read>0)
		{
			if (*len>max_read)
			{
				*len=max_read;
			}
		}

		*buf = malloc(((*len) + 1)*sizeof(char));
		memset(*buf, 0, (*len)*sizeof(char));

		data_read=fread(*buf,  1, *len, f);

		//printf("%d %d %d\n",data_read,*len,data_read!=*len);
		if (data_read!=*len)
		{
			free(*buf);
			fclose(f);
			return -2;
		}

		if (data_read==0)
		{
			free(*buf);
			fclose(f);
			return -1;
		}


		(*buf)[*len]=0;
		fclose(f);
	//#else
		//I could add the windows ReadFile and CreateFile here but not now.
	//#endif
	return 0;
}


long get_file_size(char *filename)
{
    	struct stat attr;
    	if (stat(filename, &attr)!= 0)
		{
			return -1;
		}
	    return (long)attr.st_size;
}

long g_disk_writes()
{
	unsigned int tot=0;
		FILE *file;
		char * line = NULL;
		size_t len = 0;
		int d0;
		int d1;
		char d2[100];
		unsigned int d3;
		file=fopen("/proc/diskstats","r");
		if (file==NULL)
		{
			return -1;
		}

		while (getline(&line, &len, file) != -1)
		{
		    sscanf(line,"%d %d %s %u", &d0, &d1, d2, &d3 );
			//printf("%s %llu\n",line,d3);
			tot+=d3;
		}
		if (line!=NULL)
		{
			free(line);
		}

		fclose(file);
	//printf(">%lu\n",tot);
	return tot;
}

int g_get_mounts(struct list *in)
{
	list_init(in);
	list_malloc(in);

		FILE *file;
		char * line = NULL;
		size_t len = 0;
		char type[PATH_MAX];
		char path[PATH_MAX];
		int show=FALSE;
		file=fopen("/proc/mounts","r");
		if (file==NULL)
		{
			goto end;
		}

		while (getline(&line, &len, file) != -1)
		{
			show=TRUE;
		    sscanf(line,"%s %s", type, path );
			if (str_count(type,"loop")>0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"cgroup")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"run")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"tmpfs")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"securityfs")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"sysfs")==0)
			{
				show=FALSE;
			}else
			if (str_count(type,"fuse")>0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"debugfs")==0)
			{
				show=FALSE;
			}else
			if (str_count(type,"systemd")>0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"proc")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"udev")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"devpts")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"pstore")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"bpf")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"hugetlbfs")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"tracefs")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"binfmt_misc")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"configfs")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"nsfs")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(path,"/boot/")==0)
			{
				show=FALSE;
			}else
			if (strcmp_begin(type,"mqueue")==0)
			{
				show=FALSE;
			}

			if (show==TRUE)
			{
				list_add(in,path);
			}
		}

		if (line!=NULL)
		{
			free(line);
		}

		fclose(file);
	end:
	return 0;
}


void cpu_usage_init(struct cpu_usage *in)
{
	in->work_jiffies0=-1;
	in->total_jiffies0=-1;

	in->work_jiffies1=-1;
	in->total_jiffies1=-1;

	in->percent=0;
};

int cpu_usage_get(struct cpu_usage *in)
{
	double dwork;
	double dtotal;
		FILE *file;
		char * line = NULL;
		size_t len = 0;
		char cpu[20];
		int d0=0;
		int d1=0;
		int d2=0;
		int d3=0;
		int d4=0;
		int d5=0;
		int d6=0;
		file=fopen("/proc/stat","r");
		if (file==NULL)
		{
			return -1;
		}

		if (getline(&line, &len, file) != -1)
		{
			//printf("%s\n",line);
			sscanf(line,"%s %d %d %d %d %d %d %d", cpu, &d0,&d1,&d2,&d3,&d4,&d5,&d6);
		}

		if (line!=NULL)
		{
			free(line);
		}
		fclose(file);

		in->work_jiffies0=(double)(d0+d1+d2);
		in->total_jiffies0=(double)(d0+d1+d2+d3+d4+d5+d6);

	dwork=in->work_jiffies0-in->work_jiffies1;
	dtotal=in->total_jiffies0-in->total_jiffies1;

	//printf("d0: %lf %lf\n",in->work_jiffies1,in->work_jiffies0);
	//printf("d1: %lf %lf\n",in->total_jiffies1,in->total_jiffies0);
	//printf("d2: %lf %lf\n",dwork,dtotal);

	if (dtotal==0.0)
	{
		//printf("exit\n");
		return 0;
	}

	in->percent=(int)(100.0*dwork/dtotal);
	//printf("inside: %d\n",in->percent);

	if (in->percent>100.0)
	{
		in->percent=100.0;
	}else
	if (in->percent<0.0)
	{
		in->percent=0.0;
	}

	if (in->work_jiffies1==-1)
	{
		in->percent=0;
	}
	in->work_jiffies1=in->work_jiffies0;
	in->total_jiffies1=in->total_jiffies0;


	return 0;
}


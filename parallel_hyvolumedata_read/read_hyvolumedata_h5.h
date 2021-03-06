#ifndef READ_HYVOLUMEDATA_H5_H
#define READ_HYVOLUMEDATA_H5_H 

#include "sds.h"

/* This file was automatically generated.  Do not edit! */
void destroy_file_list(sds *file_list,int num);
void print_file_list(sds *file_list,int num);
void get_file_list(sds *file_list);
sds *init_file_list(int num);
int get_number_of_h5_files();
double *hyvolumedata_read_dataset(const char *file_name,const char *group_name,const char *dataset_name,int *size, int* extents);
int match(const char *string,const char *pattern);


#endif

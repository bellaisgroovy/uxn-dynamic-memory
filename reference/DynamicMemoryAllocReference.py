#!/usr/bin/env python3

# Dynamic memory allocation using pages and a bitmap

# We allocate 16 bytes per page
PAGE_SZ = 16 # in bytes
# We have a total of 256 pages, so we can allocate at most 4kB
N_PAGES = 1024>>2 
VMEM_START = 64*1024-PAGE_SZ*N_PAGES

# N_PAGES bits, packed in bytes mean N_PAGES/8 entries, so with the above, the bitmap will take 64 bytes
# 0 means free
bitmap = [0] * (N_PAGES>>3)

# Takes the number of bytes to be allocated
# returns a pointer, i.e. the address of the start of the allocated memory region
def malloc(n_bytes) :
    if n_bytes==0:
        return 0
    n_pages = ((n_bytes-1) // PAGE_SZ) + 1 # integer division
    for idx in range(N_PAGES): # 0 .. N_PAGES-1
        if alloc_sz_is_free_at_idx(idx, n_pages):
            claim_alloc_sz_at_idx(idx, n_pages)
            return (idx*PAGE_SZ+VMEM_START)
    return 0 # Null pointer

def free(ptr,n_bytes) :
    idx = (ptr-VMEM_START)/PAGE_SZ
    free_alloc_sz_at_idx(idx, n_bytes)

# returns 1 if bit at idx is full, returns 0 if bit is empty
def get_bit(idx) : # idx is the index of the bit we want in memory (which represents a page)
    byte_idx = idx >> 3 # byte idx is the index of the byte we want in memory (when memory is split into bytes) (idx/8)
    bit_idx = 7 - (idx - (byte_idx<<3)) # 7 - (idx%8)
    if byte_idx > N_PAGES-1: # exit if out of range
        print("Outside of page range: ", byte_idx)
        exit(0)
    byte = bitmap[byte_idx] # load in value of byte we want
    # if byte is None:
    #     print("Invalid access:", byte_idx)
    #     exit(0)
    bit = (byte >> bit_idx) & 0x01 # move bit we want to 1st position and trim everything else
    return bit # return value of that bit

def set_bit(idx) :
    byte_idx = idx >> 3
    bit_idx = 7 - idx + (byte_idx<<3)
    byte = bitmap[byte_idx]
    bitmap[byte_idx] = byte | mask_set(bit_idx)

def mask_set(bit_idx):
    return (1 << bit_idx)

def clear_bit(idx) :
    byte_idx = idx >> 3
    bit_idx = 7 - idx + (byte_idx<<3) # 7 - (idx%8)
    byte = bitmap[byte_idx]
    # mask = 0xFF ^ (1 << bit_idx) # 1110111
    bitmap[byte_idx] = byte & mask_clear(bit_idx)

def mask_clear(bit_idx):
    return (0xFF ^ (1 << bit_idx))

# allocation size is in pages
def alloc_sz_is_free_at_idx(idx, alloc_sz) :
    for jj in range(alloc_sz) : # for page 
        if(idx+jj>N_PAGES-1): # surely less efficient than if idx+alloc_sz > n_pages-1?
            return 0 
        if (get_bit(idx+jj)==1): # if bit is allocated 
            return 0 
    return 1 # if in range and free then

# allocation size is in pages
def claim_alloc_sz_at_idx(idx, alloc_sz) : 
    for jj in range(alloc_sz):
        set_bit(idx+jj)

# allocation size is in pages
def free_alloc_sz_at_idx(idx, alloc_sz) : 
    for jj in range(alloc_sz):
        clear_bit(idx+jj)



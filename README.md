# Single C++ Header Creator
This script merges a top-level `C++` header file (together with all its sub-headers) into a single file. Useful for merging multiple headers into one (for easier distribution).<br>

Script to be run with Python `3.x`.

---

### Usage
Run the following command in the console:
```
python create_single_cpp_header.py
  --file FILE,       -f FILE     Input cpp/hpp file
  --include INCLUDE, -i INCLUDE  (Optional) Include path
  --output OUTPUT,   -o OUTPUT   (Optional) Output file path
  --nocomments,      -nc         (Optional) Comments will be filtered if flag is provided
```
Examples:
```
python create_single_cpp_header.py -f C:\project\my_project.hpp
python create_single_cpp_header.py -f C:\project\my_project.hpp -o C:\project\my_project_merged.hpp --nocomments
```

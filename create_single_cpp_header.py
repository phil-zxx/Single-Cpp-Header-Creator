import argparse
import os
import re


def create_single_header(file_name, include_paths, no_comments):
    includes_done      = []
    top_level_includes = []

    def create_single_header_impl(file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if line in includes_done:
                lines[i] = ''
            elif line.startswith('#include'):
                in_file_name = line.replace('#include ','').replace('#include',''). \
                                    replace('<','').replace('>','').replace('"','').replace('\n','')
                any_include_found = False
                for in_path in include_paths:
                    if os.path.exists(os.path.join(in_path, in_file_name)):
                        includes_done.append(line)
                        lines[i] = create_single_header_impl(os.path.join(in_path, in_file_name))
                        any_include_found = True
                        break
                if any_include_found == False:
                    lines[i] = ''
                    if line not in top_level_includes:
                        top_level_includes.append(line)
            elif line.startswith('#pragma once'):
                if line not in top_level_includes:
                    top_level_includes.append(line)
                lines[i] = ''

        return ''.join(lines)
    
    print('  Merging all files')
    header_content = create_single_header_impl(file_name)
    total_content  = ''.join(top_level_includes) + '\n' + header_content

    if no_comments:
        print('  Removing all comments')
        total_content = re.sub(r"//(.+?)\n",   '\n', total_content, flags=re.S)
        total_content = re.sub(r"/\*(.+?)\*/", '',   total_content, flags=re.S)
    
    while '\n\n\n' in total_content:
        total_content = total_content.replace('\n\n\n','\n\n')

    return total_content


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f",        required=True,  help="Input cpp/hpp file", ) 
    parser.add_argument("--include", "-i",     required=False, help="(Optional) Include path")
    parser.add_argument("--output", "-o",      required=False, help="(Optional) Output file path")
    parser.add_argument("--nocomments", "-nc", required=False, help="(Optional) Comments will be filtered if flag is provided", action='store_true')
    args = parser.parse_args()

    input_file = args.file
    print("  Using input file = %s" % input_file)

    include_paths = [os.path.dirname(input_file)]
    if args.include:
        include_paths.append(args.include)
    print("  Using include paths = %s" % include_paths)

    c = create_single_header(input_file, include_paths, args.nocomments)

    if not args.output:
        output_file = os.path.join(os.path.dirname(input_file), 'out_'+os.path.basename(input_file))
    else:
        output_file = args.output
    
    with open(output_file, 'w') as f:
        f.write(c)
    print('  Outfile saved under = %s' % output_file)
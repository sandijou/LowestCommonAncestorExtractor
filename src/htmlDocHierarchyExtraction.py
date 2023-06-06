from threading import Thread
import os
import json
import urllib.parse
from selenium import webdriver
import logging


def tree_to_string(node, depth=0):
    """
    Function to convert a tree structure to a string format. 

    Args:
        node: The node in the tree structure.
        depth: The depth of the node in the tree structure.

    Returns:
        A string representation of the node and its children.
    """
    indent = '#' * depth if isinstance(node, BlockNode) else ''
    if isinstance(node, BlockNode):
        result = f'\n{indent} {node.headline}'
        for child in node.children:
            result += tree_to_string(child, depth + 1)
    else:
        result = f'\n{node.text}\n'
    return result


def process_file(filename, sess_driver): 
    """
    Function to process a given file, extract the HTML, parse it and write the parsed output to a file.

    Args:
        filename: The name of the file to process.
        sess_driver: The Selenium webdriver instance.

    Returns:
        None
    """
    basename = os.path.basename(filename).split('.')[0]
    input_file = os.path.join(input_dir, filename)
    output_file = os.path.join(output_dir, f'{basename}_LCAextrHierar{os.path.splitext(filename)[1]}')
    #processed_files = set()

    with open(input_file, encoding='utf8') as f_in, open(output_file, 'a', encoding='utf8') as f_out:
        print(f"Processing {input_file}")
        
        # Load Document and Identifier (one per Line)
        for i, line in enumerate(f_in):
            obj = json.loads(line)
            slug = obj.get('slug', 'slug_not_defined_' + str(obj.get('id', '')))
            cleaned_html = obj.get('cleaned_html', '')
            
            # Extract hierarchy by Common Formatting
            ## Load the body content into the WebDriver
            link = "data:text/html;charset=utf-8," + urllib.parse.quote(cleaned_html, safe='')
            sess_driver.get(link)
            
            # Parse the body content
            body_node = parse_tree(sess_driver, extract_style=True)
            #body_node.tag = 'body'
            #body_node.xpath = '/html/body'
            
            # Transform bodyNode into hierarchy blocks
            hierarchyTree = extractHierarchy(bodyNode, ContentExtractor.RenderedStyle)
            text_with_extracted_hierarchy = tree_to_string(hierarchy_tree)
            
            out_obj = {'slug': slug, 'textWithExtractedHierarchy': text_with_extracted_hierarchy}
            f_out.write(json.dumps(out_obj) + '\n')
            
            #processed_files.add(slug)

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} lines...")
        logging.info(f"Finished processing {filename}")
        

def process_directory(input_dir, output_dir, use_multiprocessing=False):
    """
    Function to process all files in a directory.

    Args:
        input_dir: The directory where the input files are located.
        output_dir: The directory where the processed files are to be saved.
        use_multiprocessing: A flag indicating whether multiprocessing is to be used or not.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    filenames = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir) if filename.endswith('.jsonl')]

    sess_driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
    
    if use_multiprocessing:
        threads = []
        for filename in filenames:
            thread = Thread(target=process_file, args=(filename, sess_driver,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
    else:
        for filename in filenames:
            process_file(filename, sess_driver)

    sess_driver.close()
    logging.info("Done processing directory.")

    
# pass directory containing jsonl files with one html string per line in the field 'cleaned_html' 
#input_dir = ""
#output_dir = ""

# Toggle multiprocessing ON/OFF
#process_directory(input_dir, output_dir, use_multiprocessing=True)
    
    
    
    '''# Use the basename of the file to identify the respective output file
    toCheck_processed_file = f'/kaggle/input/v3lcaeoutput1-3/processingOutput/{basename}_LCAextractedTextHierarchy.jsonl'
    
    if os.path.exists(toCheck_processed_file):
        # Append the pre-processed output file to the new output path
        with open(output_file, 'a', encoding='utf8') as f_out_new, open(toCheck_processed_file, 'r', encoding='utf8') as f_out_old:
            for line in f_out_old:
                out_obj = json.loads(line)
                slug = out_obj.get('slug', 'slug_not_defined_' + str(out_obj.get('id', '')))
                processed_slugs.add(slug)
                f_out_new.write(line)'''
    ## INSERT HERE
    #with open(input_file, encoding='utf8') as f_in, open(output_file, 'a', encoding='utf8') as f_out:
        #print(f"Processing {input_file}")

        #for i, line in enumerate(f_in):
            #obj = json.loads(line)
            #slug = obj.get('slug', 'slug_not_defined_' + str(obj.get('id', '')))

            '''if slug in processed_slugs1:
                print(f'slug already done: {slug}\n')
                continue'''
            
            #cleaned_html = obj.get('cleaned_html', '')

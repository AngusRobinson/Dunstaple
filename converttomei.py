import os
from verovio import toolkit

def convert_mxl_to_mei(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialize Verovio toolkit
    vrvToolkit = toolkit()

    # Iterate over all MXL files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.mxl'):
            input_path = os.path.join(input_directory, file_name)
            output_path = os.path.join(output_directory, file_name.replace('.mxl', '.mei'))

            # Load the MXL file
            if vrvToolkit.loadFile(input_path):
                # Convert and save as MEI
                mei_data = vrvToolkit.getMEI(True)  # True to include the MEI header
                with open(output_path, 'w') as mei_file:
                    mei_file.write(mei_data)
                print(f'Converted: {file_name} to MEI')
            else:
                print(f'Failed to convert: {file_name}')

# Usage
input_directory = 'corpus/bach'  # Replace with your MXL files directory path
output_directory = 'corpus/bach/mei_versions'  # Replace with your desired output path
convert_mxl_to_mei(input_directory, output_directory)


import os
import csv
from lxml import etree
from pathlib import Path
import glob
from dotenv import load_dotenv

def parse_to_csv(date_str):
    # Set up base directory paths
    BASE_DIR = Path(os.getenv('BASE_DIR'))
    XML_DIR = BASE_DIR / date_str / "xml"
    XSL_DIR = BASE_DIR / date_str / "dmd_xsl"
    CSV_DIR = BASE_DIR / date_str / "csv"

    # Table structure CSV is in the same directory as this script
    TABLE_STRUCTURE_CSV = Path(__file__).resolve().parent / "table_structure.csv"

    # Ensure CSV directory exists
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    def format_csv_field(field):
        if field is None:
            return ''
        field = str(field).strip()
        if '"' in field:
            field = field.replace('"', '""')
            return f'"{field}"'
        elif '|' in field or ',' in field or '\n' in field:
            return f'"{field}"'
        return field

    def transform_xml_to_csv(xml_file, xsl_file, csv_file):
        # Load XML and XSL files
        xml_doc = etree.parse(str(xml_file))
        xsl_doc = etree.parse(str(xsl_file))

        # Create XSLT transformer
        transform = etree.XSLT(xsl_doc)

        # Apply transformation
        result = transform(xml_doc)

        # Convert result to CSV
        csv_content = str(result).strip().split('\n')
        with open(csv_file, 'w', newline='') as f:
            for row in csv_content:
                f.write(row + '\n')

    def process_gtin():
        gtin_paths = list(XML_DIR.glob("f_gtin2_*.xml"))
        assert len(gtin_paths) == 1
        gtin_xml_file = gtin_paths[0]

        gtin_xslt = etree.fromstring(
            """
            <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
                <xsl:output method="xml" indent="yes"/>

                <xsl:template match="/GTIN_DETAILS">
                    <GTINS_DETAILS>
                        <GTINS>
                            <xsl:apply-templates select="AMPPS/AMPP/GTINDATA"/>
                        </GTINS>
                    </GTINS_DETAILS>
                </xsl:template>

                <xsl:template match="GTINDATA">
                    <GTIN>
                        <GTIN><xsl:value-of select="GTIN" /></GTIN>
                        <APPID><xsl:value-of select="../AMPPID" /></APPID>
                        <STARTDT><xsl:value-of select="STARTDT" /></STARTDT>
                        <ENDDT><xsl:value-of select="ENDDT" /></ENDDT>
                    </GTIN>
                </xsl:template>
            </xsl:stylesheet>
            """
        )
        gtin_transform = etree.XSLT(gtin_xslt)

        # Load and transform GTIN XML
        with open(gtin_xml_file, 'rb') as f:
            gtin_doc = etree.parse(f)
        gtin_result = gtin_transform(gtin_doc)

        # Save transformed GTIN data to CSV
        gtin_csv_file = CSV_DIR / "f_gtin.csv"
        with open(gtin_csv_file, 'w', newline='') as f:
            for gtin_element in gtin_result.xpath('//GTIN'):
                appid = gtin_element.findtext('APPID')
                gtin = gtin_element.findtext('GTIN')
                startdt = gtin_element.findtext('STARTDT')
                enddt = gtin_element.findtext('ENDDT') or ''

                if appid and gtin and startdt:  # Only write non-empty rows
                    f.write(f"{appid}|{gtin}|{startdt}|{enddt}|\n")

        print(f"Processed {gtin_xml_file.name} to create {gtin_csv_file.name}")

    def process_files():
        # Define the XML to XSL mappings
        mappings = [
            ("f_amp2_3", ["f_amp_AmpType", "f_amp_ApiType",
             "f_amp_LicRouteType", "f_amp_AppProdInfoType"]),
            ("f_ampp2_3", ["f_ampp_AmppType", "f_ampp_PackInfoType", "f_ampp_ContentType",
             "f_ampp_PrescInfoType", "f_ampp_PriceInfoType", "f_ampp_ReimbInfoType"]),
            ("f_vtm2_3", ["f_vtm"]),
            ("f_ingredient2_3", ["f_ingredient"]),
            ("f_lookup2_3", [
                ("f_lookup_CombPackIndInfoType", "f_lookup_CombPackIndInfoType"),
                ("f_lookup_CombProdIndInfoType", "f_lookup_CombProdIndInfoType"),
                ("f_lookup_BasisOfNameInfoType", "f_lookup_BasisOfNameInfoType"),
                ("f_lookup_NamechangeReasonInfoType", "f_lookup_NamechangeReasonInfoType"),
                ("f_lookup_VirProdPresStatInfoType", "f_lookup_VirProdPresStatInfoType"),
                ("f_lookup_ControlDrugCatInfoType", "f_lookup_ControlDrugCatInfoType"),

                # Note the different names for f_lookup_LicAuthInfoType

                ("f_lookup_LicAuthInfoType", "f_lookup_LicAuthIndInfoType"),
                ("f_lookup_UoMHistoryInfoType", "f_lookup_UoMHistoryInfoType"),
                ("f_lookup_FormHistoryInfoType", "f_lookup_FormHistoryInfoType"),
                ("f_lookup_OntFormRouteInfoType", "f_lookup_OntFormRouteInfoType"),
                ("f_lookup_RouteHistoryInfoType", "f_lookup_RouteHistoryInfoType"),
                ("f_lookup_DtPayCatInfoType", "f_lookup_DtPayCatInfoType"),
                ("f_lookup_SupplierSupplierInfoType", "f_lookup_SupplierSupplierInfoType"),
                ("f_lookup_FlavourInfoType", "f_lookup_FlavourInfoType"),
                ("f_lookup_ColourInfoType", "f_lookup_ColourInfoType"),
                ("f_lookup_BasisOfStrengthInfoType", "f_lookup_BasisOfStrengthInfoType"),
                ("f_lookup_ReimbStatInfoType", "f_lookup_ReimbStatInfoType"),
                ("f_lookup_SpecContInfoType", "f_lookup_SpecContInfoType"),
                ("f_lookup_VirProdNoAvailInfoType", "f_lookup_VirProdNoAvailInfoType"),
                ("f_lookup_DiscIndInfoType", "f_lookup_DiscIndInfoType"),
                ("f_lookup_DfIndInfoType", "f_lookup_DfIndInfoType"),
                ("f_lookup_PriceBasisInfoType", "f_lookup_PriceBasisInfoType"),
                ("f_lookup_LegalCatInfoType", "f_lookup_LegalCatInfoType"),
                ("f_lookup_AvailRestrictInfoType", "f_lookup_AvailRestrictInfoType"),
                ("f_lookup_LicAuthChgRsnInfoType", "f_lookup_LicAuthChgRsnInfoType"),
                ("f_lookup_DNDInfoType", "f_lookup_DNDInfoType")
            ]),
            ("f_vmp2_3", ["f_vmp_VmpType", "f_vmp_VpiType", "f_vmp_OntDrugFormType",
             "f_vmp_DrugFormType", "f_vmp_DrugRouteType", "f_vmp_ControlInfoType"]),
            ("f_vmpp2_3", ["f_vmpp_VmppType",
             "f_vmpp_DtInfoType", "f_vmpp_ContentType"])
        ]

        # Process each mapping
        for xml_prefix, xsl_list in mappings:
            xml_files = list(XML_DIR.glob(f"{xml_prefix}*.xml"))
            if xml_files:
                xml_file = xml_files[0]  # Use the first matching XML file
                for xsl_item in xsl_list:
                    if isinstance(xsl_item, tuple):
                        xsl_name, csv_name = xsl_item
                    else:
                        xsl_name = csv_name = xsl_item
                    xsl_file = XSL_DIR / f"{xsl_name}.xsl"
                    csv_file = CSV_DIR / f"{csv_name}.csv"
                    transform_xml_to_csv(xml_file, xsl_file, csv_file)
                    print(
                        f"Processed {xml_file.name} with {xsl_file.name} to create {csv_file.name}")

        # Process BNF files
        bnf_mappings = [
            ("f_bnf_Amp", "f_bnf_Amp"),
            ("f_bnf_Vmp", "f_bnf_Vmp")
        ]

        bnf_xml_files = list(XML_DIR.glob("f_bnf1_0*.xml"))
        if bnf_xml_files:
            bnf_xml_file = bnf_xml_files[0]  # Use the first matching BNF XML file
            for xsl_name, csv_name in bnf_mappings:
                xsl_file = XSL_DIR / f"{xsl_name}.xsl"
                csv_file = CSV_DIR / f"{csv_name}.csv"
                transform_xml_to_csv(bnf_xml_file, xsl_file, csv_file)
                print(
                    f"Processed {bnf_xml_file.name} with {xsl_file.name} to create {csv_file.name}")

        # Add GTIN processing
        process_gtin()

    process_files()

    def add_headers_to_csv():
        # Read the table structure
        table_structure = {}
        with open(TABLE_STRUCTURE_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # "desc" is a really unhelpful field name if you're writing SQl (as openprescribing have described it)
                # Replace 'desc' with 'descr' in the headers
                headers = [h.replace('desc', 'descr') for h in row['headings'].split('|')]
                table_structure[row['filename']] = headers

        # Process each file in the directory
        for filename in os.listdir(CSV_DIR):
            if filename.endswith('.csv'):
                # Find the corresponding entry in table_structure
                base_filename = os.path.splitext(filename)[0]
                if base_filename in table_structure:
                    file_path = CSV_DIR / filename
                    temp_file_path = CSV_DIR / f"temp_{filename}"

                    # Read the original file and write to a new file with headers
                    with open(file_path, 'r') as original_file, open(temp_file_path, 'w', newline='') as temp_file:
                        # Use '|' as the delimiter
                        reader = csv.reader(original_file, delimiter='|')
                        writer = csv.writer(temp_file, delimiter='|')

                        # Write the header
                        writer.writerow(table_structure[base_filename])

                        # Write the rest of the data
                        for row in reader:
                            writer.writerow(row)

                    # Replace the original file with the new file
                    os.replace(temp_file_path, file_path)
                    print(f"Added headers to {filename}")
                else:
                    print(f"No header information found for {filename}")

        print("Header addition complete.")

    # Call the new function to add headers
    add_headers_to_csv()

    def modify_csv(filename, columns_to_modify, true_value='1', false_value='0'):
        file_path = CSV_DIR / filename
        if not file_path.exists():
            print(f"{filename} not found. Skipping modification.")
            return

        temp_file_path = CSV_DIR / f"temp_{filename}"

        with open(file_path, 'r', newline='') as original_file, open(temp_file_path, 'w', newline='') as temp_file:
            reader = csv.reader(original_file, delimiter='|')
            writer = csv.writer(temp_file, delimiter='|',
                                quoting=csv.QUOTE_NONE, quotechar=None, escapechar=None)

            header = next(reader)
            writer.writerow(header)

            column_indices = {}
            for col in columns_to_modify:
                try:
                    column_indices[col] = header.index(col)
                except ValueError:
                    print(f"'{col}' column not found in {filename}. Skipping this column.")

            for row in reader:
                for col, index in column_indices.items():
                    if index < len(row):
                        if columns_to_modify[col] == '0001':
                            row[index] = true_value if row[index] == '0001' else false_value
                        else:
                            row[index] = true_value if row[index] == true_value else false_value
                writer.writerow(row)

        os.replace(temp_file_path, file_path)
        print(
            f"Modified {filename}: Updated columns {', '.join(columns_to_modify.keys())}")

    # Define the files and their columns to modify
    files_to_modify = {
        'f_ingredient.csv': {'invalid': '1'},
        'f_lookup_SupplierSupplierInfoType.csv': {'invalid': '1'},
        'f_vtm.csv': {'invalid': '1'},
        'f_vmp_VmpType.csv': {'invalid': '1', 'sug_f': '0001', 'glu_f': '0001', 'pres_f': '0001', 'cfc_f': '0001'},
        'f_vmpp_VmppType.csv': {'invalid': '1'},
        'f_amp_AmpType.csv': {'invalid': '1', 'ema': '0001', 'parallel_import': '0001'},
        'f_ampp_AmppType.csv': {'invalid': '1'},
        'f_ampp_PrescInfoType.csv': {
            'sched_2': '0001', 'acbs': '0001', 'padm': '0001', 'fp10_mda': '0001', 'sched_1': '0001',
            'hosp': '0001', 'nurse_f': '0001', 'enurse_f': '0001', 'dent_f': '0001'
        },
        'f_ampp_ReimbInfoType.csv': {'bb': '0001', 'ltd_stab': '0001', 'cal_pack': '0001', 'fp34d': '0001'}
    }

    # Process each file
    for filename, columns in files_to_modify.items():
        modify_csv(filename, columns)

    print("All specified CSV files have been processed.")

    def add_extra_delimiter(csv_dir, files_to_modify):

        # Add an extra delimiter at the end of each row for specified CSV files.

        # This function is used to prepare the CSV files for future BNF code mapping.
        # By adding an extra delimiter, we create a placeholder for the BNF code
        # that will be added in a later step of the process. This ensures that the
        # file structure is ready for the BNF code addition without requiring
        # significant restructuring later.

        # Args:
        # csv_dir (Path): Directory containing the CSV files
        # files_to_modify (list): List of CSV filenames to modify

        for filename in files_to_modify:
            file_path = csv_dir / filename
            if not file_path.exists():
                print(f"{filename} not found. Skipping modification.")
                continue

            temp_file_path = csv_dir / f"temp_{filename}"

            with open(file_path, 'r', newline='') as original_file, open(temp_file_path, 'w', newline='') as temp_file:
                reader = csv.reader(original_file, delimiter='|')
                writer = csv.writer(temp_file, delimiter='|')

                # Write the header row without modification
                header = next(reader)
                writer.writerow(header)

                # Process the rest of the rows
                for row in reader:
                    writer.writerow(row + [''])  # Add an empty field at the end

            # Replace the original file with the modified file
            temp_file_path.replace(file_path)
            print(f"Added extra delimiter to {filename}")

    files_to_mitigate_bnf_code_delimeter = [
        'f_vmp_VmpType.csv',
        'f_vmpp_VmppType.csv',
        'f_amp_AmpType.csv',
        'f_ampp_AmppType.csv'
    ]
    add_extra_delimiter(CSV_DIR, files_to_mitigate_bnf_code_delimeter)


    def add_id_column(csv_files):
        for filename in csv_files:
            file_path = CSV_DIR / filename
            if not file_path.exists():
                print(f"{filename} not found. Skipping.")
                continue

            temp_file_path = CSV_DIR / f"temp_{filename}"

            with open(file_path, 'r', newline='') as original_file, open(temp_file_path, 'w', newline='') as temp_file:
                reader = csv.reader(original_file, delimiter='|')
                writer = csv.writer(temp_file, delimiter='|')

                # Read and modify the header
                header = next(reader)
                new_header = ['id'] + header
                writer.writerow(new_header)

                # Process the rest of the rows
                for id, row in enumerate(reader, start=1):
                    new_row = [str(id)] + row
                    writer.writerow(new_row)

            # Replace the original file with the modified file
            os.replace(temp_file_path, file_path)
            print(f"Added ID column to {filename}")

    # List of files to modify
    files_to_modify = [
        'f_vmp_VmpType.csv',
        'f_vmp_VpiType.csv',
        'f_vmp_ControlInfoType.csv',
        'f_vmp_DrugFormType.csv',
        'f_vmp_DrugRouteType.csv',
        'f_vmp_OntDrugFormType.csv',
        'f_vmpp_VmppType.csv',
        'f_vmpp_ContentType.csv',
        'f_vmpp_DtInfoType.csv',
        'f_amp_AmpType.csv',
        'f_amp_ApiType.csv',
        'f_amp_AppProdInfoType.csv',
        'f_amp_LicRouteType.csv',
        'f_ampp_AmppType.csv',
        'f_ampp_ContentType.csv',
        'f_ampp_PackInfoType.csv',
        'f_ampp_PrescInfoType.csv',
        'f_ampp_PriceInfoType.csv',
        'f_ampp_ReimbInfoType.csv',
        'f_gtin.csv'
    ]

    # Call the function to add ID columns
    add_id_column(files_to_modify)

    print("ID columns have been added to all specified CSV files.")

    # def remove_extra_delimiter_reimbinfo(csv_dir):
    #     filename = 'f_ampp_ReimbInfoType.csv'
    #     file_path = csv_dir / filename
    #     if not file_path.exists():
    #         print(f"{filename} not found. Skipping modification.")
    #         return

    #     temp_file_path = csv_dir / f"temp_{filename}"

    #     with open(file_path, 'r', newline='') as original_file, open(temp_file_path, 'w', newline='') as temp_file:
    #         # Read and write the header without modification
    #         header = original_file.readline()
    #         temp_file.write(header)

    #         # Process the rest of the lines
    #         for line in original_file:
    #             # Remove the last delimiter if it's empty
    #             parts = line.rstrip().split('|')
    #             if parts[-1] == '':
    #                 parts = parts[:-1]
    #             new_line = '|'.join(parts) + '\n'
    #             temp_file.write(new_line)

    #     # Replace the original file with the modified file
    #     os.replace(temp_file_path, file_path)
    #     print(f"Removed extra delimiter from {filename}")

    # # Usage
    # remove_extra_delimiter_reimbinfo(CSV_DIR)


    def perform_csv_substitutions(csv_dir, substitution_rules):
        """
        Perform substitutions in CSV files based on the provided rules.
        Skip rows where a value is not found in the source, but print those rows.
        Ensure only existing fields are written to the output file.

        Args:
        csv_dir (Path): Directory containing the CSV files
        substitution_rules (list): List of dictionaries, each containing:
            - 'target_file': The file to modify
            - 'source_file': The file to get substitution values from
            - 'substitutions': List of dictionaries, each containing:
                - 'target_column': Column in target file to substitute
                - 'source_column': Column in source file to match
                - 'value_column': Column in source file to get new value from
        """
        for rule in substitution_rules:
            target_file = csv_dir / rule['target_file']
            source_file = csv_dir / rule['source_file']
            
            # Read source file into memory
            source_data = {}
            with open(source_file, 'r', newline='') as f:
                reader = csv.DictReader(f, delimiter='|')
                for row in reader:
                    for sub in rule['substitutions']:
                        source_data.setdefault(sub['source_column'], {})[row[sub['source_column']]] = row[sub['value_column']]
            
            # Process target file
            temp_file = csv_dir / f"temp_{rule['target_file']}"
            with open(target_file, 'r', newline='') as input_file, open(temp_file, 'w', newline='') as output_file:
                reader = csv.DictReader(input_file, delimiter='|')
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter='|')
                
                writer.writeheader()
                for row in reader:
                    skip_row = False
                    for sub in rule['substitutions']:
                        if row[sub['target_column']] not in source_data[sub['source_column']]:
                            print(f"Skipping row (value not found in source): {row}")
                            skip_row = True
                            break
                        else:
                            new_value = source_data[sub['source_column']][row[sub['target_column']]]
                            if sub['target_column'] not in fieldnames:
                                print(f"Warning: Field '{sub['target_column']}' not in original CSV. Skipping this substitution.")
                            else:
                                row[sub['target_column']] = new_value
                    
                    if not skip_row:
                        # Only write fields that exist in the original CSV
                        writer.writerow({k: v for k, v in row.items() if k in fieldnames})
            
            # Replace original file with modified file
            temp_file.replace(target_file)
            print(f"Substitutions completed for {rule['target_file']}")
    # Define the substitution rules
    substitution_rules = [
        {
            'target_file': 'f_vmp_VpiType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmp_ControlInfoType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmp_DrugFormType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmp_DrugRouteType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmp_OntDrugFormType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmpp_VmppType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmpp_ContentType.csv',
            'source_file': 'f_vmpp_VmppType.csv',
            'substitutions': [
                {
                    'target_column': 'prntvppid',
                    'source_column': 'vppid',
                    'value_column': 'id'
                },
                {
                    'target_column': 'childvppid',
                    'source_column': 'vppid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_vmpp_DtInfoType.csv',
            'source_file': 'f_vmpp_VmppType.csv',
            'substitutions': [
                {
                    'target_column': 'vppid',
                    'source_column': 'vppid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_amp_AmpType.csv',
            'source_file': 'f_vmp_VmpType.csv',
            'substitutions': [
                {
                    'target_column': 'vpid',
                    'source_column': 'vpid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_amp_ApiType.csv',
            'source_file': 'f_amp_AmpType.csv',
            'substitutions': [
                {
                    'target_column': 'apid',
                    'source_column': 'apid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_amp_AppProdInfoType.csv',
            'source_file': 'f_amp_AmpType.csv',
            'substitutions': [
                {
                    'target_column': 'apid',
                    'source_column': 'apid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_amp_LicRouteType.csv',
            'source_file': 'f_amp_AmpType.csv',
            'substitutions': [
                {
                    'target_column': 'apid',
                    'source_column': 'apid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_AmppType.csv',
            'source_file': 'f_vmpp_VmppType.csv',
            'substitutions': [
                {
                    'target_column': 'vppid',
                    'source_column': 'vppid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_AmppType.csv',
            'source_file': 'f_amp_AmpType.csv',
            'substitutions': [
                {
                    'target_column': 'apid',
                    'source_column': 'apid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_ContentType.csv',
            'source_file': 'f_ampp_AmppType.csv',
            'substitutions': [
                {
                    'target_column': 'prntappid',
                    'source_column': 'appid',
                    'value_column': 'id'
                },
                 {
                    'target_column': 'childappid',
                    'source_column': 'appid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_PackInfoType.csv',
            'source_file': 'f_ampp_AmppType.csv',
            'substitutions': [
                {
                    'target_column': 'appid',
                    'source_column': 'appid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_PrescInfoType.csv',
            'source_file': 'f_ampp_AmppType.csv',
            'substitutions': [
                {
                    'target_column': 'appid',
                    'source_column': 'appid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_PriceInfoType.csv',
            'source_file': 'f_ampp_AmppType.csv',
            'substitutions': [
                {
                    'target_column': 'appid',
                    'source_column': 'appid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_ampp_ReimbInfoType.csv',
            'source_file': 'f_ampp_AmppType.csv',
            'substitutions': [
                {
                    'target_column': 'appid',
                    'source_column': 'appid',
                    'value_column': 'id'
                }
            ]
        },
        {
            'target_file': 'f_gtin.csv',
            'source_file': 'f_ampp_AmppType.csv',
            'substitutions': [
                {
                    'target_column': 'amppid',
                    'source_column': 'appid',
                    'value_column': 'id'
                }
            ]
        },
    ]

    # Perform the substitutions
    perform_csv_substitutions(CSV_DIR, substitution_rules)

    print("All CSV substitutions have been completed.")

if __name__ == "__main__":
    # This block will only run if the script is executed directly
    # For testing purposes, you can uncomment the line below:
    parse_to_csv("2024_09_02")
    pass

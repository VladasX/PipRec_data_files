import json
import urllib.request
import dis

# Extract imports
def extract_imports(input_file, output_file):
    # Load data
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Load PyPI packages
    with open("data/pypi.csv", 'r') as f:
        f.readline()
        pypi = f.read().splitlines()

    pypi = set(pypi) # Convert to set for O(1) complexity when checking membership

    result = {}
    project_count = len(data.keys())
    counter = 0

    for key, value in data.items():
        # Store imports in a set to avoid duplicates
        import_list = set()
        
        # Loop through each python file
        for url in value:
            # Convert to raw link
            url = url.split('/')
            del url[5]
            url = url[3:]
            url = "/".join(url)
            
            try:
                # Get the code
                with urllib.request.urlopen("https://raw.githubusercontent.com/" + url) as response:
                    code = response.read()
                    code = code.decode("utf8")
                
                # Get imports
                instructions = dis.get_instructions(code)
                imports = [__ for __ in instructions if "IMPORT" in __.opname]
                for instr in imports:
                    if instr.opname == "IMPORT_NAME":
                        if instr.argval in pypi:
                            import_list.add(instr.argval)
            except:
                # Invalid code found or HTTP error
                pass
                        
        # Save results as a list for json                
        result[key] = list(import_list)

        # This can take a while for large projects
        counter += 1
        print("{}/{} done".format(counter, project_count))

    # Save extracted imports
    with open(output_file, 'w') as outfile:
        json.dump(result, outfile)

if __name__ == "__main__":
    extract_imports("data/urls.json", "data/imports.json")

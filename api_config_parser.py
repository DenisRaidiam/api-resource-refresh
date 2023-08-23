import json


def main():
    # Open the JSON file and load the data
    with open('api_config.json') as f:
        data = json.load(f)

    # Initialize an empty list to store the names
    names = []

    # Iterate over each object in the JSON data
    for obj in data:
        # Check if the 'conformanceTest' field is set to true
        if obj.get('conformanceTest') == True:
            # If it is, add the 'name' field to the list
            names.append(obj['name'])

    # Print the final list
    print(names)


if __name__ == '__main__':
    main()

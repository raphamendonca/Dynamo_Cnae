import os
import sys, getopt


"""
aws dynamodb batch-write-item --request-items file://atividadeEconomica4.json --endpoint-url http://localhost:8000 --region local
"""

command = "aws dynamodb batch-write-item --request-items file://%s --endpoint-url http://%s --region %s"

def carrega_jsons():
    files = []
    for file in os.listdir():
        if file.endswith(".json"):
            files.append(os.path.join( file))
    files.sort()
    return files

def main(argv):
    #json_file = 'atividadeEconomica.json'
    aws_url = 'localhost:8000'
    aws_region = 'local'

    try:
        #opts, args = getopt.getopt(argv,"hf:u:r:",["file=","url=", "region="])
        opts, args = getopt.getopt(argv,"hu:r:",["url=", "region="])
    except getopt.GetoptError:
        #print ('xls_to_dynamodb_json.py -f <file> -u <url> -r <region>') 
        print ('xls_to_dynamodb_json.py -u <url> -r <region>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            #print ('xls_to_dynamodb_json.py -f <file> -u <url> -r <region>')
            print ('xls_to_dynamodb_json.py -u <url> -r <region>')
            sys.exit()
        #elif opt in ("-f", "--file"):
        #    json_file = arg
        elif opt in ("-u", "--url"):
            aws_url = arg
        elif opt in ("-r", "--region"):
            aws_region = arg

    print("")
    print("The command below will be executed in: %s at region %s the input of requests in file: %s" % (aws_url, aws_region, "file.json"))
    print(command)
    print("")
    text = input("Want to execute the command to every .json file in the folder? [y/n]  ") 
    if text == 'y':
        print("......")
        files = carrega_jsons()
        for json_file in files:
            #print(command % (json_file, aws_url, aws_region))
            os.system(command % (json_file, aws_url, aws_region))
            print("End of file %s" % json_file)
        print("Done")
        print("Processed %s files" % len(files))

if __name__ == "__main__":
   main(sys.argv[1:])
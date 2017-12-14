import uuid
import json
import datetime
import os


# CREATE DUMP FILE

def time_stamp():
    time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    return time

def init_file(name, job_id):
    # Initialize File
    current_dir = os.path.dirname(os.path.abspath(__file__)) #<-- absolute dir the script is in
    rel_name = "data/data-{}-{}.json".format(time_stamp(), name)
    data_file = os.path.join(current_dir, rel_name)

    data_root = {
        "job_id": job_id,
        "data": []
    }

    with open(data_file, 'w+') as f:
        json.dump(data_root, f)
    print("file {} initialized: {}".format(name, job_id))
    return data_file

def write_error(name, job_id, error_obj):
    # Handle ERROR
    error_file = "error/error-{}.txt".format(job_id)
    with open(error_file, 'wb') as f:
        f.write(error_obj)
    print("error report at {}. job: {}".format(time_stamp(), job_id))
    return error_file

def read_file(data_file):
    with open(data_file) as f:
        data = json.load(f)
    return data

def read_write(data_file, payload):
    # READ DATA
    working_file = read_file(data_file)
    data = working_file['data']
    data.append(payload)
    working_file['data'] = data
    # WRITE DATA
    with open(data_file, 'w') as f:
        json.dump(working_file, f)
    return data_file

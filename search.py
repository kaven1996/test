import json

# 从文件加载 JSON 数据
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 处理 JSON 数据
def process_json(data, cpu, device):
    if device in data:
        device_data = data[device]
        if cpu in device_data and 'cpu' in device_data[cpu]:
            print(f"CPU: {cpu}, Device: {device}")
            for model, precisions in device_data[cpu].items():
                print(f"Model: {model}, Precisions: {', '.join(precisions)}")
        elif cpu in device_data and 'gpu' in device_data[cpu]:
            print(f"GPU: {cpu}, Device: {device}")
            for model, precisions in device_data[cpu].items():
                print(f"Model: {model}, Precisions: {', '.join(precisions)}")
    else:
        print("Device not found in data")

# 加载 JSON 文件
json_data = {
    "19-14900k": {
        "cpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        },
        "gpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        }
    },
    "19-13900k": {
        "cpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        },
        "gpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        }
    }
}

# 输入参数
cpu_input = "cpu"
device_input = "19-13900k"

# 处理 JSON 数据
process_json(json_data, cpu_input, device_input)


import json

# 从文件加载 JSON 数据
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 处理 JSON 数据
def process_json(data, cpu_gpu, device):
    if device in data:
        device_data = data[device]
        if cpu_gpu.startswith('cpu'):
            device_type = "CPU"
        elif cpu_gpu.startswith('gpu'):
            device_type = "GPU"
        else:
            print("Invalid device prefix")
            return

        if cpu_gpu.endswith('.1'):
            cpu_gpu_prefix = cpu_gpu.split('.')[0]
            if cpu_gpu_prefix in device_data:
                device_data = device_data[cpu_gpu_prefix]
                if 'cpu' in device_data:
                    print(f"{device_type}: {device}, Device: {cpu_gpu_prefix}")
                    for model, precisions in device_data['cpu'].items():
                        print(f"Model: {model}, Precisions: {', '.join(precisions)}")
                elif 'gpu' in device_data:
                    print(f"{device_type}: {device}, Device: {cpu_gpu_prefix}")
                    for model, precisions in device_data['gpu'].items():
                        print(f"Model: {model}, Precisions: {', '.join(precisions)}")
            else:
                print(f"{device_type} not found in data")
        else:
            print("Invalid index, only 1 is supported")
    else:
        print("Device not found in data")

# 加载 JSON 文件
json_data = {
    "19-14900k": {
        "cpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        },
        "gpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        }
    },
    "19-13900k": {
        "cpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        },
        "gpu": {
            "bloomz": ["fp16", "int8", "int4"],
            "chat": ["fp16", "int8", "int4"]
        }
    }
}

# 输入参数
cpu_gpu_input = "cpu.1"
device_input = "19-13900k"

# 处理 JSON 数据
process_json(json_data, cpu_gpu_input, device_input)
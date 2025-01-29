def print_dict(obj):
    # obj = vars(settings)
    print(f"Key value pairs:")
    for key, val in obj.items():
        if "__" not in key:
            print(f" > '{key}' > '{val}'")
    
    return 

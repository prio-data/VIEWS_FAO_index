def get_percentiles(option):
    if option == 'Default':
        return ['90', '95', '98', '99']
    
    elif option == 'User defined':
        user_input = input("Enter a comma-separated list of values (e.g., 90,95,98): ")
        user_values = [value.strip() for value in user_input.split(',')]
        return user_values
    
    elif option == 'All values':
        lst = [str(i) for i in range(1, 96)] + [str(i / 2) for i in range(191, 201)]

        cleaned_percentiles = [str(int(float(p))) if p.endswith('.0') else p for p in lst]
        return cleaned_percentiles
    
    else:
        raise ValueError("Invalid option. Choose from 'Default', 'User defined', or 'All Values'.")
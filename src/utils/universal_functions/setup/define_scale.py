def select_scale(unique_countries_list):
    print("Available countries:")
    for country in unique_countries_list:
        print(country)

    print("\nOptions:")
    print("1. Enter 'Global' to analyze all data as one entity.")
    print("2. Enter one or more country names separated by commas.")
    print("3. Enter 'Process all countries' to analyze each country individually.")

    user_input = input("\nSelect an option: ").strip()

    if user_input.lower() == 'global':
        return ['Global']
    elif user_input.lower() == 'process all countries':
        return unique_countries_list
    else:
        selected_countries = [country.strip() for country in user_input.split(',') if country.strip()]
        valid_countries = [country for country in selected_countries if country in unique_countries_list]

        if not valid_countries:
            raise ValueError("Invalid selection. Please choose valid country names from the list, 'Global', or 'Process all countries'.")
        
        return valid_countries

from urllib.parse import urlparse

def parse_jdbc_url(jdbc_url: str) -> dict:
    """
    Parse a JDBC URL and return connection parameters.
    
    Args:
        jdbc_url: JDBC URL string (e.g., jdbc:postgresql://host:port/dbname)
        
    Returns:
        Dictionary containing connection parameters
    """
    if jdbc_url.startswith('jdbc:postgresql://'):
        jdbc_url = jdbc_url.replace('jdbc:postgresql://', 'postgresql://')
    
    parsed_url = urlparse(jdbc_url)
    return {
        'dbname': parsed_url.path.lstrip('/'),
        'user': parsed_url.username or 'postgres',
        'password': parsed_url.password or 'postgres',
        'host': parsed_url.hostname,
        'port': parsed_url.port or '5432'
    }

def convert_patient_data(patient_dict: dict) -> dict:
    """
    Convert patient data types and prepare for database insertion.
    
    Args:
        patient_dict: Dictionary containing patient data
        
    Returns:
        Dictionary with converted data types
    """
    type_conversions = {
        'age': float,
        'weight': float,
        'platelets': float,
        'spo2': float,
        'creatinine': float,
        'hematocrit': float,
        'heartrate': float,
        'calcium': float,
        'wbc': float,
        'glucose': float,
        'inr': float,
        'potassium': float,
        'sodium': float,
        'ethnicity': int
    }
    
    for field, converter in type_conversions.items():
        if field in patient_dict:
            patient_dict[field] = converter(patient_dict[field])
    
    return patient_dict

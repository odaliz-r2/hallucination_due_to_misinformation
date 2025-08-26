import pandas as pd

def filter_little_known_etnias(input_csv, output_csv, pop_threshold=10000):
    """
    Filtra etnias poco conocidas del dataset de Joshua Project.
    Criterios: Population < pop_threshold y LeastReached == 'Y'.
    Guarda el resultado en un nuevo CSV y muestra el conteo.
    """
    # Lee el CSV con low_memory=False para evitar DtypeWarning
    df = pd.read_csv(input_csv, low_memory=False)
    
    # Imprime las columnas para depuración
    print("Columnas en el CSV:", df.columns.tolist())
    
    # Verifica que las columnas necesarias existan
    required_columns = ['PeopNameInCountry', 'Population', 'LeastReached']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"¡Error! La columna '{col}' no está en el CSV. Columnas disponibles: {df.columns.tolist()}")
    
    # Filtra etnias poco conocidas
    # Convierte PopInCountry a numérico, manejando errores
    df['Population'] = pd.to_numeric(df['Population'], errors='coerce')
    filtered_df = df[(df['Population'] < pop_threshold) & (df['LeastReached'] == 'Y')]
    
    # Elimina duplicados por 'PeopNameInCountry' para evitar repeticiones
    filtered_df = filtered_df.drop_duplicates(subset=['PeopNameInCountry'])
    
    # Guarda en nuevo CSV
    filtered_df.to_csv(output_csv, index=False)
    
    # Muestra el número
    num_etnias = len(filtered_df)
    print(f"¡Se encontraron {num_etnias} etnias poco conocidas!")
    print(f"Archivo guardado en: {output_csv}")
    print(f"Criterios usados: Population < {pop_threshold} y LeastReached == 'Y'")
    
    return num_etnias

# Ejemplo de uso: Cambia las rutas si es necesario
if __name__ == "__main__":
    input_csv = 'AllPeoplesInCountry.csv'  # Tu CSV completo
    output_csv = 'etnias_poco_conocidas.csv'  # Nuevo archivo
    try:
        filter_little_known_etnias(input_csv, output_csv)
    except KeyError as e:
        print(e)
    except FileNotFoundError:
        print(f"¡Error! El archivo {input_csv} no se encuentra. Asegúrate de que esté en el directorio correcto.")
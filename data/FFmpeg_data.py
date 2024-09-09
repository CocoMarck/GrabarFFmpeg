import sys, os

# Obtén la ruta al directorio actual del script
current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )

# Construye la ruta a Languages desde el directorio que contiene el módulo
dir_data = os.path.join(current_dir, 'resources')

# Archivo de registro de configuraciónes
cfg_file = os.path.join( dir_data, 'FFmpeg_cfg.txt' )
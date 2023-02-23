import os
import shutil

#diretório
root_dir = os.path.abspath(r'/mnt/share/')

#nome das pastas a copiar
dirs_to_copy = ['AguasClaras', 'Apuã', 'Bandeirantes2', 'Bandeirantes', 'BoaEsperanca', 'Boa Esperanca', 'CerroTigre', 'Orquideas', 'Floresta', 'Gallo', 'GoiasVerde', 'GranjaSobrado', 'Guaiba', 'Jotabasso', '492', 'IrmaosBueno', 'PontalDaSerra', 'Verdura', 'RioGalhao', 'Rio Galhao', 'RioGalhão', 'RioVerdinho', 'BarraGrande', 'SantaAngélica', 'SantaAngelica', 'SantoAntônio', 'Santo Antônio', 'ParaísoRioPreto', 'ParaisoRioPreto', 'SãoFrancisco', 'Sao Francisco', 'SaoFranciscoOriente', 'SãoFranciscoOriente', 'SãoFranciscoDeSales', 'SaoFranciscoDeSales', 'SaoFranciscoSales', 'SãoTomaz', 'Sao Tomaz', 'TresIrmaos','Tres Irmaos', 'VacaBranca']

#destino
destination_dir = os.path.abspath(r'/home/guilherme/Documents/Fazendas Legado/')

for dirpath, dirnames, files in os.walk(root_dir):
    for src_dir in [os.path.join(dirpath, dirname) for dirname in dirnames if dirname in dirs_to_copy]:
        index = 0
        while True:
            dst_dir = os.path.join(destination_dir, f'{os.path.basename(src_dir)}_{index}')
            if os.path.exists(dst_dir):
                index += 1
            else:
                try:
                    shutil.copytree(src_dir, dst_dir)
                except (IOError, shutil.Error) as e:
                    print(f"Error copying {src_dir} to {dst_dir}: {e}")
                else:
                    print(f'Copied {src_dir} to {dst_dir}')
                break
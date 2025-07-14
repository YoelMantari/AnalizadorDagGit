import subprocess
import json
import math

class analizador_dag:
    def __init__(self):
        # diccionario para guardar commits
        self.commits = {}
        # diccionario para guardar padres de cada commit
        self.padres = {}
        
    def obtener_commits_git(self, repo_path):
        # obtiene commits usando git rev-list
        try:
            cmd = ["git", "rev-list", "--all", "--parents"]
            resultado = subprocess.check_output(cmd, cwd=repo_path, text=True)
            lineas = resultado.strip().split('\n')
            
            # procesa cada linea de salida
            for linea in lineas:
                if linea:
                    partes = linea.split()
                    commit = partes[0]
                    padres_commit = partes[1:] if len(partes) > 1 else []
                    
                    # guarda commit y sus padres
                    self.commits[commit] = True
                    self.padres[commit] = padres_commit
                    
        except subprocess.CalledProcessError:
            return False
        return True
            
    def calcular_densidad_ramas(self):
        # densidad simple = numero nodos / niveles maximos
        if not self.commits:
            return 0
        
        # cuenta niveles del grafo
        max_nivel = 0
        for commit in self.commits:
            nivel = len(self.padres.get(commit, []))
            if nivel > max_nivel:
                max_nivel = nivel
                
        num_nodos = len(self.commits)
        densidad = num_nodos / (max_nivel + 1) if max_nivel >= 0 else 0
        return densidad
        
    def calcular_path_critico(self, head_commit, tag_commit):
        # path simple entre dos commits
        if head_commit not in self.commits or tag_commit not in self.commits:
            return []
        
        # busca camino simple
        path = [head_commit]
        actual = head_commit
        
        # recorre hasta encontrar destino
        while actual != tag_commit and len(path) < 10:
            padres = self.padres.get(actual, [])
            if not padres:
                break
            actual = padres[0]  # toma primer padre
            path.append(actual)
            
        return path
        
    def calcular_entropia(self):
        # cuenta merges y fast forwards
        merges = 0
        fast_forwards = 0
        
        for commit in self.commits:
            num_padres = len(self.padres.get(commit, []))
            if num_padres > 1:
                merges += 1  # es merge
            elif num_padres == 1:
                fast_forwards += 1  # es fast forward
                
        total = merges + fast_forwards
        if total == 0:
            return 0
        
        # calcula probabilidades
        p_merge = merges / total
        p_ff = fast_forwards / total
        
        # formula de entropia
        entropia = 0
        if p_merge > 0:
            entropia -= p_merge * math.log2(p_merge)
        if p_ff > 0:
            entropia -= p_ff * math.log2(p_ff)
            
        return entropia
        
    def analizar_repositorio(self, repo_path):
        # funcion principal que hace todo el analisis
        if not self.obtener_commits_git(repo_path):
            return None
        
        # calcula las tres metricas
        densidad = self.calcular_densidad_ramas()
        entropia = self.calcular_entropia()
        
        # toma primer y ultimo commit para path
        commits_lista = list(self.commits.keys())
        head_commit = commits_lista[0] if commits_lista else ""
        tag_commit = commits_lista[-1] if len(commits_lista) > 1 else head_commit
        path_critico = self.calcular_path_critico(head_commit, tag_commit)
        
        # arma resultado final
        metricas = {
            "densidad_ramas": densidad,
            "entropia_historia": entropia,
            "path_critico": path_critico,
            "total_commits": len(self.commits)
        }
        
        return metricas
        
    def exportar_json(self, metricas, archivo_salida):
        # guarda metricas en archivo json
        with open(archivo_salida, 'w') as f:
            json.dump(metricas, f, indent=2)

def main():
    # funcion principal para ejecutar desde terminal
    import sys
    if len(sys.argv) < 2:
        print("uso: python graph_analysis.py <repo_path>")
        return
        
    repo_path = sys.argv[1]
    analizador = analizador_dag()
    metricas = analizador.analizar_repositorio(repo_path)
    
    if metricas:
        analizador.exportar_json(metricas, "metricas.json")
        print("analisis completado - archivo: metricas.json")
        print("densidad:", metricas["densidad_ramas"])
        print("entropia:", metricas["entropia_historia"])
    else:
        print("error analizando repositorio")

if __name__ == "__main__":
    main()
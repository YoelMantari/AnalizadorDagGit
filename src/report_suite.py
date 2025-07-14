import json

class commit_stats_service:
    def __init__(self, json_reader):
        # inyeccion de dependencia
        self.json_reader = json_reader
        
    def calcular_estadisticas(self, json_path):
        # lee metricas y calcula stats
        data = self.json_reader.leer(json_path)
        return {
            "total_commits": data.get("total_commits", 0),
            "densidad": round(data.get("densidad_ramas", 0), 2),
            "entropia": round(data.get("entropia_historia", 0), 2)
        }

class release_notes_service:
    def __init__(self, git_client):
        # inyeccion de dependencia
        self.git_client = git_client
        
    def extraer_notas(self, tag1, tag2):
        # extrae notas entre tags
        commits = self.git_client.obtener_commits()
        return [f"- {commit}" for commit in commits]

class changelog_writer:
    def __init__(self, notes_service):
        # composition: reutiliza notes service
        self.notes_service = notes_service
        
    def generar_markdown(self, stats, notas):
        # genera markdown con las 3 secciones requeridas
        md = "# reporte dag\n\n"
        md += "## estadisticas\n\n"
        md += f"total commits: {stats['total_commits']}\n"
        md += f"densidad: {stats['densidad']}\n"
        md += f"entropia: {stats['entropia']}\n\n"
        md += "## release notas\n\n"
        for nota in notas:
            md += f"{nota}\n"
        md += "\n## changelog\n\n"
        md += "cambios en esta version\n"
        return md

class json_reader:
    def leer(self, path):
        with open(path, 'r') as f:
            return json.load(f)

class git_client:
    def obtener_commits(self):
        return ["commit 1", "commit 2"]

class reporting_suite:
    def __init__(self):
        # facade que inicializa servicios
        reader = json_reader()
        git = git_client()
        self.stats = commit_stats_service(reader)
        self.notes = release_notes_service(git)
        self.writer = changelog_writer(self.notes)
        
    def generate_report(self, json_path, formato="markdown"):
        # metodo principal facade
        stats = self.stats.calcular_estadisticas(json_path)
        notas = self.notes.extraer_notas("v1.0", "v2.0")
        contenido = self.writer.generar_markdown(stats, notas)
        
        archivo = "reporte.md"
        with open(archivo, 'w') as f:
            f.write(contenido)
        return archivo

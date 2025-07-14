#!/bin/bash

# builder pattern para generar reportes

step_init() {
    echo "iniciando analisis de grafo..."
    cd "$(dirname "$0")/.."
    python src/graph_analysis.py --repo . --output metrics.json
    echo "metricas guardadas en metrics.json"
}

step_report() {
    echo "generando reporte..."
    python -c "
import sys
sys.path.append('src')
from report_suite import *

# crea servicios
stats_service = commit_stats_service(read_json_file)
notes_service = release_notes_service()
writer = changelog_writer(notes_service)

# crea facade y genera reporte
suite = reporting_suite(stats_service, notes_service, writer)
output_file = suite.generate_report('metrics.json', 'markdown')
print(f'reporte generado: {output_file}')
"
    echo "reporte guardado en reporte.md"
}

step_preview() {
    echo "mostrando reporte..."
    if [ -f "reporte.md" ]; then
        less reporte.md
    else
        echo "no se encontro reporte.md"
    fi
}

main() {
    step_init
    step_report
    step_preview
}

main
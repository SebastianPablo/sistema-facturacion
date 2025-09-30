#!/usr/bin/env python
"""
Script para backup automático de la base de datos.
"""

import os
import subprocess
import datetime
from pathlib import Path
import zipfile

def create_backup():
    """Crear backup de la base de datos."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Nombre del archivo de backup
    backup_file = backup_dir / f"facturacion_backup_{timestamp}.sql"
    
    print(f"🔄 Creando backup: {backup_file}")
    
    try:
        # Comando para backup de PostgreSQL
        cmd = [
            'pg_dump',
            '-h', 'localhost',
            '-U', 'facturacion_user',
            '-d', 'facturacion_db',
            '-f', str(backup_file)
        ]
        
        # Ejecutar backup
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Backup creado exitosamente: {backup_file}")
            
            # Comprimir backup
            compress_backup(backup_file)
            
            # Limpiar backups antiguos
            cleanup_old_backups(backup_dir)
            
        else:
            print(f"❌ Error en backup: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error creando backup: {e}")

def compress_backup(backup_file):
    """Comprimir archivo de backup."""
    zip_file = backup_file.with_suffix('.zip')
    
    print(f"🗜️  Comprimiendo backup: {zip_file}")
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(backup_file, backup_file.name)
    
    # Eliminar archivo original
    backup_file.unlink()
    
    print(f"✅ Backup comprimido: {zip_file}")

def cleanup_old_backups(backup_dir, keep_days=30):
    """Limpiar backups antiguos."""
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
    
    print(f"🧹 Limpiando backups anteriores a {cutoff_date.strftime('%Y-%m-%d')}")
    
    deleted_count = 0
    for backup_file in backup_dir.glob("facturacion_backup_*.zip"):
        file_time = datetime.datetime.fromtimestamp(backup_file.stat().st_mtime)
        
        if file_time < cutoff_date:
            backup_file.unlink()
            deleted_count += 1
            print(f"🗑️  Eliminado: {backup_file.name}")
    
    print(f"✅ {deleted_count} backups antiguos eliminados")

def restore_backup(backup_file):
    """Restaurar backup de la base de datos."""
    print(f"🔄 Restaurando backup: {backup_file}")
    
    try:
        # Comando para restaurar backup
        cmd = [
            'psql',
            '-h', 'localhost',
            '-U', 'facturacion_user',
            '-d', 'facturacion_db',
            '-f', str(backup_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Backup restaurado exitosamente")
        else:
            print(f"❌ Error restaurando backup: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error restaurando backup: {e}")

def list_backups():
    """Listar backups disponibles."""
    backup_dir = Path('backups')
    
    if not backup_dir.exists():
        print("❌ No hay directorio de backups")
        return
    
    backups = list(backup_dir.glob("facturacion_backup_*.zip"))
    
    if not backups:
        print("❌ No hay backups disponibles")
        return
    
    print("📋 Backups disponibles:")
    for backup in sorted(backups, reverse=True):
        file_time = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
        size_mb = backup.stat().st_size / (1024 * 1024)
        print(f"  📄 {backup.name} ({size_mb:.1f} MB) - {file_time.strftime('%Y-%m-%d %H:%M')}")

def main():
    """Función principal."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create':
            create_backup()
        elif command == 'list':
            list_backups()
        elif command == 'restore' and len(sys.argv) > 2:
            backup_file = Path(sys.argv[2])
            if backup_file.exists():
                restore_backup(backup_file)
            else:
                print(f"❌ Archivo no encontrado: {backup_file}")
        else:
            print("❌ Comando no válido")
    else:
        print("🗄️  Sistema de Backup - Base de Datos")
        print("\nComandos disponibles:")
        print("  python backup_database.py create    - Crear backup")
        print("  python backup_database.py list       - Listar backups")
        print("  python backup_database.py restore <archivo> - Restaurar backup")

if __name__ == "__main__":
    main()

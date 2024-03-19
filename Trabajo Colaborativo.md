----------
# Comandos útiles para trabajo colaborativo en Git  

### Crear y gestionar ramas Crear una nueva rama 
```bash
git switch -c "nombre-de-la-rama"
```
### Cambiarse a una rama existente
```bash
git switch "nombre-de-la-rama"`
```
### Listar todas las ramas
```bash
git branch
```
### Eliminar una rama (local)
```bash
git branch -d <nombre-de-la-rama>
```
### Eliminar una rama (forzar, útil si la rama no se fusionó)
```bash
git branch -D <nombre-de-la-rama>
```
### Fusionar una rama a la rama actual
```bash
git merge <nombre-de-la-rama>
```
### Rebase de una rama
```bash
git rebase <nombre-de-la-rama>
```

# Comparar ramas

### Ver cambios entre dos ramas
```bash
git diff <rama-origen> <rama-destino>
```

# Trabajo colaborativo

### Obtener cambios del repositorio remoto
```bash
git fetch
```
### Obtener y fusionar cambios del repositorio remoto
```bash
git pull
```
### Subir cambios a una rama
```bash
git push -u origin nombre-de-la-rama
```
### Eliminar una rama del repositorio remoto
```bash
git push origin --delete <nombre-de-la-rama>
```
### Ver ramas remotas
```bash
git remote show origin
```
### Ver seguimiento de ramas remotas
```bash
git branch -vv
```
## Otras operaciones

### Cambiar nombre de una rama
```bash
git branch -m <nombre-antiguo> <nombre-nuevo>
```
### Deshacer cambios en una rama específica
```bash
git reset --hard HEAD
```
### Ver historial de cambios de una rama
```bash
git log <nombre-de-la-rama>
```
### Ver cambios de una rama específica
```bash
git log <rama-origen>..<rama-destino>
```
### Ver los cambios en el directorio de trabajo
```bash
git status
```

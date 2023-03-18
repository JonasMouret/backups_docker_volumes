### Backup Docker Volumes:

# How to :

### To execute the script
```
./main -v path/where/to/save/backups
```

This script is build for backup volume create with [Caprover](https://caprover.com/)
As you could see in the code :
```python
if not volume.name.startswith("captain--"):
	# Skip docker volumes if not started with captain--
	continue
```

- If you want to backup all the volumes please fell free to remove this line.

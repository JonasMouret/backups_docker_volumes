import docker
import tarfile
import os
import datetime
import argparse
import logging


def backup_volume(volume):
    for volume in volumes:
        print(volume.name)
        if not client.images.list(name="ubuntu"):
            # If it does not exist, pull it
            client.images.pull("ubuntu")

        if not volume.name.startswith("captain--"):
            # Skip docker volumes if not started with captain--
            continue
        try:
            container = client.containers.create(
                'ubuntu',
                'tail -f /dev/null',
                volumes={volume.name: {'bind': '/mnt', 'mode': 'ro'}},
                hostname='backup_container'
            )
            container.start()
            archive, stat = container.get_archive('/mnt')
            with open(f'{volume_path}{volume.name}${now}.tar', 'wb') as f:
                for chunk in archive:
                    f.write(chunk)
            container.stop()
            container.remove()
        except docker.errors.APIError as e:
            print(f"Error backing up volume {volume.name}: {e}")


if __name__ == '__main__':
    client = docker.from_env()
    volumes = client.volumes.list()
    version = "1.0.0"

    parser = argparse.ArgumentParser(description=f"MoBo Backups Volumes Docker - version {version}")
    parser.add_argument("-v", "--source", help="Folder where to save backups volumes ", default="backups_volumes_docker", required=True, type=str, const="volume_path", nargs='?')
    date = datetime.datetime.now()
    now = date.strftime("%Y%m%d_%H%M%S")
    folder = f"{date.strftime('%Y%m%d_%H%M%S')}_backup_caprover"
    volume_path = f"{parser.parse_args().source}/{folder}/"

    if not os.path.exists(volume_path):
        os.makedirs(volume_path)

    backup_volume(volumes)



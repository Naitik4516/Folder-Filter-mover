# Folder Filter Mover

The Folder Filter Mover project provides two Python scripts, `main.py` and `main2.py`, that are designed to help programmers take backups of their projects more efficiently, especially when dealing with problematic folders such as `node_modules` and `venv`.

## main.py

The `main.py` script is a single-threaded implementation that copies files from the source directory to the destination directory. It provides a simple and straightforward way to take backups, but it may not be the most efficient option for large projects or when dealing with folders that cause backup issues.

## main2.py

The `main2.py` script is a more advanced implementation that utilizes multiprocessing to achieve maximum speed when copying files. By leveraging multiple cores, it significantly improves the backup process, making it ideal for larger projects or when dealing with problematic folders.

Both scripts are useful tools for programmers who need to take backups of their projects on physical storage devices. They provide a solution to the common problem of dealing with folders like `node_modules` and `venv`, which can cause issues and slow down the backup process.

Please note that these scripts are intended for use in Python projects and may not be suitable for other programming languages or scenarios. But you can always modify them to suit your needs.

> Note: It's for **Windows** only.

> Note: It's important to ensure that you have the necessary permissions and rights to access and copy files from the source directory to the destination directory.

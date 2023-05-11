#!/usr/bin/python3

import sys
import pathlib
import subprocess
import os

if len(sys.argv) != 3:
  print(f"usage: {sys.argv[0]} <origem> <destino>")
  exit(1)


file = pathlib.Path(sys.argv[1]).absolute()
original_file = file
parent = file.parent
destination = pathlib.Path(sys.argv[2])

if not destination.is_dir():
  print(destination, "não é um diretório! Abortando.")
  exit(1)

print("Fazendo backup de ", file, "para", destination, ".")
input("Pressione Enter para continuar. Ctrl+C para abortar.")
tar_created = False

if file.is_file():
  print(file, "já é um arquivo. Pulando o tar.")
elif file.is_dir():
  print(file, "é um diretório. Criando tar.")
  tarred = file.with_suffix(".tar")
  subprocess.check_call(["tar", "-C", parent, "-cvf", tarred, file.name])
  file = tarred
  tar_created = True
else:
  print(file, "tem um tipo não suportado! Abortando.")
  exit(1)

builtin_checksum = file.suffix in (".tar", ".gz", ".7z", ".zip", ".rar")

if builtin_checksum:
  print("Formato já tem um checksum imbutido. Pulando md5.")
else:
  md5 = file.with_extension("md5")
  print("Gerando checksum")
  subprocess.check_call(f"md5sum {file} > {md5}", shell=True)

print("Copiando arquivos para o destino")
subprocess.check_call(["cp", file, destination])
if not builtin_checksum:
  subprocess.check_call(["cp", md5, destination])

print("Arquivo(s) copiado(s).")

if tar_created:
  os.remove(file)

print("Para remover o arquivo original use:")
if original_file.is_dir():
  print(f"rm -r '{original_file}'")
else:
  print(f"rm", '{original_file}')

print("Adeus!")
